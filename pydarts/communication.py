"""
Module for user-backend communication.
"""


def __test_input(prompt):
    """Test input method mocking user input by returning the prompt."""
    return prompt

def __test_output(text):
    """Test output method silencing any output."""


METHOD = "standard"
INPUT_METHODS = {
    "standard": input,
    "testing": __test_input
    }
OUTPUT_METHODS = {
    "standard": print,
    "testing": __test_output
    }


def get_input(prompt, **kwargs):
    """Ask user for valid input. If invalid, display the error and repeat.
    kwargs are forwarded to 'sanitized_input'.
    """

    while True:
        try:
            return sanitized_input(prompt, **kwargs)
        except SanitizationError as e:
            OUTPUT_METHODS[METHOD](str(e))

            if isinstance(e, MinLargerMaxError):
                # re-raise to avoid infinite loop
                raise


class SanitizationError(Exception):
    """Raised if sanitization cannot be performed with given parameters."""

class MinLargerMaxError(SanitizationError):
    pass


def sanitized_input(prompt, method=METHOD, type_=None, min_=None, max_=None):
    """Helper method to retrieve sanitized user input.
    Attempts conversion to requested type and validates the input.
    Inspiration was taken from
    https://stackoverflow.com/questions/23294658/asking-the-user-for-input-until-they-give-a-valid-response

    :param prompt: Prompt to display when asking user for input
    :type prompt: str
    :param method: Method for communicating with user
    :type method: str
    :param type_: Expected type of the input. Defaults to str
    :param min_: Minimum value for input number, or minimum length for input string
    :param max_: Maximum value for input number
    """

    if min_ is not None and max_ is not None and max_ < min_:
        raise MinLargerMaxError("min_ must be less than or equal to max_.")

    ui = INPUT_METHODS[method](prompt)

    if type_ is not None:
        try:
            ui = type_(ui)
        except ValueError:
            raise SanitizationError(
                    "Input type must be {0}.".format(type_.__name__))

    if max_ is not None and ui > max_:
        raise SanitizationError(
                "Input must be less than or equal to {0}.".format(max_))
    elif min_ is not None:
        if type_ in [None, str]:
            if len(ui) < min_:
                raise SanitizationError(
                        "Input length must be greater of equal to {}".format(min_))
        else:
            if ui < min_:
                raise SanitizationError(
                        "Input must be greater than or equal to {0}.".format(min_))
    return ui
