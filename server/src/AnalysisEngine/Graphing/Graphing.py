import logging
import abc
import networkx as nx
from AnalysisEngine.Analysis import Analysis
from AnalysisEngine.Graphing.Gephi.GephiRPC import GephiRpcClient
from AnalysisEngine.Graphing.Utils.GraphUtils import GraphUtils, GraphColor
import datetime
import json


class Graphing(Analysis):
    __metaclass__ = abc.ABCMeta
    _logger = logging.getLogger(__name__)
    __arguments = [dict(name="Limit", prettyName="Tweet limit", type="integer",
                        default=0),
                   dict(name="layoutIterations", prettyName="Layout Iterations", type="integer",
                        default=-1),
                   dict(name="LAYOUT_ALGO", prettyName="Layout Algorithm", type="enum", options=["FA2MS", "OPENORD"],
                        default="FA2MS"),
                   dict(name="LinLogMode", prettyName="FAMS2 Lin Log Mode", type="boolean",
                        default=False),
                   dict(name="PreventOverlap", prettyName="FAMS2 Prevent Overlap", type="boolean",
                        default=False),
                   dict(name="gravity_strength", prettyName="Gravity Strength", type="integer",
                        default=1.0),
                   dict(name="GRAVITY_X_SCALING", prettyName="Gravity X Scaling", type="integer",
                        default=1.0),
                   dict(name="GRAVITY_Y_SCALING", prettyName="Gravity Y Scaling", type="integer",
                        default=1.0),
                   dict(name="SCALING", prettyName="Scaling", type="integer",
                        default=2.0),

                   ]

    def __init__(self, analytics_meta):
        super(Graphing, self).__init__(analytics_meta)

    @abc.abstractmethod
    def process(self):
        pass

    @abc.abstractmethod
    def get_color(cls):
        return

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(Graphing, cls).get_args()

    @classmethod
    def get_classification(cls):
        return "Graph"

    def get_prefered_result(self):
        return "url_graph"

    def get_prefered_gdo_app(self):
        return "Graph"

    @classmethod
    def get_type(cls):
        pass

    def export_to_gridfs(self, G, name):
        with self.dbm.gridfs.new_file(filename=name, content_type="text/xml") as f:
            nx.write_graphml(G, f)

    def layout(self, G, extra_params=None):

        self.analytics_meta.graph_id = "GRAPH_" + self.analytics_meta.db_ref + ".graphml"
        self.analytics_meta.save()

        n_iterations = self.args["layoutIterations"]
        if n_iterations <= 0:
            self._logger.info("Not laying out as number of iterations <=0")
            self.analytics_meta.description += " (NOT layed out)"
            return G

        self.export_to_gridfs(G, self.analytics_meta.graph_id)
        self._logger.info("Exported graph ready for layout %s", self.analytics_meta.graph_id)

        self.analytics_meta.status = "EXPORTED RAW"
        self.analytics_meta.save()

        GraphUtils.fix_graphml_format_better(self.analytics_meta.graph_id, self.dbm.gridfs)
        self._logger.info("Reformatted graph ready for layout %s", self.analytics_meta.graph_id)
        self.analytics_meta.status = "REFORMAT COMPLETE"
        self.analytics_meta.save()

        params = {"LAYOUT_ITERATIONS": n_iterations,
                  "LAYOUT_ALGO": self.args["LAYOUT_ALGO"],
                  "PREVENT_OVERLAP": self.args["PreventOverlap"],
                  "LIN_LOG_MODE":self.args["LinLogMode"],
                  "GRAVITY": float(self.args["gravity_strength"]),
                  "GRAVITY_X_SCALING":float(self.args["GRAVITY_X_SCALING"]),
                  "GRAVITY_Y_SCALING":float(self.args["GRAVITY_Y_SCALING"]),
                  "LAYOUT_SCALE":float(self.args["SCALING"])}

        self._logger.info("Using Gephi Parameters %s", params)

        if extra_params is not None:
            for i in extra_params.keys():
                params[i] = extra_params[i]

        client = GephiRpcClient()

        result = json.loads(client.call(json.dumps({"GephiParameters": params,
                                                    "fileName": self.analytics_meta.graph_id})))
        self._logger.info("Result: %s", result)

        self._logger.info("Build graph %s", self.analytics_meta.id)
        self.analytics_meta.status = "LAYOUT COMPLETE"
        self.analytics_meta.description += " (layed out)"
        self.analytics_meta.save()

        with self.dbm.gridfs.get_last_version(self.analytics_meta.graph_id) as f:
            return nx.read_graphml(f)

    def finalise_graph(self, G, color = None):

        if self.analytics_meta.graph_id is None:
            self.analytics_meta.graph_id = "GRAPH_" + self.analytics_meta.db_ref + ".graphml"
            self.analytics_meta.save()
            self._logger.info("Found graph collection which hasn't had a name registered to it")

        if color is None:
            color = self.get_color()
        GraphColor.color_graph(G, color)

        self._logger.info("Colored graph %s", self.analytics_meta.id)
        self.analytics_meta.status = "COLORED"
        self.analytics_meta.save()

        self.export_to_gridfs(G, self.analytics_meta.graph_id)

        self._logger.info("Saved analytics %s", self.analytics_meta.graph_id)
        self.analytics_meta.status = "EXPORTED"
        self.analytics_meta.save()

        GraphUtils.fix_graphml_format_better(self.analytics_meta.graph_id, self.dbm.gridfs)

        self._logger.info("Saved GDO fomatted graph %s", self.analytics_meta.graph_id)
        self.analytics_meta.status = "SAVED"
        self.analytics_meta.end_time = datetime.datetime.now()
        self.analytics_meta.save()
