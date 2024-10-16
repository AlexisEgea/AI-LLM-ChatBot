class ModelAI:
    def __init__(self, model_name, input_price, output_price):
        self.model = None
        self.model_name = model_name

        self.memory = ""
        self.limit_memory_size = 1000

        self.input_price = input_price
        self.output_price = output_price