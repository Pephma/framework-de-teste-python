class TestCase:
    def __init__(self, test_method_name):
        self.test_method_name = test_method_name

    def set_up(self):
        pass

    def tear_down(self):
        pass

    def run(self):
        self.set_up()
        test_method = getattr(self, self.test_method_name)
        test_method()
        self.tear_down()