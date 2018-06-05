import testlink
import datetime
import os
import time
import json
from pprint import pprint
from unittest import (
    TestLoader,
    TextTestResult,
    TextTestRunner)
from tests.calculations_tests import TestLibrary

OK = 'ok'
FAIL = 'fail'
ERROR = 'error'
SKIP = 'skip'


class JsonTestResult(TextTestResult):

    def __init__(self, stream, descriptions, verbosity):
        super_class = super(JsonTestResult, self)
        super_class.__init__(stream, descriptions, verbosity)

        self.successes = []

    def addSuccess(self, test):
        super(JsonTestResult, self).addSuccess(test)
        self.successes.append(test)

    # Pobranie właściwości wyników testów.
    def json_append(self, test, result, out):
        suite = test.__class__.__name__
        if suite not in out:
            out[suite] = {OK: [], FAIL: [], ERROR: [], SKIP: []}
        if result is OK:
            unit_test = {
                test._testMethodName: {
                    'formatted_method_name': test.formatted_method_name,
                    'time_start': datetime.datetime.fromtimestamp
                    (test.time_start).strftime('%Y-%m-%d %H:%M:%S:%f'),
                    'time_end': datetime.datetime.fromtimestamp
                    (test.time_end).strftime('%Y-%m-%d %H:%M:%S:%f'),
                    'exec_time': test.exec_time,
                    'ts_status': "passed"
                }}
            out[suite][OK].append(unit_test)
        elif result is FAIL:
            unit_test = {
                test._testMethodName: {
                    'formatted_method_name': test.formatted_method_name,
                    'time_start': datetime.datetime.fromtimestamp
                    (test.time_start).strftime('%Y-%m-%d %H:%M:%S:%f'),
                    'time_end': "-",
                    'exec_time': "-",
                    'ts_status': "blocked"
                }}
            out[suite][FAIL].append(unit_test)
        elif result is ERROR:
            unit_test = {
                test._testMethodName: {
                    'formatted_method_name': test.formatted_method_name,
                    'time_start': datetime.datetime.fromtimestamp
                    (test.time_start).strftime('%Y-%m-%d %H:%M:%S:%f'),
                    'time_end': "-",
                    'exec_time': "-",
                    'ts_status': "failed"
                }}
            out[suite][ERROR].append(unit_test)
        elif result is SKIP:
            unit_test = {
                test._testMethodName: {
                    'formatted_method_name': test.formatted_method_name,
                    'time_start': datetime.datetime.fromtimestamp
                    (test.time_start).strftime('%Y-%m-%d %H:%M:%S:%f'),
                    'time_end': "-",
                    'exec_time': "-",
                    'ts_status': "skipped"
                }}
            out[suite][SKIP].append(unit_test)
        else:
            raise KeyError("No such result: {}".format(result))
        return out

    def jsonify(self):
        json_out = dict()
        for t in self.successes:
            json_out = self.json_append(t, OK, json_out)

        for t, _ in self.failures:
            json_out = self.json_append(t, FAIL, json_out)

        for t, _ in self.errors:
            json_out = self.json_append(t, ERROR, json_out)

        for t, _ in self.skipped:
            json_out = self.json_append(t, SKIP, json_out)

        return json_out


