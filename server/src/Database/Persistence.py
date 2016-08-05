from pymongo import MongoClient
import gridfs
import logging


class DatabaseManager(object):
    logger = logging.getLogger(__name__)

    def __init__(self, uname, pwd, host, port):
        print uname, host, pwd, port
        self.client = MongoClient(host, port,  connect=False)
        self.data_db = self.client.get_database("DATA")
        self.data_db.authenticate(uname, pwd, source="admin")
        self.fdb = self.client.get_database("FILE_DATA")
        self.fdb.authenticate(uname, pwd, source="admin")
        self.gridfs = gridfs.GridFS(self.fdb)

    def deleteGridFSFile(self, fName):

        try:
            f = self.gridfs.get_last_version(fName)
            self.gridfs.delete(f._id)
        except gridfs.NoFile:
            self.logger.warning("No file associated with analytics %s", fName)


class StatusDAO(object):
    def __init__(self, collection):
        self.collection = collection

    def insert(self, status_json):
        self.collection.insert(status_json)

    def get_cursor(self, query, limit):
        return self.collection.find(query).limit(limit)
