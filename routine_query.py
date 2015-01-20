#!/usr/bin/env python
from Summoner import *


def main():
    names = [
        "你根本在發廢文",
        "嵐辰星月夜",
        "性侵大使",
        "人品爆發揪咪030",
        "戰神露特娜",
        "Aragorn",
        "Salas",
        "HappyStrom",
    ]
    for name in names:
        result = Summoner(name).get_recent_games()
        print(result)

if __name__ == "__main__":
    main()
