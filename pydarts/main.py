import os.path
import sys
import argparse

from .database import analyze_sessions, sessions_log
from .game import Game
from .communication import CliCommunicator


dirname = os.path.dirname(os.path.abspath(__file__))


def main():
    args = vars(_parse_command())
    player_names = args.pop("stats", None)

    if player_names is not None:
        player_entries = analyze_sessions(sessions_log)
        for name, entry in player_entries.items():
            # pylint: disable=len-as-condition
            if len(player_names) and name not in player_names:
                continue
            entry.print_info()
        sys.exit(0)

    _display_banner()
    g = Game(CliCommunicator())
    g.run()

    _play_ending_song()

def _parse_command():
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--stats", metavar="NAME", nargs="*",
            help="display player stats")

    return parser.parse_args()

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
                os.path.join(dirname, "..", "data", "chase_the_sun.wav"))
        play_obj = wave_obj.play()
        play_obj.wait_done()
    except ImportError:
        print("Run 'pip install simpleaudio==1.0.1' for sound support!")
