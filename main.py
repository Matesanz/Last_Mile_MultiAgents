#!/usr/bin/env python
from model.lastMileModel import LastMileModel
from utils.portrayal import agent_portrayal
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid

import nest_asyncio

if __name__ == "__main__":

        height = 10
        width = 10
        moto_number = 10
        van_number = 5
        business_number = 7

        nest_asyncio.apply()

        grid = CanvasGrid(agent_portrayal, height, width, 500, 500)

        server = ModularServer(
                LastMileModel,
                [grid],
                "Last Mile Model",
                {"N_moto": moto_number,
                 "N_van": van_number,
                 "N_business": business_number,
                 "width": width,
                 "height": height}
        )

        server.port = 8517  # The default

        server.launch()
