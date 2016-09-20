from pymongo import MongoClient
from pymongo.errors import ConfigurationError
import gridfs
import logging


class DatabaseManager(object):
    logger = logging.getLogger(__name__)

    def __init__(self, raw_data_db, results_db):
        self.logger.info("Mongo: datadb %s, management db %s", raw_data_db, results_db)

        self.data_db_client = MongoClient(raw_data_db["host"],
                                          raw_data_db["port"],
                                          connect=False)
        self.managementDB_client = MongoClient(results_db["host"],
                                               results_db["port"],
                                               connect=False)

        self.data_db = self.data_db_client.get_database("DATA")
        self.data_db.authenticate(raw_data_db["username"], raw_data_db["password"], source=raw_data_db["auth_db"])
        try:
            self.data_db.command("ping")
        except ConfigurationError:
            self.logger.critical("Cannot connect to " + raw_data_db["host"])

        self.fdb = self.managementDB_client.get_database(results_db["name"])
        self.fdb.authenticate(results_db["username"],
                              results_db["password"],
                              source=results_db["auth_db"])
        try:
            self.fdb.command("ping")
        except ConfigurationError:
            self.logger.critical("Cannot connect to " + results_db["host"])

        self.gridfs = gridfs.GridFS(self.fdb)

    def deleteGridFSFile(self, file_name):

        try:
            f = self.gridfs.get_last_version(file_name)
            self.gridfs.delete(f._id)
        except gridfs.NoFile:
            self.logger.warning("No file associated with analytics %s", file_name)