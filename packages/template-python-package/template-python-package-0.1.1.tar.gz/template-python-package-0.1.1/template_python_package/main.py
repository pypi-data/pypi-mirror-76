
class TemplateMain:
    """A template class main

    Parameters
    ----------
    prop1 : str
        Property 1 for the class

    prop2: str
        Property 2 for the class
    """
    def __init__(self, prop1, prop2):
        self.prop1 = prop1
        self.prop2 = prop2

    def dict(self):
        return {
            'prop1': self.prop1,
            'prop2': self.prop2
        }

    def tuple(self):
        return self.prop1, self.prop2

    def list(self):
        return [self.prop1, self.prop2]

    def set(self):
        return {self.prop1, self.prop2}

    def __repr__(self):
        return f'TemplateMain, <id: {id(self)}>'
