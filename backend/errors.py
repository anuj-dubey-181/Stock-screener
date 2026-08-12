class DSLParsingError(Exception):

    def __init__(self, message):
        self.code = "DSL_PARSING_ERROR"
        self.message = message
        super().__init__(self.message)


class DSLValidationError(Exception):

    def __init__(self, message):
        self.code = "DSL_VALIDATION_ERROR"
        self.message = message
        super().__init__(self.message)


class APIError(Exception):

    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(self.message)