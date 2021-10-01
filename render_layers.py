class render_layers:
    """ A python singleton """

    class __impl:
        """ Implementation of the singleton interface """

        def __init__(self) -> None:
            self.layers = []
            
        def add(self, obj):
            self.layers.append(obj)

        def remove(self, obj):
            if obj in self.layers:
                self.layers.remove(obj)

        def output(self):
            for item in self.layers:
                print(item.name)

    # storage for the instance reference
    __instance = None

    def __init__(self):
        """ Create singleton instance """
        # Check whether we already have an instance
        if render_layers.__instance is None:
            # Create and remember instance
            render_layers.__instance = render_layers.__impl()

        # Store instance reference as the only member in the handle
        self.__dict__['_Singleton__instance'] = render_layers.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)