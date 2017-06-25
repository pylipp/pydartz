import os.path
import argparse

from lxml import etree
import simpleaudio

from .session import Session
from .database import analyze_sessions, sessions_log
from .communication import get_input


dirname = os.path.dirname(os.path.abspath(__file__))


def main():
    args = vars(_parse_command())
    player_names = args.pop("stats", None)

    if player_names is not None:
        player_entries = analyze_sessions(sessions_log)
        for name, entry in player_entries.items():
            if len(player_names) and name not in player_names:
                continue
            entry.print_info()
        import sys; sys.exit(0)

    s = _setup_session()
    s.run()

    _play_ending_song()

def _parse_command():
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--stats", metavar="NAME", nargs="*",
            help="display player stats")

    return parser.parse_args()

def _setup_session():
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

    nr_players = get_input("Nr of players: ", type_=int, min_=1)

    names = []
    for i in range(nr_players):
        name = get_input("Name of player {}: ".format(i+1), min_=1)
        names.append(name)

    start_value = get_input("Start value: ", type_=int, min_=2)

    nr_legs = get_input("Nr of legs: ", type_=int, min_=1)

    return Session(names, start_value, nr_legs, log_parent=sessions_log)

def _play_ending_song():
    wave_obj = simpleaudio.WaveObject.from_wave_file(
            os.path.join(dirname, "..", "data", "chase_the_sun.wav"))
    play_obj = wave_obj.play()
    play_obj.wait_done()
