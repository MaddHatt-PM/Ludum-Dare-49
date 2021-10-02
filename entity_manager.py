class EntityManager:
    """ A python singleton """

    class __impl:
        """ Implementation of the singleton interface """

        def __init__(self) -> None:
            self.entities = []
            self.ice_blocks = []
            self.goals = []
            self.collidables = []
            self._deltaTime = 0.0
            
        def add(self, obj):
            self.entities.append(obj)

        def remove(self, obj):
            if obj in self.entities:
                self.entities.remove(obj)
            
            if obj in self.ice_blocks:
                self.ice_blocks.remove(obj)

            if obj in self.goals:
                self.goals.remove(obj)

            if obj in self.collidables:
                self.collidables.remove(obj)

        def add_ice(self, obj):
            self.ice_blocks.append(obj)

        def add_collidable(self, obj):
            self.collidables.append(obj)

        def add_goal(self, obj):
            self.goals.append(obj)

        def remove_goal(self, obj):
            self.goals

        def tick_all(self, deltaTime):
            self._deltaTime = deltaTime
            for entity in self.entities:
                if entity.enabled:
                    entity.tick()

        def output(self):
            for item in self.entities:
                print(item.name)

        def clear(self):
            for item in self.entities:
                item.destroy()

        def deltatime(self):
            return self._deltaTime

        def is_level_completed(self):
            if len(self.goals) == 0:
                return False

            for goal in self.goals:
                if goal.is_completed == False:
                    return False

            return True

    # storage for the instance reference
    __instance = None

    def __init__(self):
        """ Create singleton instance """
        # Check whether we already have an instance
        if EntityManager.__instance is None:
            # Create and remember instance
            EntityManager.__instance = EntityManager.__impl()

        # Store instance reference as the only member in the handle
        self.__dict__['_Singleton__instance'] = EntityManager.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)