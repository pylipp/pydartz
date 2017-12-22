from __future__ import print_function

import os.path
import sys
import time
import argparse

from .database import analyze_sessions, Sessions
from .game import Game
from .communication import CommunicatorBase, INFO_VISIT, INFO_FINISH, INFO_LEG
from .finishes import FINISHES

log_dir = os.path.expanduser("~/.local/share/pydartz")
os.makedirs(log_dir, exist_ok=True)
log_filepath = os.path.join(log_dir, "stats.xml")
open(log_filepath, "a").close()
sessions_log = Sessions(log_filepath=log_filepath)


def main():
    args = vars(_parse_command())
    player_names = args.pop("stats", None)

    if player_names is not None:
        player_entries = analyze_sessions(sessions_log._log_entry)
        for name, entry in player_entries.items():
            # pylint: disable=len-as-condition
            if len(player_names) and name not in player_names:
                continue
            print(entry.information())
        sys.exit(0)

    _display_license()
    time.sleep(1)
    os.system("cls || clear")
    _display_banner()

    g = Game(CliCommunicator(), sessions_log)
    g.run()

    _play_ending_song()


class CliCommunicator(CommunicatorBase):
    """Command Line Interface communicator that request user input using
    Python's builtin '(raw_)input' method and that prints to stdout.
    """

    def __init__(self):
        super(CliCommunicator, self).__init__(
            raw_input if sys.version_info.major < 3 else input, print)

    def print_info(self, message_type, **data):
        output = None

        if message_type == INFO_VISIT:
            player = data["player"]
            output = "{p.name} has {p.score_left} and {0} left.".format(
                ["one dart", "two darts", "three darts"][player.darts - 1],
                p=player)
        elif message_type == INFO_FINISH:
            player = data["player"]
            score_left = str(player.score_left)
            if score_left in FINISHES:
                output = "Finish options:"
                for finish in FINISHES[score_left]:
                    output += "\n\t" + " ".join(finish)
        elif message_type == INFO_LEG:
            players = data["players"]
            output = "\n".join(
                        "    {}: {:2d}".format(p.name, p.nr_won_legs)
                        for p in players)
            output += "\n"
            output += 80 * "="

        if output is not None:
            self._output_info_method(output)

    def print_error(self, **data):
        output = str(data["error"])
        self._output_error_method(output)


def _parse_command():
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--stats", metavar="NAME", nargs="*",
            help="display player stats")

    return parser.parse_args()


def _display_license():
    print("""\
pydartz  Copyright (C) 2017  Philipp Metzner
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
""")


# pylint: disable=line-too-long
def _display_banner():
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

def _play_ending_song():
    try:
        import simpleaudio
        wave_obj = simpleaudio.WaveObject.from_wave_file(
                os.path.join(sys.prefix, "data", "chase_the_sun.wav"))
        play_obj = wave_obj.play()
        play_obj.wait_done()
    except ImportError:
        print("Run 'pip install simpleaudio==1.0.1' for sound support!")
