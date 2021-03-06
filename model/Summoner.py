import os
import re
import json
import requests
from pymongo import *

from util_method import *

try:
    client = MongoClient(os.environ['OPENSHIFT_MONGODB_DB_URL'])
except KeyError:
    client = MongoClient()


class Summoner:
    games = client.lol.games
    summoners = client.lol.summoners
    def __init__(self, name):
        self.summoner_name = name
        self.rank = 'OP'
        self.id = self.getid()
        self.data = self.load()
        self.new_data_raw = []
        self.tzinfo = TaipeiTimeZone()

    def getid(self):
        url = 'http://lol.moa.tw/summoner/show/' + self.summoner_name
        response = requests.get(url)
        id_obj = re.findall(r'MoaObj.lol.sumId = (.+);', response.text)
        self.rank = re.findall(r'前季階級</td><td class="strong h6">(.*)</td>', response.text)[0]
        return id_obj[0] if id_obj else None

    def get_recent_games(self):
        try:
            url = 'http://lol.moa.tw/Ajax/bs_recentgames/%d/%s' % (self.id, self.summoner_name)
            response = requests.get(url)
            result = re.findall(r'var recentgames=(.+);', response.text)
            self.json_data = json.loads(result[0])
            self.data |= self.get_recent_times()
            self.data = sorted(self.data)
            self.today_games = today_times(self.data)
            self.dump()
        except Exception as e:
            print(e)
            raise e
        response_data = {
            'id': self.id,
            'name': self.summoner_name,
            'rank': self.rank,
            'today_games': self.today_games,
            'data': self.data
        }
        return response_data

    def get_recent_times(self):
        return {local_datetime(game['createDate'], self.tzinfo)
                for game in self.json_data['gameStatistics']}

    def get_summoner_info(self):
        try:
            return Summoner.summoners.find_one({"summoner": self.summoner_name})['info']
        except:
            pass

    def set_summoner_info(self, *, summoner_info):
        rc = Summoner.summoners.update(
            {"summoner": self.summoner_name},
            {
                "summoner": self.summoner_name,
                "info": summoner_info
            }, upsert=True
        )
        print(rc)

    def load(self):
        return {r['date']
                for r in Summoner.games.find({"summoner": self.summoner_name})}

    def dump(self):
        for time in sorted(self.data):
            game_id = Summoner.games.update(
                {
                    "summoner": self.summoner_name,
                    "date": time
                }, {
                    "summoner": self.summoner_name,
                    "date": time
                },
                upsert=True
            )
            print(game_id)

    def clean_db(self):
        self.Summoner.remove({"summoner": self.summoner_name})


def main():
    summoners = [
        '你根本在發廢文',
        'Salas',
        'Aragorn',
        '嵐辰星月夜',
        '性侵大使',
        '人品爆發揪咪030',
    ]
    info_packs = {
        '你根本在發廢文': {
            'photo': 'https://fbcdn-sphotos-g-a.akamaihd.net/hphotos-ak-xfp1/v/t1.0-9/1476648_863664923655368_9153354075974269710_n.jpg?oh=c56befd749ab1335169d05cdf3d6529f&oe=55425FB2&__gda__=1428725801_9ed95c7f7deb1dbfca5e51b001c4a124',
            'saying': '天下皆雷，我獨凱瑞。',
            'nickname': '廢文哥',
            },
        '': {

        }
    }
    for name in summoners[:1]:
        print(name)
        summoner = Summoner(name)
        #games = summoner.get_recent_games()
        summoner.set_summoner_info(summoner_info=info_packs['你根本在發廢文'])
        sinfo = summoner.get_summoner_info()
        print(sinfo['saying'])

if __name__ == '__main__':
    main()
