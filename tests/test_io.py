""" Unit Test for validation of Template Input/Output (i.e. reading / writing from files).
"""

# pytest
import pytest

# validir
from validir.template import Template

# define some valid and invalid documents
simple_valid_docs = [
"""root:
    - foo
""",
"""root:
    - foo:
        - bar1
"""
]
simple_invalid_docs = [
"""root:
    foo:
        bar
""",
"""foo:
    - bar
""",
"""foo:
"""
]

def test_simple_load():
    # make sure we succeed when loading these
    for doc in simple_valid_docs:
        try:
            Template(doc)
        except Exception as e:
            assert False, f"Load failure: {e}"

def test_simple_load_bad():
    # make sure we fail when loading these
    for doc in simple_invalid_docs:
        with pytest.raises(Exception):
            Template(doc)

def test_load():
    # make sure we succeed when loading this
    with open("sample_template_1.yaml", "r") as yamlfile:
        try:
            Template(yamlfile)
        except Exception as e:
            assert False, f"Load failure: {e}"

