from pymongo import MongoClient
import gridfs
import logging


class DatabaseManager(object):
    logger = logging.getLogger(__name__)

    def __init__(self, user_name, pwd, host, port):
        self.logger.info("Mongo: host %s, port %d, username %s", host, port, user_name)
        self.client = MongoClient(host, port,  connect=False)
        self.data_db = self.client.get_database("DATA")
        self.data_db.authenticate(user_name, pwd, source="admin")
        self.fdb = self.client.get_database("FILE_DATA")
        self.fdb.authenticate(user_name, pwd, source="admin")
        self.gridfs = gridfs.GridFS(self.fdb)

    def deleteGridFSFile(self, file_name):

        try:
            f = self.gridfs.get_last_version(file_name)
            self.gridfs.delete(f._id)
        except gridfs.NoFile:
            self.logger.warning("No file associated with analytics %s", file_name)