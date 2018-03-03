import sqlite3

class bretpiDb():
	def __init__(self):
		self.sql_file = 'bret_pi_db.sqlite'
		#self.sql_file = '/Users/mgdunn/bret/db/bret_db.sqlite'
		self.connection = None

	def openConnection(self):
		if self.connection is None:
			self.connection = sqlite3.connect(self.sql_file, detect_types=sqlite3.PARSE_DECLTYPES)
		return self.connection

	def beginTransaction(self):
		self.results = None
		self.cursor = self.openConnection().cursor();

	def fetchall(self):
		self.cursor.fetchall()

	def commitTranscation(self):
		if self.connection is not None:
			self.connection.commit()
			self.results = self.cursor.fetchall()
			self.connection.close()
		self.cursor = None
		self.connection = None

	def rollbackTransaction(self):
		if self.cursor is not None:
			self.cursor.rollback()
		self.results = None
		self.cursor = None

	def addTime(self, datetime):
		self.beginTransaction()
		self.cursor.execute('SELECT max(`id`) from `checkins`;')
		#self.cursor.execute('SELECT * from `checkins`;')
		results = self.cursor.fetchall()
		if results is None or len(results) == 0 or results[0][0] == None:
			nextId = 0
		else:
			nextId = results[0][0] + 1
		self.cursor.execute('insert into `checkins` values(?, ?, ?)', (nextId, datetime, 0))
		self.commitTranscation()

	def trySend(self, sendFunc):
		self.beginTransaction()
		self.cursor.execute('SELECT `id`,`check_in_time` from `checkins` WHERE `delivered` = 0;')
		results = self.cursor.fetchall()
		if results is None or len(results) == 0 or results[0][0] == None:
			self.commitTranscation();
			return
		successes = []
		failures = []
		for row in results:
			try:
				if sendFunc(row[1]):
					successes.append(row[0])
			except:
				failures.append(row[0])
		print successes
		print failures
                for checkinId in successes:
			self.cursor.execute('UPDATE `checkins` SET `delivered` = 1 WHERE `id` = ?', (checkinId,))
		self.commitTranscation();
		return successes

	def getAllCheckins(self):
		self.beginTransaction()
		self.cursor.execute('SELECT `check_in_time`, `delivered` from `checkins`;')
		self.commitTranscation();
		return self.results

