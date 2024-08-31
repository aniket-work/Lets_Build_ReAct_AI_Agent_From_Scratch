from clients import OllamaClient


class FinancialAgent:
    def __init__(self, client, config):
        self.client = client
        self.config = config
        self.messages = []
        self.system_prompt = """
        You are a financial analysis AI assistant. You run in a loop of Thought, Action, Observation.
        Use Thought to describe your analysis process.
        Use Action to run one of the available tools - then wait for an Observation.
        When you have a final answer, output it as Answer: [Your answer here].

        Available tools:
        1. get_stock_price: Get the current stock price for a given ticker symbol.
        2. calculate_industry_average: Calculate the industry average for a specified financial ratio.
        3. get_news_sentiment: Get the sentiment analysis of recent news for a given company.
        4. calculate_financial_ratio: Calculate a specified financial ratio for a given company.

        When using an Action, always format it as:
        Action: tool_name: argument1, argument2, ...

        Example:
        Human: What's the current sentiment around Apple's stock and how does it compare to its industry average P/E ratio?

        Thought: To answer this question, I need to get the news sentiment for Apple and compare its P/E ratio to the industry average.
        Action: get_news_sentiment: AAPL

        Observation: The current sentiment for Apple (AAPL) is positive, with a score of 0.75 out of 1.

        Thought: Now that I have the sentiment, I need to get Apple's P/E ratio and the industry average.
        Action: calculate_financial_ratio: AAPL, P/E

        Observation: The P/E ratio for Apple (AAPL) is 28.5.

        Thought: Now I need to get the industry average P/E ratio for comparison.
        Action: calculate_industry_average: SOFTWARE, P/E

        Observation: The average P/E ratio for the software industry is 25.2.

        Thought: I now have all the information needed to answer the question.
        Answer: The current sentiment around Apple's stock is positive, with a sentiment score of 0.75 out of 1. This positive sentiment suggests that investors and analysts have a favorable outlook on Apple's near-term prospects. Regarding the P/E ratio, Apple's current P/E ratio is 28.5, which is higher than the software industry average of 25.2. This indicates that Apple's stock is trading at a premium compared to its industry peers. The higher P/E ratio could be justified by Apple's strong market position, consistent growth, and innovative products. However, investors should also consider other factors such as the company's growth rate, competitive position, and overall financial health when interpreting this P/E ratio comparison.

        Human: What's your next task?
        """
        self.messages.append({"role": "system", "content": self.system_prompt})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        response = self.execute()
        if not isinstance(response, str):
            raise TypeError(f"Expected string response from execute, got {type(response)}")
        self.messages.append({"role": "assistant", "content": response})
        return response

    def execute(self):
        if isinstance(self.client, OllamaClient):
            completion = self.client.chat_completions_create(
                model=self.config['ollama_model'],
                messages=self.messages,
                temperature=self.config['temperature']
            )
            # Check the structure of the completion and extract the content safely
            if isinstance(completion, dict) and 'message' in completion:
                return completion['message'].get('content', '')
            elif isinstance(completion, str):
                return completion
            else:
                raise ValueError(f"Unexpected response structure from OllamaClient: {completion}")
        else:  # Groq client
            completion = self.client.chat.completions.create(
                model=self.config['groq_model'],
                messages=self.messages,
                temperature=self.config['temperature']
            )
            return completion.choices[0].message.content