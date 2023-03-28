# -*- coding: utf-8 -*-


class EntityBuilder(type):
    """
    build an entity at
    """

    def __init__(cls, name, bases, namespace, **kwargs):
        def constructor(self, parsed_json):
            self.json = parsed_json

            class PropWrapper:
                def __init__(self, prop):
                    self.value = prop

                def __call__(self):
                    return self.value

            for property_name in self.json.keys():
                setattr(self, property_name, PropWrapper(self.json[property_name]))

        cls.__init__ = constructor
