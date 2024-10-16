import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

from src.model.model_ai import ModelAI


class OpenaiModel(ModelAI):
    def __init__(self, model_name, input_price, output_price):
        load_dotenv()
        super().__init__(model_name, input_price, output_price)
        self.open_ai_key = os.getenv("OPENAI_API_KEY")
        self.total_cost = 0
        self.model = None
        self.init_model()

    def init_model(self):
        self.model = ChatOpenAI(model=self.model_name)

    def get_response(self, message):
        with open('src/metadata/chat_bot/instruction.md', 'r') as instruction_file:
            instruction = instruction_file.read()

        message_package = [
            SystemMessage(content=instruction),
            SystemMessage(content=self.memory),
            HumanMessage(content=message),
        ]

        response_package = self.model.invoke(message_package)
        response = StrOutputParser().invoke(response_package)

        self.update_memory(message, response)
        self.count_cost_conversation(response_package)

        # Uncomment to see price per question
        # self.display_cost(response_package)

        return response

    # TODO: finish this part by calling a new self.model.invoke(message_package) for memory resume
    def update_memory(self, message, response):
        if len(self.memory) > self.limit_memory_size:
            self.limit_memory_size += len(self.memory) / 2
            pass
        self.memory += (f"User: {message}\n"
                        f"AI:{response}\n")

    def count_cost_conversation(self, response_package):
        input_tokens = response_package.usage_metadata['input_tokens']
        output_tokens = response_package.usage_metadata['output_tokens']

        input_price = (input_tokens / 1000000) * self.input_price
        output_price = (output_tokens / 1000000) * self.output_price

        self.total_cost += input_price + output_price

    def display_cost(self, response_package):
        input_tokens = response_package.usage_metadata['input_tokens']
        output_tokens = response_package.usage_metadata['output_tokens']
        total_tokens = input_tokens + output_tokens

        input_price = (input_tokens / 1000000) * self.input_price
        output_price = (output_tokens / 1000000) * self.output_price
        total_price = input_price + output_price

        print("\nTokens:")
        print(f"Input: {input_tokens} -> {format(input_price, '.10f')}$")
        print(f"Output: {output_tokens} -> {format(output_price, '.10f')}$")
        print(f"Total: {total_tokens} -> {format(total_price, '.10f')}$\n")
