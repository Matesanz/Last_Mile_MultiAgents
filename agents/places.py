from mesa import Agent
import numpy as np
from random import sample
from utils.pack import Pack
from agents.rider import Rider


class Base(Agent):
        '''
        HeadQuarter Agent Class: Place where riders pick up Packs
        in order to perform a delivery
        '''

        def __init__(self, unique_id, model):
                super().__init__(unique_id, model)

                # Initialize list with business coordinates in Grid
                self.destinies = self.model.business_locations
                # Every step matches a minute within a day
                self.timing = 1440

        def step(self):

                '''
                On every step gives Packs Objetc to Riders at
                Base Location, adds a minute to minute counter
                and tells Riders wheter to work or stay at Base.
                '''

                self.give_packs_to_riders_at_base()
                self.update_timing()
                self.tell_timing_to_riders()
                return

        def create_pack(self):
                '''

                :return: a Pack object to be delivered
                '''

                # Set random destiny into pack
                dest = sample(self.destinies, 1)[0]
                p = Pack(dest)

                return p

        def get_riders_at_base(self):
                '''

                :return: gets all riders at Base Location
                '''
                this_cell = self.model.grid.get_cell_list_contents([self.pos])
                riders = [obj for obj in this_cell if isinstance(obj, Rider)]
                return riders

        def give_packs_to_riders_at_base(self):
                '''
                Add Packs to Riders Class in order to be delivered
                '''

                # Get list of riders at base
                riders = self.get_riders_at_base()

                for rider in riders:
                        empty_places = rider.max_packs - len(rider.packs)
                        for i in range(empty_places):
                                pack = self.create_pack()
                                rider.pick_pack(pack)

        def update_timing(self):
                '''
                Updates Minute Counter
                '''

                # Remove one minute form day timing
                self.timing -= 1
                if self.timing == 0:
                        # If timing goes to 0 reset to 3600 min
                        print("New Day")
                        self.reset_riders_dropped_packs_counter()
                        self.reset_timing()

        def reset_timing(self):
                '''
                Resets minute Counter
                '''
                self.timing = 1440

        def is_working_time(self):

                '''
                Returns whether is working time or not
                '''


                # 1440 == 10 am
                # 1200 == 2 pm
                # 1020 == 5 pm
                # 810 == 8:30 pm

                if 1440 > self.timing > 1200 or 1020 > self.timing > 810:
                        return True
                else:
                        return False

        def tell_timing_to_riders(self):
                '''
                Tell Riders at Base Location whether to work or not
                '''

                # Tell riders at base whether to continue or not
                riders = self.get_riders_at_base()
                working_status = self.is_working_time()
                [rider.change_rider_working_status(working_status)for rider in riders]

        def reset_riders_dropped_packs_counter(self):
                '''
                Resets Riders at Base Location Dropped Pack Counter
                '''
                # Reset Riders Daily packs counter to 0
                riders = self.get_riders_at_base()
                [rider.reset_dropped_packs_counter()for rider in riders]






class Business(Agent):
        '''
        Business Object: Place where riders must go,
        in order to drop a Pack Object
        '''

        def __init__(self, unique_id, model):
                super().__init__(unique_id, model)

                self.open_probability = 0.8
                self.open = True

        def step(self):
                '''
                On every step there's a chance that business is closed
                '''

                # Business is open under certain probability
                [self.open_business() if np.random.random() <= self.open_probability else self.close_business()]

        def close_business(self):
                '''
                Sets open parameter to False
                '''
                # Close business
                self.open = False

        def open_business(self):
                '''
                Sets open parameter to True
                '''
                # Open Business
                self.open = True