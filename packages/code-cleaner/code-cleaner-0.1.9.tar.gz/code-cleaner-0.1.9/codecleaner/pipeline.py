class Pipeline():
    """
    Defines a pipeline
    """

    def __init__(self, callables):
        """
        Constructor of the class. Accepts a dictionary of configurations that will be used to define the workflow of the
        class.
        """
        self.callables = callables

    def run(self, item):
        """
        Applies all the cleaning algorithms to the text
        """
        for callable_object in self.callables:
            item = callable_object.run(item)
        return item
