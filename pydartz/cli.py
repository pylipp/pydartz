import argparse
import os
import shutil
import sys
import time

from . import __version__
from .communication import INFO_FINISH, INFO_LEG, INFO_VISIT, CommunicatorBase
from .database import Sessions, analyze_sessions
from .finishes import FINISHES
from .game import Game

log_dir = os.path.expanduser("~/.local/share/pydartz")
os.makedirs(log_dir, exist_ok=True)
log_filepath = os.path.join(log_dir, "stats.xml")
with open(log_filepath, "a"):
    pass
sessions_log = Sessions(log_filepath=log_filepath)


def main():
    args = vars(_parse_command())
    player_names = args.pop("stats", None)

    if player_names is not None:
        player_entries = analyze_sessions(sessions_log._log_entry)
        for name, entry in player_entries.items():
            if len(player_names) and name not in player_names:
                continue
            print(entry.information())
        sys.exit(0)

    time.sleep(1)
    os.system("cls || clear")
    _display_banner()

    g = Game(CliCommunicator(), sessions_log)
    try:
        g.run()
        _play_ending_song()
    except KeyboardInterrupt:
        print("\n\nUser quit by pressing Ctrl-C. Good bye!")


class CliCommunicator(CommunicatorBase):
    """Command Line Interface communicator that request user input using
    Python's builtin 'input' method and that prints to stdout.
    """

    def __init__(self):
        super().__init__(input, print)

    def print_info(self, message_type, **data):
        output = None

        if message_type == INFO_VISIT:
            player = data["player"]
            info = ["no darts", "one dart", "two darts", "three darts"][player.darts]
            output = f"{player.name} has {player.score_left} and {info} left."
        elif message_type == INFO_FINISH:
            player = data["player"]
            score_left = str(player.score_left)
            if score_left in FINISHES:
                output = "Finish options:"
                for finish in FINISHES[score_left]:
                    output += "\n\t" + " ".join(finish)
        elif message_type == INFO_LEG:
            players = data["players"]
            output = "\n".join(f"    {p.name}: {p.nr_won_legs:2d}" for p in players)
            output += "\n"
            output += 80 * "="

        if output is not None:
            self._output_info_method(output)

    def print_error(self, **data):
        output = str(data["error"])
        self._output_error_method(output)


def _parse_command():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-s", "--stats", metavar="NAME", nargs="*", help="display player stats"
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"pydartz version {__version__}",
        help="display version info and exit",
    )  # pragma: no cover

    return parser.parse_args()


def _display_banner():
    terminal_width = shutil.get_terminal_size((80, 20)).columns
    if terminal_width < 94:
        # Display smaller banner for narrow terminals
        print(" pydarts ".center(terminal_width, "#"))
        return

    # fmt: off
    print(r"      ___                                   ___           ___                         ___     ")
    print(r"     /\  \                   _____         /\  \         /\  \                       /\__\    ")
    print(r"    /::\  \       ___       /::\  \       /::\  \       /::\  \         ___         /:/ _/_   ")
    print(r"   /:/\:\__\     /|  |     /:/\:\  \     /:/\:\  \     /:/\:\__\       /\__\       /:/ /\  \  ")
    print(r"  /:/ /:/  /    |:|  |    /:/  \:\__\   /:/ /::\  \   /:/ /:/  /      /:/  /      /:/ /::\  \ ")
    print(r" /:/_/:/  /     |:|  |   /:/__/ \:|__| /:/_/:/\:\__\ /:/_/:/__/___   /:/__/      /:/_/:/\:\__\ ")
    print(r" \:\/:/  /    __|:|__|   \:\  \ /:/  / \:\/:/  \/__/ \:\/:::::/  /  /::\  \      \:\/:/ /:/  /")
    print(r"  \::/__/    /::::\  \    \:\  /:/  /   \::/__/       \::/~~/~~~~  /:/\:\  \      \::/ /:/  / ")
    print(r"   \:\  \    ~~~~\:\  \    \:\/:/  /     \:\  \        \:\~~\      \/__\:\  \      \/_/:/  /  ")
    print(r"    \:\__\        \:\__\    \::/  /       \:\__\        \:\__\          \:\__\       /:/  /   ")
    print(r"     \/__/         \/__/     \/__/         \/__/         \/__/           \/__/       \/__/    ")
    print()
    # fmt: on


def _play_ending_song():
    data_directory = "data"
    filename = "chase_the_sun.wav"
    try:
        import simpleaudio

        wave_obj = simpleaudio.WaveObject.from_wave_file(
            os.path.join(sys.prefix, data_directory, filename)
        )
        play_obj = wave_obj.play()
        play_obj.wait_done()
    except ImportError:
        try:
            import subprocess

            media_player = os.getenv("PYDARTZ_MEDIA_PLAYER", "mpv")
            subprocess.run(
                [media_player, f"{data_directory}/{filename}"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception:
            print("Run 'pip install -U pydartz[audio]' for sound support!")
