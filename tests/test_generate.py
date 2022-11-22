""" Unit tests for verification of template generation from data.

These tests ensure we:
 - Generate expected template files from sample directories.
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

# test directories and the location of ground truth data
DIRECTORIES = ["directories/extra_directory", "directories/missing_directory", "directories/simple_directory"]
TRUTH_DIR = "directories/generated_templates"

############################ TEST FUNCTIONS ###################################

def test_generation():
    # iterate through all test directories
    for directory in DIRECTORIES:
        # generate templates with a variety of conditions
        template_hidden = Template.construct(directory, check_hidden=True, allow_extra=True)
        template_no_hidden = Template.construct(directory, check_hidden=False, allow_extra=True)
        
        # compare to "ground truth"
        with open(os.path.join(TRUTH_DIR, directory + "_hidden.yaml"), "r") as yamlfile:
            assert yaml.safe_load(yamlfile)["root"] == template_hidden.dump()["root"]
        with open(os.path.join(TRUTH_DIR, directory + "_no_hidden.yaml"), "r") as yamlfile:
            assert yaml.safe_load(yamlfile)["root"] == template_no_hidden.dump()["root"]