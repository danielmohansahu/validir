""" Regression tests for full validation of directories against templates.

These tests ensure full end-to-end operation is as expected.
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

# test directories and the corresponding templates
DIRECTORIES = ["directories/extra_directory", "directories/missing_directory", "directories/simple_directory"]
TEMPLATES = "directories/validation_templates"

############################ TEST FUNCTIONS ###################################

def test_validation():
    # iterate through all test directories
    for directory in DIRECTORIES:
        # find the corresponding templates
        valid_templates = glob.glob(os.path.join(TEMPLATES, directory, "valid", "*.yaml"))
        invalid_templates = glob.glob(os.path.join(TEMPLATES, directory, "invalid", "*.yaml"))
        
        # make sure the valid templates succeed
        for template in valid_templates:
            assert (Template(template).validate(directory))

        # make sure the invalid templates fail
        for template in invalid_templates:
            assert (not Template(template).validate(directory))

