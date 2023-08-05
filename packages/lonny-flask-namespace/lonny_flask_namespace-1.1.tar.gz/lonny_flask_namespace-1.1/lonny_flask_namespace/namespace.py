from flask import g

class Configuration:
    global_prefix = "_lonny_flask_ext"

class Namespace:
    _unique_id = 0

    def __init__(self, generator):
        self._id = self._unique_id
        self._generator = generator
        self._unique_id += 1

    def get(self):
        root = g.setdefault(Configuration.global_prefix, dict())
        return root.setdefault(self._id, self._generator())