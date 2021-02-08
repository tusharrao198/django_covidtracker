from django.apps import AppConfig


class CovidtrackerConfig(AppConfig):
    name = "covidtracker"


# import os
# import psycopg2
# import json
# import ssl
# from pathlib import Path
# import urllib.request, urllib.error

# # from datetime import datetime

# # ignoring ssl error
# ctx = ssl.create_default_context()
# ctx.check_hostname = False
# ctx.verify_mode = ssl.CERT_NONE

# url_ = "https://api.rootnet.in/covid19-in/stats/latest"
# url2 = "https://api.rootnet.in/covid19-in/stats/history"


# # function for opening url
# def open_url(url_):
#     try:
#         fh = urllib.request.urlopen(url_, context=ctx)
#         # .read() reads whole as a string
#         data = fh.read().decode()
#         js = json.loads(data)
#         return js

#     except:
#         open_url(url_)


# def get_cerdentials():
#     BASE_DIR = Path(__file__).resolve().parent.parent
#     path_ = os.path.join(BASE_DIR)
#     info_ = open(path_ + "/.env").read()
#     line = info_.split("\n")
#     dict_ = {}
#     for el in line:
#         k, v = el.split("=")
#         dict_[k] = v
#     return dict_


# dict_ = get_cerdentials()

# conn = psycopg2.connect(
#     dbname=dict_["DB_NAME"],
#     user=dict_["DB_USER"],
#     password=dict_["DB_PASSWORD"],
#     host=dict_["DB_HOST"],
# )

# # create a cursor
# cur = conn.cursor()

# # execute a statement
# cur.execute("DROP TABLE IF EXISTS states")
# cur.execute(
#     """CREATE TABLE IF NOT EXISTS states
# (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
# name TEXT UNIQUE, confirmed INTEGER, deaths INTEGER,
# recovered INTEGER  )
# """
# )


# # Connecting to url
# js = open(url_)


# # Connecting to url of datewise cases
# # cases increment
# Totalcases = js["data"]["summary"]["total"]

# js2 = open_url(url2)

# # cases incement of last two days in  INDIA
# dict_inc = {}
# for i in range(len(js2["data"])):
#     # info_datewise = i
#     if i >= (len(js2["data"]) - 2):
#         cases_state = [
#             js2["data"][i]["summary"]["total"],
#             js2["data"][i]["summary"]["deaths"],
#             js2["data"][i]["summary"]["discharged"],
#         ]
#         dict_inc[js2["data"][i]["day"]] = cases_state
# # finding increase in cases per day
# len_dict = len(list(dict_inc))
# day_before = list(dict_inc)[0]
# last = list(dict_inc)[1]
# # print(day_before)
# # print(last)
# inc = dict_inc[last][0] - dict_inc[day_before][0]


# for i in js["data"]["regional"]:
#     state_name = i["loc"]
#     confirmed = i["totalConfirmed"]
#     deaths = i["deaths"]
#     recovered = i["discharged"]
#     cur.execute(
#         "INSERT OR REPLACE INTO states(name, confirmed, deaths, recovered) VALUES(?, ?, ?, ?)",
#         (state_name, confirmed, deaths, recovered),
#     )
#     # cur.execute("UPDATE states SET ")


# conn.commit()
# cur.execute("SELECT * FROM states ORDER BY confirmed DESC ")
# row = cur.fetchall()
# # display the PostgreSQL database server version

# for r in row:
#     r = r
# print(r)

# # close the communication with the PostgreSQL
# # cur.close()
# # except (Exception, psycopg2.DatabaseError) as error:
# #     print(error)


# if __name__ == "__main__":
#     connect()