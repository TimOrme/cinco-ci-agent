class Pipeline:

    def __init__(self, steps):
        self.steps = steps


class Step:

    def __init__(self, function):
        self.function = function

    def __call__(self):
        self.function()
