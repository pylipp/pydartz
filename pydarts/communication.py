"""
Module for user-backend communication.
"""
from __future__ import print_function

from collections import deque


class CommunicatorBase(object):
    """Communicators provide a high-level interface to fetch data requested by
    the game routine and to display information about game stastics.
    The only member variables are two callables functioning as input and output
    method, resp.
    """

    def __init__(self, input_method, output_method):
        self._input_method = input_method
        self._output_method = output_method

    def get_input(self, prompt=None, **kwargs):
        """Prompt the user to give valid input. If invalid, display error and
        repeat. kwargs are forwarded to 'sanitized_input'."""
        while True:
            try:
                user_input = self._input_method(prompt or "")
                return sanitized_input(user_input, **kwargs)
            except SanitizationError as e:
                self.print_output(str(e))

                if isinstance(e, MinLargerMaxError):
                    # re-raise to avoid infinite loop
                    raise

    def print_output(self, text):
        """Print some info to the frontend."""
        self._output_method(str(text))

class CliCommunicator(CommunicatorBase):
    """Command Line Interface communicator that request user input using
    Python's builtin 'input' method and that prints to stdout.
    """

    def __init__(self):
        super().__init__(input, print)

class TestingCommunicator(CommunicatorBase):
    """Communicator for testing game procedures (visits, legs, sessions).
    Requires sensible input data representing throws or visits.
    """

    def __init__(self, *data):
        self._data = deque((str(d) for d in data))
        def pop(deque_):
            return deque_.popleft()
        super().__init__(pop, lambda _: None)

    def get_input(self, prompt=None, **kwargs):
        """Pop element from data deque."""
        return super().get_input(prompt=self._data, **kwargs)

    def print_output(self, text):
        """Does not display any text. Re-raises any exception being passed."""
        if issubclass(text.__class__, Exception):
            raise text


class RosCommunicator(CommunicatorBase):
    """Subclass providing communication using ROS via the '/get_input' service
    and the 'print_output' topic.
    """

    def get_input(self, prompt=None, **kwargs):
        """The user reply is a ServiceResponse object that the actual reply
        string has to be passed to sanitized_input().
        """
        while True:
            try:
                user_input = self._input_method(prompt or "").reply
                return sanitized_input(user_input, **kwargs)
            except SanitizationError as e:
                self.print_output(str(e))

                if isinstance(e, MinLargerMaxError):
                    # re-raise to avoid infinite loop
                    raise

def create_communicator(kind, *args, **kwargs):
    kind = kind.lower()
    if kind == "cli":
        return CliCommunicator()
    elif kind == "testing":
        return TestingCommunicator(*args, **kwargs)
    else:
        raise ValueError("Unknown communicator kind '{}'.".format(kind))

def sanitized_input(ui, type_=None, min_=None, max_=None):
    """Helper method to retrieve sanitized user input.
    Attempts conversion to requested type and validates the input.
    Input that's supposed to be string is stripped from whitespace.
    Inspiration was taken from
    https://stackoverflow.com/questions/23294658/asking-the-user-for-input-until-they-give-a-valid-response

    :param ui: user input that is to be sanitized
    :param type_: Expected type of the input. Defaults to str
    :param min_: Minimum value for input number, or minimum length for input string
    :param max_: Maximum value for input number
    """

    if min_ is not None and max_ is not None and max_ < min_:
        raise MinLargerMaxError("min_ must be less than or equal to max_.")

    if type_ is not None:
        try:
            ui = type_(ui)
        except ValueError:
            raise SanitizationError(
                    "Input type must be {0}.".format(type_.__name__))
        if type_ is str:
            ui = ui.strip()

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

class SanitizationError(Exception):
    """Raised if sanitization cannot be performed with given parameters."""

class MinLargerMaxError(SanitizationError):
    pass
