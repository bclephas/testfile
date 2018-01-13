#!/usr/bin/env python

from __future__ import print_function

import argparse
import os
import subprocess
import sys

# Facilitate having a locally available PyYAML instance
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'pyyaml/lib/')))
import yaml

def _build_commandline(commands):
    '''Commands can be a list or a simple string'''
    if not isinstance(commands, basestring):
        script = ';'.join(commands)
    else:
        script = commands

    return script

def _execute_commandline(script):
    '''Executes the script provided.
       Returns a tuple with stdout, stderr and the process's exitcode'''
    process = subprocess.Popen(script,
                               shell=True,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    (out, err) = process.communicate()
    
    return (out.strip(), err.strip(), process.returncode)

def _print_verbose(verbose, out, err, returncode):
    '''Prints additional information for easier debugging'''
    if verbose:
        print('Out: [\n' + out + '\n]\nErr: [\n' + err + '\n]\nReturncode: ' + str(returncode))

def _print_result(test, step, returncode):
    '''Prints the result of the test case, using ANSI colors for improved visibility'''
    class ANSI(object):
        ESCAPE  = '\033[%sm'
        RESET   = ESCAPE %  '0'
        BLACK   = ESCAPE % '30'
        RED     = ESCAPE % '31'
        GREEN   = ESCAPE % '32'
        YELLOW  = ESCAPE % '33'
        BLUE    = ESCAPE % '34'
        MAGENTA = ESCAPE % '35'
        CYAN    = ESCAPE % '36'
        WHITE   = ESCAPE % '37'

        @staticmethod
        def decorate(fmt, msg):
            return fmt + msg + ANSI.RESET

    result = ANSI.decorate(ANSI.GREEN, 'PASS') if returncode == 0 else ANSI.decorate(ANSI.RED, 'FAILED')
    print('{} ... {}'.format(test, result))
    if returncode != 0:
        print('Command \'{}\' failed; expected exitcode {}, but was {}'.format(step, 0, returncode))

def _terminate_if_required(returncode):
    '''When returncode is non-zero, terminate the script'''
    if returncode != 0:
        sys.exit(returncode)

def execute_testfile(config, verbose=False):
    '''Executes all commands in the provided Testfile. Config is a yamlified dictionary'''
    fixture_config = config.get('fixture', {})

    # handle fixture's one time setup
    if 'onetime_setup' in fixture_config:
        script = _build_commandline(fixture_config['onetime_setup'])
        (out, err, returncode) = _execute_commandline(script)
        _print_verbose(verbose, out, err, returncode)
        _terminate_if_required(returncode)

    tests = config.get('tests', [])
    for test in tests:
        test_description = test['test']

        try:
            returncode = 0

            # handle fixture's setup
            if 'setup' in fixture_config:
                test_setup_script = _build_commandline(fixture_config['setup'])
                (out, err, returncode) = _execute_commandline(test_setup_script)
                _print_verbose(verbose, out, err, returncode)

            if returncode != 0:
                continue

            # handle test steps
            test_script = _build_commandline(test['steps'])
            (out, err, returncode) = _execute_commandline(test_script)
            _print_verbose(verbose, out, err, returncode)

            if returncode != 0:
                continue
        finally:
            test_returncode = returncode

            # handle fixture's teardown
            if 'teardown' in fixture_config:
                test_setup_script = _build_commandline(fixture_config['teardown'])
                (out, err, returncode) = _execute_commandline(test_setup_script)
                _print_verbose(verbose, out, err, returncode)
   
            _print_result(test_description, test_script, test_returncode)

    # handle fixture's one time teardown
    if 'onetime_teardown' in fixture_config:
        script = _build_commandline(fixture_config['onetime_teardown'])
        (out, err, returncode) = _execute_commandline(script)
        _print_verbose(verbose, out, err, returncode)
        _terminate_if_required(returncode)

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', dest='filename', nargs='+', default='Testfile')
    parser.add_argument('-v', '--verbose', dest='verbose', default=False, action='store_true')
    
    args = parser.parse_args()

    if isinstance(args.filename, basestring):
        filenames = [args.filename]
    elif isinstance(args.filename, list):
        filenames = args.filename
    else:
        raise ValueError('filename argument should be a string or a list')

    for filename in filenames:
        if not os.path.isfile(filename):
            print('{} not found{}'.format(filename, os.linesep), file=sys.stderr)
            parser.print_help()
            sys.exit(1)

        stream = file(filename, 'r')
        config = yaml.load(stream)

        returncode = execute_testfile(config, args.verbose)
        if returncode != 0:
            sys.exit(returncode)

    sys.exit(0)

