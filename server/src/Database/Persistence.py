from pymongo import MongoClient
from pymongo.errors import ConfigurationError
import gridfs
import logging


class DatabaseManager(object):
    logger = logging.getLogger(__name__)

    def __init__(self, data_db_credentials, management_db_credentials):
        self.logger.info("Mongo: datadb %s, management db %s", data_db_credentials, management_db_credentials)

        self.data_db_client = MongoClient(data_db_credentials["host"],
                                          data_db_credentials["port"],
                                          connect=False)
        self.managementDB_client = MongoClient(management_db_credentials["host"],
                                               management_db_credentials["port"],
                                               connect=False)

        self.data_db = self.data_db_client.get_database("DATA")
        self.data_db.authenticate(data_db_credentials["username"], data_db_credentials["password"], source="admin")
        try:
            self.data_db.command("ping")
        except ConfigurationError:
            self.logger.critical("Cannot connect to " + data_db_credentials["host"])

        self.fdb = self.data_db_client.get_database("FILE_DATA")
        self.fdb.authenticate(management_db_credentials["username"],
                              management_db_credentials["password"],
                              source="admin")
        try:
            self.fdb.command("ping")
        except ConfigurationError:
            self.logger.critical("Cannot connect to " + management_db_credentials["host"])

        self.gridfs = gridfs.GridFS(self.fdb)

    def deleteGridFSFile(self, file_name):

        try:
            f = self.gridfs.get_last_version(file_name)
            self.gridfs.delete(f._id)
        except gridfs.NoFile:
            self.logger.warning("No file associated with analytics %s", file_name)