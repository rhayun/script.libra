import time

try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database

from libra import common


def get(hashed):
    try:
        t = int(time.time())
        common.makeFile(common.dataPath)
        dbcon = database.connect(common.libraDbFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS cache (""hash TEXT, ""data TEXT, ""expire TEXT, ""created TEXT, ""UNIQUE(hash)"");")
        dbcur.execute("SELECT * FROM cache WHERE hash = '%s'" % (hashed))
        match = dbcur.fetchone()

        if int(match[2]) < t:
            dbcur.execute("DELETE FROM cache WHERE hash = '%s'" % (hashed))
            dbcon.commit()
            return None

        return match

    except:
        return None


def set(hashed, data, hours=24):
    try:
        r = repr(data)
        t = int(time.time())
        e = int(t+(60*60*int(hours)))
        common.makeFile(common.dataPath)
        dbcon = database.connect(common.libraDbFile)
        dbcur = dbcon.cursor()
        dbcur.execute("CREATE TABLE IF NOT EXISTS cache (""hash TEXT, ""data TEXT, ""expire TEXT, ""created TEXT, ""UNIQUE(hash)"");")        
        dbcur.execute("DELETE FROM cache WHERE hash = '%s'" % (hashed))
        dbcur.execute("INSERT INTO cache Values (?, ?, ?, ?)", (hashed, r, e, t))
        dbcon.commit()

        return True

    except:
        return None

