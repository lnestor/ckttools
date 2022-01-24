class Gate:
    def __init__(self, output, type_, inputs):
        self.output = output
        self.type = type_
        self.inputs = inputs

    def __str__(self):
        return "%s = %s(%s)" % (self.output, self.type, ", ".join(self.inputs))
