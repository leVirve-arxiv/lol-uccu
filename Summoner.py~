import os
import re
import json
import pickle
import requests
from pymongo import *

from util_method import *

try:
	client = MongoClient(os.environ['OPENSHIFT_MONGODB_DB_URL'])
except KeyError:
	client = MongoClient()

class Summoner:
    def __init__(self, name):
        self.games = client.lol.games
        self.summoner_name = name
        self.id = self.getid()
        self.data = self.load()
        self.new_data_raw = []
        self.tzinfo = TaipeiTimeZone()

    def getid(self):
        url = 'http://lol.moa.tw/summoner/show/' + self.summoner_name
        response = requests.get(url)
        id_obj = re.findall(r'MoaObj.lol.acctId = (.+);', response.text)
        return id_obj[0] if id_obj else None

    def get_recent_games(self):
        try:
            url = 'http://lol.moa.tw/Ajax/bs_recentgames/' + self.id + '/' + self.summoner_name
            response = requests.get(url)
            result = re.findall(r'var recentgames=(.+);', response.text)
            self.json_data = json.loads(result[0])
            self.data |= self.get_recent_times()
            self.data = sorted(self.data)
            self.dump()
        except Exception as e:
            print(e)
            raise e
        return self.data

    def get_recent_times(self):
        return { local_datetime(game['createDate'], self.tzinfo)
                for game in self.json_data['gameStatistics'] }

    def load(self):
        return { r['date']
                for r in self.games.find({ "summoner": self.summoner_name }) }

    def dump(self):
        for time in sorted(self.data):
            game_id = self.games.update(
                    {
                        "summoner": self.summoner_name,
                        "date": time },
                    {
                        "summoner": self.summoner_name,
                        "date": time
                    },
                    upsert=True)
            print(game_id)

    def clean_db(self):
        self.games.remove({ "summoner": self.summoner_name })

def main():
    summoners = [
                    '你根本在發廢文',
                    'Salas',
                    'Aragorn',
                    '嵐辰星月夜',
                    '性侵大使',
                    '人品爆發揪咪030',
                ]
    for name in summoners[:1]:
        print(name)
        summoner = Summoner(name)
        games = summoner.get_recent_games()
        for result in summoner.games.find({ "summoner": name }):
            print(result)

if __name__ == '__main__':
    main()
