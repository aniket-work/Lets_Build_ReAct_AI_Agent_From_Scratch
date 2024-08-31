import json
from dotenv import load_dotenv
import os
from groq import Groq
from agent import FinancialAgent
from clients import OllamaClient
from tools.stock_data import get_stock_price
from tools.financial_calculations import calculate_financial_ratio, calculate_industry_average
from tools.news_sentiment import get_news_sentiment

load_dotenv()


def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)


def get_client(config):
    if config.get('use_groq', False):
        return Groq(api_key=os.environ.get("GROQ_API_KEY"))
    else:
        return OllamaClient()


def main():
    config = load_config()
    try:
        client = get_client(config)
        agent = FinancialAgent(client, config)
    except Exception as e:
        print(f"Error initializing the AI client: {str(e)}")
        print("Please check your configuration and ensure the AI service is running.")
        return

    tools = {
        "get_stock_price": get_stock_price,
        "calculate_industry_average": calculate_industry_average,
        "get_news_sentiment": get_news_sentiment,
        "calculate_financial_ratio": calculate_financial_ratio
    }

    query = input("Enter your financial analysis query: ")

    iteration = 0
    while iteration < config['max_iterations']:
        try:
            result = agent(query)
            print(result)

            if "Action:" in result:
                action_parts = result.split("Action:", 1)[1].strip().split(": ", 1)
                tool_name = action_parts[0]
                tool_args = action_parts[1] if len(action_parts) > 1 else ""

                if tool_name in tools:
                    try:
                        observation = tools[tool_name](tool_args)
                        query = f"Observation: {observation}"
                    except Exception as e:
                        query = f"Observation: Error occurred while executing the tool: {str(e)}"
                else:
                    query = f"Observation: Tool '{tool_name}' not found"

            elif "Answer:" in result:
                break
            else:
                query = "Observation: No valid action or answer found. Please provide a clear action or answer."

        except Exception as e:
            print(f"An error occurred while processing the query: {str(e)}")
            print("Please check your configuration and ensure the AI service is running.")
            break

        iteration += 1

    if iteration == config['max_iterations']:
        print("Reached maximum number of iterations without a final answer.")


if __name__ == "__main__":
    main()
