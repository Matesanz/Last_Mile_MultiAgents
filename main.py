#!/usr/bin/env python
from model.lastMileModel import LastMileModel
from utils.portrayal import agent_portrayal
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid

import nest_asyncio


if __name__ == "__main__":

    nest_asyncio.apply()

    grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)

    server = ModularServer(LastMileModel,
                           [grid],
                           "Last Mile Model",
                           {"N_moto": 50, "N_van": 50, "N_business": 7, "width": 20, "height": 20})

    server.port = 8517  # The default

    server.launch()
