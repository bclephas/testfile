# Testfile

Testfile is a small Python based framework for executing various shell commands
in a unit test like fashion. Testfile can be used to automate tedious and
often repeated shell commands.

The Testfile is structured using keywords that are described below.

# Example Testfile

    fixture:
      onetime_setup: echo "Will execute at most once, before the first test"
      setup:
        - echo "Will execute for each test, as a sequence of commands"
    tests:
      - test: "my test"
        description: "Some comments about this test"
        steps:
          - echo "First step"
          - echo "Second step"
      - test: "another test"
        steps:
          - echo "First and only step of this test"

# Usage

Create a file called Testfile and invoke Testfile. Alternatively
invoke Testfile with a filename of choice.

    usage: testfile.py [-h] [-f FILENAME] [-v]

    optional arguments:
      -h, --help            show this help message and exit
      -f FILENAME, --file FILENAME
      -v, --verbose

# Keywords

| Keyword          | Required   | Description                                                        |
|------------------|------------|--------------------------------------------------------------------|
| fixture          | No         | Defines common properties for available test cases                 |
| onetime_setup    | No         | Command executed once before running the first test case           |
| onetime_teardown | No         | Command executed once after running the last test case, guaranteed |
| setup            | No         | Command executed at the start of each test case                    |
| teardown         | No         | Command executed at the end of each test case, guaranteed          |
| tests            | Yes        | Test case definitions                                              |
| test             | No         | Single test case definitions                                       |
| description      | No         | Free format textual description of the test                        |
| steps            | Yes        | List of commands to be executed                                    |

## Fixture (optional)

Defines common properties for test cases that are grouped together in this
fixture.

## Onetime_setup (optional)

This command is *always* executed exactly once before the first test case is
executed, when available.
Value can be a string or a list of strings representing the commands to execute.

## Onetime_teardown (optional)

This command is *always* executed exactly once after the last test case has
executed, when available.
This command always runs, even with failures in the test cases, when available.
Value can be a string or a list of strings representing the commands to execute.

## Setup (optional)

This command is *always* executed before each test case inside the fixture.
Value can be a string or a list of strings representing the commands to execute.

## Teardown (optional)

This command is *always* executed after each test case inside the fixture.
This command always runs, even with failures in the test case, when available.
Value can be a string or a list of strings representing the commands to execute.

## Tests (mandatory)

Definitions of test cases in this fixture.
Recommended is to group related test cases together in one file.

## Test (optional)

Defines a single test case

## Description (optional)

A free format singleline string to write anything you might like.
Multiline stirngs are not supported at this time.

## Steps (mandatory)

Contains a list of individual commands to execute in succession.
If a command returns a non-zero exit code, the steps and thereby the test
fails.
Value can be a string or a list of strings representing the commands to execute.

* Multiline strings are not supported at this time.
* Complex steps are best invoked from a separate script. External scripts are
  executed with /bin/sh.

