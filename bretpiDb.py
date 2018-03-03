import os
import sys
import sqlite3
import json

confData = json.load(open('button.conf'))
sql_file = confData["sql_file"]

def transaction(func):
    def new_func(*args, **kwargs):
        connection = sqlite3.connect(sql_file, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = connection.cursor()
        try:
            retval = func(cursor, *args, **kwargs)
            connection.commit()
        except:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()
        return retval
    new_func.__name__ = func.__name__
    new_func.__doc__ = func.__doc__
    return new_func

@transaction
def addTime(cursor, datetime):
    cursor.execute('SELECT max(`id`) from `checkins`;')
    results = cursor.fetchall()
    if results is None or len(results) == 0 or results[0][0] == None:
        nextId = 0
    else:
        nextId = results[0][0] + 1
    cursor.execute('insert into `checkins` values(?, ?, ?)', (nextId, datetime, 0))

@transaction
def trySend(cursor, sendFunc):
    cursor.execute('SELECT `id`,`check_in_time` from `checkins` WHERE `delivered` = 0;')
    results = cursor.fetchall()
    if results is None or len(results) == 0 or results[0][0] == None:
        return
    successes = []
    failures = []
    for row in results:
        try:
            if sendFunc(row[1]):
                successes.append(row[0])
        except:
            failures.append(row[0])
    for checkinId in successes:
        cursor.execute('UPDATE `checkins` SET `delivered` = 1 WHERE `id` = ?', (checkinId,))
    return successes
