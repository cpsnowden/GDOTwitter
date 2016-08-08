import abc
import logging
from datetime import timedelta

import numpy as np
from dateutil import parser

from AnalysisEngine.Graphing.Graphing import Graphing


class TrendGraph(Graphing):
    __metaclass__ = abc.ABCMeta
    _logger = logging.getLogger(__name__)

    __arguments = [dict(name="timeLabelInterval", prettyName="Time between time indicator labels (hrs)", type="integer",
                        default=1.0),
                   dict(name="timeInterval", prettyName="Time interval to classify source of gravity (s)",
                        type="integer", default=1.0)]

    def __init__(self, analytics_meta):
        super(TrendGraph, self).__init__(analytics_meta)

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(TrendGraph, cls).get_args()

    @classmethod
    def get_time_step(cls, date, start, interval):
        return int(divmod((date - start).total_seconds(), interval)[0])

    # @classmethod
    # def get_classification(cls):
    #     return super(TrendGraph, cls).get_classification()

    @classmethod
    def link_node_to_history(cls, G, history, node_id, user_id):
        past_user_node_id = cls.get_last_node(user_id, history)
        if past_user_node_id is not None:
            G.add_edge(past_user_node_id, node_id, type="user")
        history[user_id] = node_id

    @classmethod
    def get_last_node(cls, common_id, history):
        if common_id in history:
            return history[common_id]
        else:
            return None

    def add_time_indicator_nodes(self, G, start_date):

        if self.args["timeLabelInterval"] > 0:
            max_gravity_x = 0
            max_gravity_y = 0
            min_gravity_x = 0
            min_gravity_y = 0

            for nid in G.nodes():
                node = G.node[nid]
                if node["gravity_x"] > max_gravity_x:
                    max_gravity_x = node["gravity_x"]
                elif node["gravity_x"] < min_gravity_x:
                    min_gravity_x = node["gravity_x"]
                if node["gravity_y"] > max_gravity_y:
                    max_gravity_y = node["gravity_y"]
                elif node["gravity_y"] < min_gravity_y:
                    min_gravity_y = node["gravity_y"]

            self._logger.info("Max_x: %d, Min_x: %d, Max_y: %d, Min_y: %d, Step: %d", max_gravity_x, min_gravity_x,
                              max_gravity_y,
                              min_gravity_y,
                              float(self.args["timeLabelInterval"]) / self.args["timeInterval"])

            for i in np.arange(min_gravity_x, max_gravity_x,
                               float(self.args["timeLabelInterval"]) / self.args["timeInterval"]):
                G.add_node("TimeInd_T:" + str(start_date + timedelta(seconds=i)),
                           type="TimeIndicator",
                           node_type="time",
                           time=str(start_date + timedelta(seconds=i)),
                           x=float(i),
                           y=float(max_gravity_y + 10),
                           gravity_x=float(i),
                           gravity_x_strength=float(100),
                           gravity_y=float(max_gravity_y + 10),
                           gravity_y_strength=float(100),
                           size = float(10.0))

                G.add_node("TimeInd_B:" + str(start_date + timedelta(seconds=i)),
                           type="TimeIndicator",
                           node_type="time",
                           time=str(start_date + timedelta(seconds=i)),
                           x=float(i),
                           y=float(max_gravity_y + 10),
                           gravity_x=float(i),
                           gravity_x_strength=float(100),
                           gravity_y=float(min_gravity_y - 10),
                           gravity_y_strength=float(100),
                           size = float(10.0))

        return G
