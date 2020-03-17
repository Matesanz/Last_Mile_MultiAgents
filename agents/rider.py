from mesa import Agent
import numpy as np
import agents.places

class Rider(Agent):
        """ An agent that goes from A to B """

        def __init__(self, unique_id, model):
                super().__init__(unique_id, model)

                self.packs = []
                self.max_packs = 1
                self.patience = 3
                self.base_location = self.model.base_location
                self.active = False

        def step(self):

                # If rider is active: works
                if self.active:

                        # if rider arrives to base picks the pack
                        if not self.packs and not self.is_rider_in_base():
                                self.move(self.base_location)

                        # if rider arrives to destiny drop the pack
                        if self.packs:

                                if self.is_rider_in_destiny():
                                        # print("i dropped the pack")
                                        if self.is_business_open():
                                                self.drop_pack()
                                        else:
                                                print('Business is closed')
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
                return self.active

        def change_rider_working_status(self, status):
                self.active = status

        def is_business_open(self):
                this_cell = self.model.grid.iter_cell_list_contents([self.pos])
                business = [obj for obj in this_cell
                            if isinstance(obj, agents.places.Business)][0]
                return business.open

        def put_pack_to_bottom_of_list(self):
                last_pack = self.packs[-1]
                # remove last pack
                self.packs.pop()
                # insert last pack to bottom of list
                self.packs.insert(0, last_pack)

        def drop_pack(self):

                self.packs.pop()
                # print(self.packs)

        def pick_pack(self, pack):

                self.packs.append(pack)

        def set_destiny(self, destiny):
                self.destiny = destiny
                # print('my new destiny is ', self.destiny)

        def is_rider_in_destiny(self):
                return (self.pos == self.packs[-1].destination)

        def is_rider_in_base(self):
                return (self.pos == self.base_location)

        def is_rider_full(self):
                return (len(self.packs) == self.max_packs)


class Moto(Rider):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.max_packs = 1

class Van(Rider):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.max_packs = 2
