Place your Juliet C/C++ test case files in this directory.

Juliet test cases typically contain functions named:
- *_bad() - vulnerable code
- *_good() - secure code (ground truth)

The parse_juliet.py script will extract these functions automatically.

Example structure:
juliet_files/
  ├── CWE123/
  │   ├── test_case_1.c
  │   └── test_case_2.c
  └── CWE456/
      └── test_case_3.c



