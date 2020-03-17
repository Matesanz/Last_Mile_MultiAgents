from mesa import Agent
import numpy as np
from random import sample
from utils.pack import Pack
from agents.rider import Rider


class Base(Agent):

        def __init__(self, unique_id, model):
                super().__init__(unique_id, model)
                self.destinies = self.model.business_locations
                self.timing = 1440

        def step(self):
                self.give_packs_to_riders_at_base()
                self.update_timing()
                self.tell_timing_to_riders()
                return

        def create_pack(self):

                # Set random destiny into pack
                dest = sample(self.destinies, 1)[0]
                p = Pack(dest)

                return p

        def get_riders_at_base(self):
                this_cell = self.model.grid.get_cell_list_contents([self.pos])
                riders = [obj for obj in this_cell if isinstance(obj, Rider)]
                return riders

        def give_packs_to_riders_at_base(self):
                # Get list of riders at abse
                riders = self.get_riders_at_base()

                for rider in riders:
                        empty_places = rider.max_packs - len(rider.packs)
                        for i in range(empty_places):
                                pack = self.create_pack()
                                rider.pick_pack(pack)

        def update_timing(self):
                # Remove one minute form day timing
                self.timing -= 1
                if self.timing == 0:
                        # If timing goes to 0 reset to 3600 min
                        print("New Day")
                        self.reset_timing()

        def reset_timing(self):
                self.timing = 1440

        def is_working_time(self):
                # 1440 == 10 am
                # 1200 == 2 pm
                # 1020 == 5 pm
                # 810 == 8:30 pm

                if 1440 > self.timing > 1200 or 1020 > self.timing > 810:
                        return True
                else:
                        return False

        def tell_timing_to_riders(self):

                # Tell riders at base whether to continue or not
                riders = self.get_riders_at_base()
                working_status = self.is_working_time()
                [rider.change_rider_working_status(working_status)for rider in riders]






class Business(Agent):

        def __init__(self, unique_id, model):
                super().__init__(unique_id, model)

                self.open_probability = 0.8
                self.open = True

        def step(self):
                # Business is open under certain probability
                [self.open_business() if np.random.random() <= self.open_probability else self.close_business()]

        def close_business(self):
                # Close business
                self.open = False

        def open_business(self):
                # Open Business
                self.open = True