from .communication import INFO_VISIT, INFO_FINISH, INPUT_THROW


#pylint: disable=too-many-instance-attributes
class Player:
    """Representation of a player.
    Holds long-term, per-game and per-visit information. Provides routines to
    perform a classic 501.
    Each player has a unique name that are passed at initialization.
    It is also required to pass a start value to initialize the player's
    remaining score."""

    INDEX = 0

    def __init__(self, name, start_value=501, communicator=None):
        self._name = name
        self._index = Player.INDEX
        Player.INDEX += 1
        self._start_value = start_value
        self._nr_won_legs = 0
        self._communicator = communicator

        self._score_left = start_value
        self._throws = 0

        self._darts = 3
        self._visit = []

    def begin(self):
        """Reset actions at the beginning of a player's turn."""
        if self._visit:
            self._visit = []
        self._darts = 3

    def reset(self):
        """Reset actions at the beginning of a leg."""
        self._throws = 0
        self._score_left = self._start_value

    def victorious(self):
        return self._score_left == 0

    def substract(self, score, is_total=True):
        """Substract `score` from the player's `score_left`. If `is_total` is
        true or if the score is obviously the last one of a player's turn, the
        number of remaining darts is set to zero.
        Note that score has to be valid since this method does not do any
        checks on its own."""
        self._score_left -= score
        #TODO this logic should be moved to _process_score
        if is_total or score + sum(self._visit) == 180:
            self._throws += self._darts
            self._darts = 0
        else:
            self._throws += 1
            self._darts -= 1
        self._visit.append(score)

    def score_valid(self, score):
        """Check whether `score` is valid, i.e. the current visit must not
        exceed 180, the player must not be busted and the score has to be
        legitimatly thrown (e.g. one cannot score 130 with two remaining darts.)

        Raises a ValueError if the score is invalid.
        """
        difference = self._score_left - score

        if score + sum(self._visit) > 180 or \
                score > 60 * self._darts or \
                difference < 0 or difference == 1:
            raise ValueError

        return True

    def print_info(self):
        """Print information on player's left score and darts and, optionally,
        finishing options."""
        self._communicator.print_info(INFO_VISIT, player=self)
        self._communicator.print_info(INFO_FINISH, player=self)

    @property
    def score_left(self):
        return self._score_left

    @property
    def darts(self):
        return self._darts

    @property
    def name(self):
        return self._name

    @property
    def throws(self):
        return self._throws

    def visit_sum(self):
        return sum(self._visit)

    @property
    def nr_won_legs(self):
        return self._nr_won_legs

    def just_won_leg(self):
        self._nr_won_legs += 1

    def play(self):
        """Read score input given by the user while checking for errors.
        Player information is printed before each throw. If _process_score()
        does not raise any errors, the input score is substracted from the
        player's remaining score.
        The procedure is repeated if the player has darts remaining and has not
        yet won.
        """
        self.begin()

        while self._darts and not self.victorious():
            self.print_info()
            input_ = self._communicator.get_input(INPUT_THROW, self._name)
            try:
                score, is_total = self._process_score(input_)
                self.substract(score, is_total)
            except ValueError as e:
                self._communicator.print_error(error=e)

    def _process_score(self, score):
        """Parse the passed score. Valid options are:
        - x (an integer between 0 and 180)
        - xd (an integer between 0 and 180, with the character 'd' appended,
          indicating that the player's turn is over ('done'))
        - d (equivalent to '0d')
        - b (the character 'b', indicating that the player busted. The player's
          score will be reset in substract())
        A ValueError is thrown if an invalid score is passed. This can be
        caused by a score that exceeds the remaining score allowed in the
        current visit or by a typo."""
        try:
            score = score.lower()
            if score.endswith("d"):
                if len(score) == 1:
                    score = 0
                else:
                    score = int(score[:-1])
                is_total = True
            elif score == "b":
                # player busted, undo whatever he scored so far in his turn
                # all three darts are taken into account for the average, see
                # http://www.dartsnutz.net/forum/archive/index.php/thread-18910.html
                score = -self.visit_sum()
                is_total = True
            else:
                score = int(score)
                is_total = False

            if self.score_valid(score):
                return score, is_total
        except (ValueError):
            # custom message
            raise ValueError("Invalid input: {}".format(score))
