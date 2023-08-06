class Model:
    def __init__(self, *args, **kwargs):
        self.args = args
        for kwarg in kwargs:
            setattr(self, kwarg, kwargs[kwarg])
