from Summoner import *

def main():
    names = [""]
    for name in names:
        result = Summoner(name).query()
        print(result)

if __name__ == "__main__":
    main()
