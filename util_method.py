from datetime import datetime, timezone, tzinfo, timedelta

class TaipeiTimeZone(tzinfo):
    offset = timedelta(hours=8)
    def utcoffset(self, dt):
        return self.offset
    def tzname(self, dt):
        return "台北標準時間"
    def dst(self, dt):
        return self.offset
    def fromutc(self, dt):
        dtoff = dt.utcoffset()
        dtdst = dt.dst()
        delta = dtoff - dtdst
        if delta:
            dt += delta
            dtdst = dt.dst()
        return dt + dtdst if dtdst else dt
    def __repr__(self):
        return "台北標準時間"

def local_datetime(utc_datetime, tz):
    local_date = datetime.strptime(utc_datetime, "%Y-%m-%dT%H:%M:%S.%fZ")
    return local_date + tz.offset

def tz_object(utc_date, tz):
    localdate = datetime.strptime(utc_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    localdate = localdate.replace(tzinfo=timezone.utc).astimezone(tz=tz)
    strlocaldate = localdate.strftime('%Y/%m/%d %H:%M:%S')
    return strlocaldate, localdate

def pprint(content):
    import pprint
    pprint.pprint(content)

if __name__ == '__main__':
    t = datetime(2014, 12, 21, 12, 56, 39, 204000)
    t = '2014-12-29T16:55:14.965Z'
    t = local_datetime(t, TaipeiTimeZone())
    print(t)
