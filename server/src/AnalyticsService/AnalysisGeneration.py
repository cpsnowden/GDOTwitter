import logging
from api.Objects.MetaData import DatasetMeta
from Database.Persistence import DatabaseManager
import yaml

with open("config.yml", 'r') as config_file:
    cfg = yaml.load(config_file)
mongo_settings = cfg["mongo"]

class   AnalysisGeneration(object):
    _logger = logging.getLogger(__name__)

    @classmethod
    def get(cls, analytics_meta):
        graph_type = analytics_meta.type

        func = cls.get_options_dict().get(graph_type,
                                          lambda x: cls._logger.error("Unknown type specified %s", analytics_meta))

        cls._logger.info("Attempting construction of type %s", graph_type)
        gridfs, db_col, args, schema_id = cls.setup(analytics_meta)
        return func(analytics_meta, gridfs, db_col, args, schema_id)

    @classmethod
    def get_option_details(cls):

        return map(lambda option:{"type":option.get_type(), "args":option.get_args()}, cls.get_options())

    @classmethod
    def get_details(cls):
        return {"classification": cls.get_classification(),
                "options": cls.get_option_details()}

    @classmethod
    def get_options_dict(cls):
        return dict([(o.get_type(), o.get) for o in cls.get_options()])

    @classmethod
    def get_options(cls):
        return []

    @classmethod
    def get_classification(cls):
        return "Unspecified"

    @classmethod
    def setup(cls, analytics_meta):
        dataset_meta = DatasetMeta.objects.get(id=analytics_meta.dataset_id)
        dbm = DatabaseManager(mongo_settings["username"], mongo_settings["password"], mongo_settings["host"], mongo_settings["port"])
        db_col = dbm.data_db.get_collection(dataset_meta.db_col)

        args = analytics_meta.specialised_args

        cls._logger.info("Found arguments %s", args)

        return dbm.gridfs, db_col, args, dataset_meta.schema