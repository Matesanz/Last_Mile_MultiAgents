from mesa import Agent
import numpy as np
from random import sample
from utils.pack import Pack
from agents.rider import Rider


class Base(Agent):

        def __init__(self, unique_id, model):
                super().__init__(unique_id, model)
                self.destinies = self.model.business_locations

        def step(self):
                self.give_packs_to_riders_at_base()
                return

        def create_pack(self):

                dest = sample(self.destinies, 1)[0]
                p = Pack(dest)

                return p

        def give_packs_to_riders_at_base(self):
                this_cell = self.model.grid.get_cell_list_contents([self.pos])
                riders = [obj for obj in this_cell if isinstance(obj, Rider)]

                for rider in riders:
                        empty_places = rider.max_packs - len(rider.packs)
                        for i in range(empty_places):
                                pack = self.create_pack()
                                rider.pick_pack(pack)


class Business(Agent):

        def __init__(self, unique_id, model):
                super().__init__(unique_id, model)

                self.open_probability = 0.8
                self.open = True

        def step(self):
                [self.open_business() if np.random.random() <= self.open_probability else self.close_business()]

        def close_business(self):
                self.open = False

        def open_business(self):
                self.open = True