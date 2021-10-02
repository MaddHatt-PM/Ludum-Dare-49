from enum import Enum, IntEnum

class LayerIDs(IntEnum):
    background = 0
    entities = 10
    foreground = 20
    ui = 30

class RenderLayers:
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
        if RenderLayers.__instance is None:
            # Create and remember instance
            RenderLayers.__instance = RenderLayers.__impl()

        # Store instance reference as the only member in the handle
        self.__dict__['_Singleton__instance'] = RenderLayers.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)