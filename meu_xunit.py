class TestResult:
    def __init__(self):
        self.run_count = 0
        self.failures = []
        self.errors = []

    def test_started(self):
        self.run_count += 1

    def add_failure(self, test_method_name):
        self.failures.append(test_method_name)

    def add_error(self, test_method_name):
        self.errors.append(test_method_name)

    def summary(self):
        return f'{self.run_count} run, {len(self.failures)} failed, {len(self.errors)} error'

class TestCase:
    def __init__(self, test_method_name):
        self.test_method_name = test_method_name

    def set_up(self):
        pass

    def tear_down(self):
        pass

    def run(self, result):
        result.test_started()
        self.set_up()
        try:
            test_method = getattr(self, self.test_method_name)
            test_method()
        except AssertionError:
            result.add_failure(self.test_method_name)
        except Exception:
            result.add_error(self.test_method_name)
        self.tear_down()

class TestSuite:
    def __init__(self):
        self.tests = []

    def add_test(self, test):
        self.tests.append(test)

    def run(self, result):
        for test in self.tests:
            test.run(result)

class TestStub(TestCase):
    def test_success(self):
        assert True

    def test_failure(self):
        assert False

    def test_error(self):
        raise Exception("Erro proposital")

class TestSpy(TestCase):
    def __init__(self, name):
        super().__init__(name)
        self.log = ""

    def set_up(self):
        self.log += "set_up "

    def test_method(self):
        self.log += "test_method "

    def tear_down(self):
        self.log += "tear_down"

class TestCaseTest(TestCase):
    def set_up(self):
        self.result = TestResult()

    def test_result_success_run(self):
        stub = TestStub('test_success')
        stub.run(self.result)
        assert '1 run, 0 failed, 0 error' == self.result.summary()

    def test_result_failure_run(self):
        stub = TestStub('test_failure')
        stub.run(self.result)
        assert '1 run, 1 failed, 0 error' == self.result.summary()

    def test_result_error_run(self):
        stub = TestStub('test_error')
        stub.run(self.result)
        assert '1 run, 0 failed, 1 error' == self.result.summary()

    def test_result_multiple_run(self):
        TestStub('test_success').run(self.result)
        TestStub('test_failure').run(self.result)
        TestStub('test_error').run(self.result)
        assert '3 run, 1 failed, 1 error' == self.result.summary()

    def test_was_set_up(self):
        spy = TestSpy('test_method')
        spy.run(self.result)
        assert "set_up " in spy.log

    def test_was_run(self):
        spy = TestSpy('test_method')
        spy.run(self.result)
        assert "test_method " in spy.log



    def test_was_tear_down(self):
        spy = TestSpy('test_method')
        spy.run(self.result)
        assert "tear_down" in spy.log

    def test_template_method(self):
        spy = TestSpy('test_method')
        spy.run(self.result)
        assert "set_up test_method tear_down" == spy.log

class TestSuiteTest(TestCase):
    def test_suite_size(self):
        suite = TestSuite()
        suite.add_test(TestStub('test_success'))
        suite.add_test(TestStub('test_failure'))
        suite.add_test(TestStub('test_error'))
        assert len(suite.tests) == 3

    def test_suite_success_run(self):
        result = TestResult()
        suite = TestSuite()
        suite.add_test(TestStub('test_success'))
        suite.run(result)
        assert result.summary() == '1 run, 0 failed, 0 error'

    def test_suite_multiple_run(self):
        result = TestResult()
        suite = TestSuite()
        suite.add_test(TestStub('test_success'))
        suite.add_test(TestStub('test_failure'))
        suite.add_test(TestStub('test_error'))
        suite.run(result)
        assert result.summary() == '3 run, 1 failed, 1 error'

if __name__ == '__main__':
    result = TestResult()
    suite = TestSuite()
    suite.add_test(TestCaseTest('test_result_success_run'))
    suite.add_test(TestCaseTest('test_result_failure_run'))
    suite.add_test(TestCaseTest('test_result_error_run'))
    suite.add_test(TestCaseTest('test_result_multiple_run'))
    suite.add_test(TestCaseTest('test_was_set_up'))
    suite.add_test(TestCaseTest('test_was_run'))
    suite.add_test(TestCaseTest('test_was_tear_down'))
    suite.add_test(TestCaseTest('test_template_method'))
    suite.add_test(TestSuiteTest('test_suite_size'))
    suite.add_test(TestSuiteTest('test_suite_success_run'))
    suite.add_test(TestSuiteTest('test_suite_multiple_run'))
    suite.run(result)
    print(result.summary())