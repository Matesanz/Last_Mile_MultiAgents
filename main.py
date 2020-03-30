#!/usr/bin/env python
from model.lastMileModel import LastMileModel
from utils.portrayal import agent_portrayal
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule

import nest_asyncio

if __name__ == "__main__":

        height = 10
        width = 10
        moto_number = 10
        van_number = 5
        business_number = 7

        nest_asyncio.apply()

        grid = CanvasGrid(agent_portrayal, height, width, 500, 500)

        chart = ChartModule([{"Label": "Packs Moto", "Color": "#63c458"},
                             {"Label": "Packs Van", "Color": "#4d4dff"},
                             {"Label": "Total Packs", "Color": "#c46358"}
                             ],
                            data_collector_name='datacollector')

        server = ModularServer(
                LastMileModel,
                [grid, chart],
                "Last Mile Model",
                {"N_moto": moto_number,
                 "N_van": van_number,
                 "N_business": business_number,
                 "width": width,
                 "height": height}
        )

        server.port = 8517  # The default

        server.launch()
