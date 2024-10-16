from src.model.openai.openai_cost import OPENAI_COST
from src.model.openai.openai import OpenaiModel

class ModelFactory:
    def __init__(self, model_name):
        self.model_name = model_name

    def get_model(self):
        if self.model_name in OPENAI_COST:
            input_price = OPENAI_COST[self.model_name]['input_price']
            output_price = OPENAI_COST[self.model_name]['output_price']
            return OpenaiModel(self.model_name, input_price, output_price)

        raise ValueError(f"Model '{self.model_name}' not supported for this project.")
