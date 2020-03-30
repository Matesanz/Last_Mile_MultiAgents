from mesa import Agent
import numpy as np
import agents.places

class Rider(Agent):
        """
        An agent that goes from A to B to Drop a Pack
        """

        def __init__(self, unique_id, model):
                super().__init__(unique_id, model)

                self.packs = []
                self.max_packs = 1
                self.total_packs = 0
                self.patience = 3
                self.base_location = self.model.base_location
                self.active = False

        def step(self):
                """
                If Rider is in working time moves towards Business
                when he does have Packs or towards Base when he doesn't.
                If he is at Target drops the PAck if Business is open.
                If Closed waits until opens or until Patience turns into 0.
                """

                # If rider is active: works
                if self.active:

                        # if rider arrives to base picks the pack
                        if not self.packs and not self.is_rider_in_base():
                                self.move(self.base_location)

                        # if rider arrives to destiny drop the pack
                        if self.packs:

                                if self.is_rider_in_destiny():

                                        if self.is_business_open():
                                                # Drops the Pack
                                                self.drop_pack()
                                        else:
                                                # Business is Closed
                                                self.patience -= 1
                                                if self.patience == 0:
                                                        self.put_pack_to_bottom_of_list()
                                                        self.patience = 3
                                                else:
                                                        pass

                                else:
                                        # print("i have ", len(self.packs), " packs")
                                        self.move(self.packs[-1].destination)

                # If rider is not active do nothing
                else:
                        pass

        def move(self, destiny):
                '''

                :param  destiny: tuple(x,y): coordinates to move towards
                :return:
                '''

                # Calculates direction vector towards destiny
                direction = np.subtract(destiny, self.pos)
                # Get longest axis in direcion
                axis = np.argmax(abs(direction))

                #print(direction)
                # The longest direction element becomes 1 toward the destiny
                direction[axis] /= abs(direction[axis])
                # The shortest direction element becomes 0
                direction[axis - 1] = 0

                # Add normalized direction to actual position to calculate next position
                new_position = np.add(self.pos, direction)

                # Apply movement to agent
                new_position = tuple(new_position)
                self.model.grid.move_agent(self, new_position)

        def is_rider_able_to_work(self):
                '''
                Returns whether Rider is able or not to work
                '''
                return self.active

        def change_rider_working_status(self, status):
                '''
                changer whether Rider is able or not to work
                '''
                self.active = status

        def is_business_open(self):
                '''
                Checks if business at same location is open
                '''
                this_cell = self.model.grid.iter_cell_list_contents([self.pos])
                business = [obj for obj in this_cell
                            if isinstance(obj, agents.places.Business)][0]
                return business.open

        def put_pack_to_bottom_of_list(self):
                '''
                If Patience turns 0 puts Pack at the beginning of list
                '''

                last_pack = self.packs[-1]
                # remove last pack
                self.packs.pop()
                # insert last pack to bottom of list
                self.packs.insert(0, last_pack)

        def drop_pack(self):
                '''
                Drops the pack at destiny
                '''
                self.total_packs += 1
                self.packs.pop()

        def pick_pack(self, pack):
                '''
                Picks Pack at Base
                :param pack: Pack Object
                '''
                self.packs.append(pack)

        def is_rider_in_destiny(self):
                '''
                Returns True if Rider is at destiny
                '''
                return (self.pos == self.packs[-1].destination)

        def is_rider_in_base(self):
                '''
                Returns True if Rider is at Base
                '''
                return (self.pos == self.base_location)

        def is_rider_full(self):
                '''
                Returns True if Rider is full of Packs
                '''
                return (len(self.packs) == self.max_packs)

        def reset_dropped_packs_counter(self):
                '''
                Resets Rider dropped Packs to 0
                '''
                self.total_packs = 0

        def nb_dropped_packs(self):
                return self.total_packs


class Moto(Rider):
        '''
        Rider class with 1 Pack maximum
        '''

        def __init__(self, unique_id, model):
                super().__init__(unique_id, model)
                self.max_packs = 1

class Van(Rider):
        '''
        Rider class with 2 Packs maximum
        '''

        def __init__(self, unique_id, model):
                super().__init__(unique_id, model)
                self.max_packs = 2
