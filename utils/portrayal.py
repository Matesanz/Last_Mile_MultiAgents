from agents.rider import Van, Moto
from agents.places import Business, Base


def agent_portrayal(agent):
        portrayal = {"Shape": "resources/moto.png",
                     "Layer": 3,
                     "scale": 0.9}

        if type(agent) is Van:

                if len(agent.packs) == 2:
                        portrayal["Shape"] = "resources/van_full.png"

                if len(agent.packs) == 1:
                        portrayal["Shape"] = "resources/van_half.png"

                if len(agent.packs) == 0:
                        portrayal["Shape"] = "resources/van.png"

        if type(agent) is Moto:

                if len(agent.packs) == 1:
                        portrayal["Shape"] = "resources/moto_full.png"

                if len(agent.packs) == 0:
                        portrayal["Shape"] = "resources/moto.png"

        if type(agent) is Base:
                portrayal["Shape"] = "resources/base.png"
                portrayal["Layer"] = 2

        if type(agent) is Business:
                portrayal["Shape"] = "resources/dest.png"
                portrayal["Layer"] = 2

        return portrayal
