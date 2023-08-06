#!/usr/bin/env python

class TestWrapper():
    _instance = None

    def __init__(self, module, case_class, test_input):
        try:
            pkg = __import__(module, fromlist=[case_class])
            test_class = getattr(pkg, case_class)
            self._instance = test_class(test_input)
        except Exception as e:
            raise RuntimeError("\nFailed to import {} with class {} - {}".format(module, case_class, e))

    def setup(self):
        return self._instance.setup()

    def run(self):
        return self._instance.run()

    def cleanup(self):
        return self._instance.cleanup()
