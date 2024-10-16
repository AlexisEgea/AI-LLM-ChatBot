from abc import ABC, abstractmethod
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser


class ModelAI(ABC):
    def __init__(self, model_name, input_price, output_price):
        self.model = None
        self.model_name = model_name

        self.memory = ""
        self.limit_memory_size = 1000

        self.input_price = input_price
        self.output_price = output_price

        self.total_cost = 0

    @abstractmethod
    def init_model(self):
        pass

    @abstractmethod
    def get_response(self, message):
        pass

    @abstractmethod
    def count_cost_conversation(self, response_package):
        pass

    @abstractmethod
    def display_cost(self, response_package):
        pass

    def update_memory(self):
        if len(self.memory) > self.limit_memory_size:
            print("AI: Memory exceeded, summary activated.")
            with open('src/metadata/summarize/instruction.md', 'r') as instruction_file:
                instruction = instruction_file.read()

            message_package = [
                SystemMessage(content=instruction),
                HumanMessage(content=self.memory),
            ]

            response_package = self.model.invoke(message_package)
            self.memory = StrOutputParser().invoke(response_package)

            self.count_cost_conversation(response_package)

            self.limit_memory_size += len(self.memory) / 2


