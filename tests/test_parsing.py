""" Unit tests for verification of template file parsing.

These tests ensure we:
 - Are loading template files correctly.
 - Are saving template files correctly.
 - Are handling malformed / invalid template files correctly.
"""

# STL
import os
import glob

# pytest
import pytest

# YAML
import yaml

# validir
from validir.template import Template

# load templates with valid syntax
VALID = glob.glob(os.path.join("example_templates", "valid_*.yaml"))

# load templates with invalid syntax
INVALID = glob.glob(os.path.join("example_templates", "invalid_*.yaml"))

############################ TEST FUNCTIONS ###################################

def test_invalid_load():
    # make sure we fail when attempting to load the bad templates
    for template in INVALID:
        with pytest.raises(Exception):
            Template(template)

def test_load_and_dump():
    # make sure we can load the following and dump back into the exact same structure    
    for template in VALID:
        # grab the raw data
        with open(template, "r") as yamlfile:
            stream = yamlfile.read()

        # render as a YAML
        original = yaml.safe_load(stream)

        # make sure we can actually parse this!
        try:
            t = Template(stream)
        except Exception as e:
            assert False, f"Load failure: {e}"

        # compare parsed version to original
        assert (t.dump()["root"] == original["root"])
