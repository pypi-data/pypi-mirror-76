""" Error type. The key value database
forces the user to use string typed keys"""

class KeyStringError(TypeError):
    """ Key String Error. A Key has to be a string """
    def __init__(self, message: str = "Key/name must be a string!"):
        """ init my error
            Arguments:
                message(str): message string
        """
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        """get error message
        Returns:
            str: error message. The key is of string type!!!
        """
        return self.message