if __name__ == '__main__':
    with open(os.devnull, 'w') as null_stream:
        runner = TextTestRunner(stream=null_stream)
        runner.resultclass = JsonTestResult

        suite = TestLoader().loadTestsFromTestCase(TestLibrary)

        # Uruchomienie testów (pomiar czasu wykonania wszystkich testów).
        test_suite_time_start = time.time()
        result = runner.run(suite)
        test_suite_time_end = time.time()
        test_suite_exec_time = test_suite_time_end - test_suite_time_start

        unittests_json_result = result.jsonify()
        pprint(unittests_json_result)

        # Konfiguracja połączenia z TestLink.
        TESTLINK_SERVER_URL = "http://185.24.216.248:81/testlink/lib/api/xmlrpc/v1" \
                              "/xmlrpc.php"
        TESTLINK_API_KEY = "5eb00dff1f7220d65e99fdbb9c947f4c"

        tlh = testlink.TestLinkHelper(TESTLINK_SERVER_URL, TESTLINK_API_KEY)
        tls = testlink.TestlinkAPIClient(tlh._server_url, tlh._devkey, verbose=False)

        # ---------------------------------------------------------------------------
        print("Statystyki TestLink")
        print(
            "\t-Number of Projects      in TestLink: %s " % tls.countProjects())
        print(
            "\t-Number of Platforms  (in TestPlans): %s " % tls.countPlatforms())
        print("\t-Number of Builds                   : %s " % tls.countBuilds())
        print(
            "\t-Number of TestPlans                : %s " % tls.countTestPlans())
        print(
            "\t-Number of TestSuites               : %s " % tls.countTestSuites())
        print(
            "\t-Number of TestCases (in TestPlans) : %s " % tls.countTestCasesTP())
        # ---------------------------------------------------------------------------

        # Pobranie prefixu projektu testowego z TestLink.
        project_prefix = tls.getTestProjectByName("House Price Calculator")['prefix']

        # Pobranie id planu testów z TestLink.
        test_plan_id = tls.getTestPlanByName("House Price Calculator",
                                             "House Price Calculator"
                                             " Library Tests")[0]['id']


        # Stworzenie wiadomości do raportu.
        def create_note_message(json_obj, tc_result):
            note = "Formatted test name: " + str(
                list(json_obj.values())[0]['formatted_method_name']) \
                   + ",\n"
            note += "Test result: " \
                    + str(list(json_obj.values())[0]['ts_status']) + ",\n"
            note += "Start date: " \
                    + str(list(json_obj.values())[0]['time_start']) + ",\n"
            if tc_result != 'p':
                note += "End date: none (test was not completed successfully),\n"
                note += "Duration: none (test was not completed successfully).\n"
            else:
                note += "End date: " \
                        + str(list(json_obj.values())[0]['time_end']) + ",\n"
                note += "Duration: " \
                        + str(list(json_obj.values())[0]['exec_time']) + ".\n"

            return note


        # Metoda wysyłająca raport przetworzonego testu do TestLink wraz z plikiem
        # .json zawierającym informacje dot. przebiegu testu.
        def report_test_case_result(json_result, tc_result):
            current_time = time.time()
            formatted_current_time = datetime.datetime.fromtimestamp(current_time) \
                .strftime('%Y-%m-%d %H:%M:%S')

            # Pobranie external id test case.
            tc_external_id = tls.getTestCaseIDByName(list(json_result.keys())[0])[0][
                'tc_external_id']
            # Pobranie id test case.
            tc_id = tls.getTestCaseIDByName(list(json_result.keys())[0])[0]['id']

            # Wysłanie raportu do TestLink.
            tls.reportTCResult(tc_id, test_plan_id, "house_price_calc_build_no_1",
                               tc_result, create_note_message(json_result,
                                                              tc_result),
                               user='mrfarinq',
                               testcaseexternalid
                               =project_prefix + '-' + tc_external_id,
                               platformname='Python 3.6',
                               execduration=list(json_result.values())[0][
                                   'exec_time'],
                               timestamp=formatted_current_time)

            # Pobranie id ostatnio wykonanego testu w celu przesłania do niego
            # pliku .json.
            last_exec_id = tls.getLastExecutionResult(test_plan_id, tc_id)[0]['id']

            # Utworzenie pliku .json z informacjami dot. testu.
            with open('details.json', 'w') as outfile:
                json.dump(json_result, outfile)

            # Przesłanie informacji dot. testu w formie pliku .json do ostatnio
            # wykonanego testu w TestLink.
            tls.uploadExecutionAttachment('details.json',
                                          last_exec_id, "result_details",
                                          "Szczegółowe dane testu z dnia "
                                          + str(list
                                                (json_result.values())[0]
                                                ['time_start']))


        # Przetworzenie testów i wysłanie raportów do TestLink.
        for test_result_in_json in unittests_json_result['TestLibrary']['ok']:
            report_test_case_result(test_result_in_json, 'p')

        for test_result_in_json in unittests_json_result['TestLibrary']['fail']:
            report_test_case_result(test_result_in_json, 'f')

        for test_result_in_json in unittests_json_result['TestLibrary']['error']:
            report_test_case_result(test_result_in_json, 'b')

        if len(unittests_json_result['TestLibrary']['skip']) > 0:
            print("Skipped tests: ")
        for test_result_in_json in unittests_json_result['TestLibrary']['skip']:
            print(test_result_in_json)

        # Pobranie właściwości zestawu testów i wysłanie pliku podsumowującego.
        test_suite_statistics = {
            'test_suite_time_start': datetime.datetime.fromtimestamp
            (test_suite_time_start).strftime('%Y-%m-%d %H:%M:%S:%f'),
            'test_suite_time_end': datetime.datetime.fromtimestamp
            (test_suite_time_end).strftime('%Y-%m-%d %H:%M:%S:%f'),
            'test_suite_exec_time': test_suite_exec_time,
            'all_tests': len(unittests_json_result['TestLibrary']['ok'])
            + len(unittests_json_result['TestLibrary']['fail'])
            + len(unittests_json_result['TestLibrary']['error'])
            + len(unittests_json_result['TestLibrary']['skip']),
            'passed_tests': len(unittests_json_result['TestLibrary']['ok']),
            'failed_tests': len(unittests_json_result['TestLibrary']['fail']),
            'blocked_tests': len(unittests_json_result['TestLibrary']['error']),
            'skipped_tests': len(unittests_json_result['TestLibrary']['skip'])
        }

        unittests_json_result['TestSuiteStatistics'] = test_suite_statistics

        with open('details.json', 'w') as outfile:
            json.dump(unittests_json_result, outfile)

        tls.uploadTestSuiteAttachment('details.json', 3)
