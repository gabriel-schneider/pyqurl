class UnknownOperatorError(Exception):
    def __init__(self, operator, message="The operator is unknown!"):
        self.operator = operator
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"The operator {self.operator} is unknown!"