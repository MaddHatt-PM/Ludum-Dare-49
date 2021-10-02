class EntityManager:
    """ A python singleton """

    class __impl:
        """ Implementation of the singleton interface """

        def __init__(self) -> None:
            self.entities = []
            self.ice_blocks = []
            self._deltaTime = 0.0
            
        def add(self, obj):
            self.entities.append(obj)

        def remove(self, obj):
            if obj in self.entities:
                self.entities.remove(obj)

        def add_ice(self, obj):
            self.ice_blocks.append(obj)

        def remove_ice(self, obj):
            if obj in self.ice_blocks:
                self.ice_blocks.remove(obj)

        def tick_all(self, deltaTime):
            self._deltaTime = deltaTime
            for entity in self.entities:
                entity.tick()

        def output(self):
            for item in self.entities:
                print(item.name)

        def clear(self):
            for item in self.entities:
                item.destroy()

        def deltatime(self):
            return self._deltaTime

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