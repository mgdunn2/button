import os
import sys
import sqlite3
import json
from db.db import transaction

confData = json.load(open('button.conf'))
sql_file = confData["sql_file"]

@transaction(sql_file)
def addTime(cursor, datetime):
    cursor.execute('SELECT max(`id`) from `checkins`;')
    results = cursor.fetchall()
    if results is None or len(results) == 0 or results[0][0] == None:
        nextId = 0
    else:
        nextId = results[0][0] + 1
    cursor.execute('insert into `checkins` values(?, ?, ?)', (nextId, datetime, 0))

@transaction(sql_file)
def trySend(cursor, sendFunc):
    cursor.execute('SELECT `id`,`check_in_time` from `checkins` WHERE `delivered` = 0;')
    results = cursor.fetchall()
    if results is None or len(results) == 0 or results[0][0] == None:
        return
    successes = []
    for row in results:
        try:
            if sendFunc(row[1]):
                successes.append(row[0])
        except:
            pass
    for checkinId in successes:
        cursor.execute('UPDATE `checkins` SET `delivered` = 1 WHERE `id` = ?', (checkinId,))
    return successes
