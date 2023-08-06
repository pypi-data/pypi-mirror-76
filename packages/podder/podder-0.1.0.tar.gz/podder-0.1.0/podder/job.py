class Job():
    def __init__(self, data: dict):
        self.data = data

    def __str__(self):
        return str(self.data)

    def __getattr__(self, name):
        if name in self.data:
            return self.data[name]
        else:
            raise AttributeError(f'No such attribute: {name}')
