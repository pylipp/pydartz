import os.path
import argparse

from tinydb import where
from lxml import etree
import simpleaudio

from .session import Session
from .database import analyze_sessions


dirname = os.path.dirname(os.path.abspath(__file__))
log_filepath = os.path.join(dirname, "..", "data", "stats.xml")

if os.path.exists(log_filepath):
    tree = etree.parse(log_filepath)
    sessions_log = tree.getroot()
else:
    sessions_log = etree.Element("sessions")


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

    tree = etree.ElementTree(sessions_log)
    tree.write(log_filepath, pretty_print=True, xml_declaration=True,
            encoding="utf-8")

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

    while True:
        try:
            nr_players = int(input("Nr of players: "))
            if nr_players >= 1:
                break
        except (ValueError):
            print("Invalid input.")

    names = []
    for i in range(nr_players):
        name = input("Name of player {}: ".format(i+1))
        names.append(name)

    while True:
        try:
            start_value = int(input("Start value: "))
            if start_value >= 2:
                break
        except (ValueError):
            print("Invalid input.")

    while True:
        try:
            nr_legs = int(input("Nr of legs: "))
            if nr_legs > 0:
                break
        except (ValueError):
            print("Invalid input.")

    return Session(names, start_value, nr_legs, log_parent=sessions_log)

def _play_ending_song():
    wave_obj = simpleaudio.WaveObject.from_wave_file(
            os.path.join(dirname, "..", "data", "chase_the_sun.wav"))
    play_obj = wave_obj.play()
    play_obj.wait_done()
