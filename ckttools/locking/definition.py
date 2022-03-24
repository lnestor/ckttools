import importlib

class Definition:
    def __init__(self, definition):
        self.name = definition["name"]
        self.key = definition["key"]
        self.module_name = definition["module"]
        self.module = importlib.import_module(self.module_name)

        self._check_module()

    def get_args(self, config, common_args):
        return self.module.get_args(config, common_args)

    def run(self, moddef, args):
        return self.module.run(moddef, args)

    def _check_module(self):
        has_args = hasattr(self.module, "get_args")
        has_run = hasattr(self.module, "run")

        if not has_args and not has_run:
            print("ERROR: module %s does not implement get_args or run" % self.module_name)
            exit(-1)
        elif not has_args:
            print("ERROR: module %s does not implement get_args" % self.module_name)
            exit(-1)
        elif not has_run:
            print("ERROR: module %s does not implement run" % self.module_name)
            exit(-1)
