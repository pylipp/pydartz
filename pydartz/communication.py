"""Module for user-backend communication."""

from collections import deque
from abc import ABCMeta, abstractmethod


INFO_VISIT, INFO_FINISH, INFO_LEG = range(3)
INPUT_NR_PLAYERS, INPUT_START_VALUE, INPUT_PLAYER_NAME, INPUT_NR_LEGS,\
    INPUT_ANOTHER_SESSION, \
    INPUT_THROW = range(6)


class CommunicatorBase:
    """Communicators provide a high-level interface to fetch data requested by
    the game routine and to display information about game stastics.
    The only member variables are three callables functioning as input and
    output (info and error) method, resp.
    A dictionary contains prompts for all possible input queries including
    sanitization kwargs. It can be overwritten in subclasses.
    """

    __metaclass__ = ABCMeta

    def __init__(self, input_method, output_info_method,
                 output_error_method=None):
        self._input_method = input_method
        self._output_info_method = output_info_method
        self._output_error_method = output_error_method or output_info_method
        self._input_prompts = {
            INPUT_NR_PLAYERS: {
                "prompt": "Nr of players: ",
                "kwargs": {"type_": int, "min_": 1},
            },
            INPUT_START_VALUE: {
                "prompt": "Start value: ",
                "kwargs": {"type_": int, "min_": 2},
            },
            INPUT_PLAYER_NAME: {
                "prompt": "Name of player {}: ",
                "kwargs": {"min_": 1},
            },
            INPUT_NR_LEGS: {
                "prompt": "Nr of legs: ",
                "kwargs": {"type_": int, "min_": 1},
            },
            INPUT_ANOTHER_SESSION: {
                "prompt": "Again (y/n/q)? ",
                "kwargs": {"choices": "ynq"},
            },
            INPUT_THROW: {
                "prompt": "{}'s score: ",
                "kwargs": {},
            },
        }

    def get_input(self, input_mode, *format_args):
        """Prompt the user to give valid input. If invalid, display error and
        repeat. Prompt parameters are read acc. to the given `input_mode` and,
        if specified, formatted using `format_args`.
        """
        while True:
            prompt_parameters = self._input_prompts[input_mode]
            prompt = prompt_parameters["prompt"].format(*format_args)
            kwargs = prompt_parameters["kwargs"]
            try:
                user_input = self._input_method(prompt)
                return sanitized_input(user_input, **kwargs)
            except SanitizationError as e:
                self.print_error(error=e)

                if isinstance(e, MinLargerMaxError):
                    # re-raise to avoid infinite loop
                    raise

    @abstractmethod
    def print_info(self, message_type, **data):
        """Print some info to the frontend."""

    @abstractmethod
    def print_error(self, **data):
        """Report error to the frontend."""


class TestingCommunicator(CommunicatorBase):
    """Communicator for testing game procedures (visits, legs, sessions).
    Requires sensible input data representing throws or visits.
    """

    def __init__(self, *data):
        self._data = deque((str(d) for d in data))
        def pop(deque_):
            return deque_.popleft()
        super().__init__(pop, lambda _: None)

    def get_input(self, input_mode=INPUT_THROW, *format_args):
        """Pop element from data deque."""
        element = self._input_method(self._data)
        return sanitized_input(element,
                               **self._input_prompts[input_mode]["kwargs"])

    def print_info(self, message_type, **data):
        """Does not do anything."""

    def print_error(self, **data):
        """Does not display any text. Re-raises any exception being passed."""
        raise data["error"]


def sanitized_input(ui, type_=str, min_=None, max_=None, choices=None):
    """Helper method to retrieve sanitized user input.
    Attempts conversion to requested type and validates the input.
    Input that's supposed to be string is stripped from whitespace.
    Inspiration was taken from
    https://stackoverflow.com/questions/23294658/asking-the-user-for-input-until-they-give-a-valid-response

    :param ui: user input that is to be sanitized
    :param type_: Expected type of the input. Defaults to str
    :param min_: Minimum value for input number, or minimum length for input str
    :param max_: Maximum value for input number, or maximum length for input str
    :param choices: Iterable that the input has to be contained in,
        default: None, meaning that no check is performed
    """

    if min_ is not None and max_ is not None and max_ < min_:
        raise MinLargerMaxError("min_ must be less than or equal to max_.")

    if type_ is not None:
        try:
            ui = type_(ui)
        except ValueError:
            raise SanitizationError(
                    "Input != {0}.".format(type_.__name__))
        if type_ is str:
            ui = ui.strip()

    if max_ is not None:
        if type_ is str:
            if len(ui) > max_:
                raise SanitizationError("Input length > {}".format(max_))
        else:
            if ui > max_:
                raise SanitizationError("Input > {}".format(max_))
    elif min_ is not None:
        if type_ is str:
            if len(ui) < min_:
                raise SanitizationError("Input length < {}".format(min_))
        else:
            if ui < min_:
                raise SanitizationError("Input < {}".format(min_))

    if choices is not None:
        if not len(str(ui)) or ui not in choices:
            raise SanitizationError("Input != [{}]".format(
                ",".join((str(c) for c in choices))))

    return ui


class SanitizationError(Exception):
    """Raised if sanitization cannot be performed with given parameters."""

class MinLargerMaxError(SanitizationError):
    pass
