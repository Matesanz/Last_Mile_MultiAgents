from collections import defaultdict
from agents.rider import Moto, Van
from mesa.time import RandomActivation


class RandomActivationByType(RandomActivation):
    '''
    Un Scheduler que activa cada tipo de agente una vez en cada paso,
    de forma aleatoria.

    Espera que todos los agentes tengan un método step().
    '''

    def __init__(self, model):
        super().__init__(model)
        self.riders_by_type = defaultdict(dict)

    def add(self, agent):
        '''
        Add an Agent object to the schedule
        Args:
            agent: An Agent to be added to the schedule.
        '''

        self._agents[agent.unique_id] = agent
        agent_class = type(agent)
        self.riders_by_type[agent_class][agent.unique_id] = agent

    def remove(self, agent):
        '''
        Remove all instances of a given agent from the schedule.
        '''

        del self._agents[agent.unique_id]
        agent_class = type(agent)
        del self.riders_by_type[agent_class][agent.unique_id]


    def get_pack_count_by_type(self, type_class):
        '''
        Returns the current number of Packs delivered by a certain typo of Rider
        Args:
            type_class: An Agent Type get the delivered packs from.
        '''

        packs = [rider.total_packs for rider in self.riders_by_type[type_class].values()]
        return sum(packs)

    def get_total_pack_count(self):
        '''
        Returns the total number of Packs delivered by all the riders
        '''

        packs_moto = self.get_pack_count_by_type(Moto)
        packs_van = self.get_pack_count_by_type(Van)

        return packs_moto + packs_van