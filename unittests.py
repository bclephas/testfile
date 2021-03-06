import mock
import unittest

import testfile

@mock.patch('testfile._execute_commandline', return_value=('', '', 0))
@mock.patch('testfile._print_verbose')
@mock.patch('testfile._print_result')
@mock.patch('testfile._terminate_if_required')
class Testfile_tests(unittest.TestCase):
    def setUp(self):
        pass

    def test_single_test__no_testcases__executes_ok(self, mock_term, mock_result, mock_verbose, mock_execute):
        config = {'tests': {}}
        returncode = testfile.execute_testfile(config)
        self.assertEqual(0, returncode)

    def test_single_test__single_testcase__executes_ok(self, mock_term, mock_result, mock_verbose, mock_execute):
        config = {
            'tests': [
            {
                'test': 'test_1',
                'steps': [
                    'echo foo'
                ]
            }]
        }
        returncode = testfile.execute_testfile(config)
        self.assertEqual(0, returncode)

    def test_single_test__multiple_testcases__executes_ok(self, mock_term, mock_result, mock_verbose, mock_execute):
        config = {
            'tests': [
            {
                'test': 'test_1',
                'steps': [
                    'echo foo'
                ]
            },
            {
                'test': 'test_2',
                'steps': [
                    'echo bar'
                ]
            },
            ]
        }
        returncode = testfile.execute_testfile(config)
        self.assertEqual(0, returncode)

    def test_single_test__no_fixture__ok(self, mock_term, mock_result, mock_verbose, mock_execute):
        config = {
            'tests': [
            {
                'test': 'test_1',
                'steps': [
                    'echo foo'
                ]
            }
            ]
        }
        returncode = testfile.execute_testfile(config)
        self.assertEqual(0, returncode)

    def test_single_test__no_tests__should_not_break(self, mock_term, mock_result, mock_verbose, mock_execute):
        config = {
        }
        returncode = testfile.execute_testfile(config)
        self.assertEqual(0, returncode)

    def test_single_test__one_time_setup__called_exactly_once(self, mock_term, mock_result, mock_verbose, mock_execute):
        config = {
            'fixture': {
                'onetime_setup': 'foo',
            },
            'tests': [
            {
                'test': 'test_1',
                'steps': [
                    'echo foo'
                ]
            },
            {
                'test': 'test_2',
                'steps': [
                    'echo bar'
                ]
            },
            ]
        }
        testfile.execute_testfile(config, verbose=True)
        self.assertEqual(3, mock_execute.call_count)
        mock_execute.assert_has_calls([mock.call('foo'),
                                       mock.call('echo foo'),
                                       mock.call('echo bar')])

    def test_single_test__one_time_teardown__called_exactly_once(self, mock_term, mock_result, mock_verbose, mock_execute):
        config = {
            'fixture': {
                'onetime_teardown': 'foo'
            },
            'tests': [
            {
                'test': 'test_1',
                'steps': [
                    'echo foo'
                ]
            },
            {
                'test': 'test_2',
                'steps': [
                    'echo bar'
                ]
            },
            ]
        }
        testfile.execute_testfile(config, verbose=True)
        self.assertEqual(3, mock_execute.call_count)
        mock_execute.assert_has_calls([mock.call('echo foo'),
                                       mock.call('echo bar'),
                                       mock.call('foo')])

    def test_single_test__teardown_called_for_each_test(self, mock_term, mock_result, mock_verbose, mock_execute):
        config = {
            'fixture': {
                'teardown': 'foo'
            },
            'tests': [
            {
                'test': 'test_1',
                'steps': [
                    'echo foo'
                ]
            },
            {
                'test': 'test_2',
                'steps': [
                    'echo bar'
                ]
            },
            ]
        }
        testfile.execute_testfile(config, verbose=True)
        self.assertEqual(4, mock_execute.call_count)
        mock_execute.assert_has_calls([mock.call('echo foo'),
                                       mock.call('foo'),
                                       mock.call('echo bar'),
                                       mock.call('foo')])

    def test_single_test__setup_called_for_each_test(self, mock_term, mock_result, mock_verbose, mock_execute):
        config = {
            'fixture': {
                'setup': 'foo'
            },
            'tests': [
            {
                'test': 'test_1',
                'steps': [
                    'echo foo'
                ]
            },
            {
                'test': 'test_2',
                'steps': [
                    'echo bar'
                ]
            },
            ]
        }
        testfile.execute_testfile(config, verbose=True)
        self.assertEqual(4, mock_execute.call_count)
        mock_execute.assert_has_calls([mock.call('foo'),
                                       mock.call('echo foo'),
                                       mock.call('foo'),
                                       mock.call('echo bar')])

    def test_single_test__optional_description(self, mock_term, mock_result, mock_verbose, mock_execute):
        config = {
            'tests': [
            {
                'test': 'test_1',
                'description': 'foobarbaz',
                'steps': [
                    'echo foo'
                ]
            },
            ]
        }
        testfile.execute_testfile(config, verbose=True)
        mock_result.assert_has_calls([mock.call('test_1', mock.ANY, 0)])

    def test_single_test__test_fails__print_error(self, mock_term, mock_result, mock_verbose, mock_execute):
        mock_execute.return_value = ('', '', 3)

        config = {
            'tests': [
            {
                'test': 'test_1',
                'steps': [
                    'echo foo'
                ]
            },
            ]
        }
        testfile.execute_testfile(config, verbose=True)
        mock_result.assert_has_calls([mock.call('test_1', 'echo foo', 3)])

    def test_single_test__test_succeeds__print_pass(self, mock_term, mock_result, mock_verbose, mock_execute):
        config = {
            'tests': [
            {
                'test': 'test_1',
                'steps': [
                    'echo foo'
                ]
            },
            ]
        }
        testfile.execute_testfile(config, verbose=True)
        mock_result.assert_has_calls([mock.call('test_1', mock.ANY, 0)])

    def test_single_test__multiple_tests_one_fails__print_correct_error(self, mock_term, mock_result, mock_verbose, mock_execute):
        mock_execute.side_effect=[('', '', 0), ('', '', 3)]

        config = {
            'tests': [
            {
                'test': 'test_1',
                'steps': [
                    'echo foo'
                ]
            },
            {
                'test': 'test_2',
                'steps': [
                    'echo bar'
                ]
            },
            ]
        }
        testfile.execute_testfile(config, verbose=True)
        mock_result.assert_has_calls([mock.call('test_1', mock.ANY, 0), mock.call('test_2', 'echo bar', 3)])

    def test_single_test__test_multiple_steps__print_pass(self, mock_term, mock_result, mock_verbose, mock_execute):
        config = {
            'tests': [
            {
                'test': 'test_1',
                'steps': [
                    'echo foo',
                    'echo bar',
                    'echo baz'
                ]
            },
            ]
        }
        testfile.execute_testfile(config, verbose=True)
        mock_execute.assert_has_calls([mock.call('echo foo;echo bar;echo baz')])

    def test_disabled_tests__correct_results_shown(self, mock_term, mock_result, mock_verbose, mock_execute):
        config = {
            'tests': [
            {
                'disabled_test': 'test_1',
                'steps': [
                    'echo foo',
                ],
            },
            {
                'test': 'test_2',
                'steps': [
                    'echo bar',
                ]
            },
            ]
        }
        testfile.execute_testfile(config, verbose=True)
        mock_result.assert_has_calls([mock.call('test_1', '', 0, ignored=True),
                                      mock.call('test_2', 'echo bar', 0)])

    def test_disabled_tests__setup_and_teardown_not_executed(self, mock_term, mock_result, mock_verbose, mock_execute):
        config = {
            'tests': [
            {
                'disabled_test': 'test_1',
                'steps': [
                    'echo foo',
                ],
            },
            {
                'test': 'test_2',
                'steps': [
                    'echo bar',
                ]
            },
            ]
        }
        testfile.execute_testfile(config)
        mock_verbose.assert_has_calls([mock.call(False, '', '', 0)])

if __name__ == '__main__':
    unittest.main()

