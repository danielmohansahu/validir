""" Unit Test for validation of Template Input/Output (i.e. reading / writing from files).
"""

# pytest
import unittest

# dir_validate
# from dir_validate import Template

# content of test_sample.py
def inc(x):
    return x + 1

def test_answer():
    assert inc(3) == 4

