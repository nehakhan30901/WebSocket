import unittest
import KVStore_API

class Test(unittest.TestCase):

	def test_mongodb_connection(self):
		#db=KVStore_API.DbAccess_Pymongo('appcfg.yaml')
		pass
		

	def test_get(self):
		db=KVStore_API.DbAccess_Pymongo('appcfg.yaml')
		self.assertEqual(db.get('keyone'),'valueone')

	def test_set(self):
		db=KVStore_API.DbAccess_Pymongo('appcfg.yaml')
		self.assertEqual(db.set('keyfour','valuefour'),'inserted field keyfour')

if __name__ == '__main__':
	unittest.main()

