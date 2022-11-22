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
DIRECTORIES = ["extra_directory", "missing_directory", "simple_directory"]
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
            print(f"Validating '{directory}' against '{template}'")
            with open(template, "r") as yamlfile:
                assert (Template(yamlfile).validate(os.path.join("directories", directory)))

        # make sure the invalid templates fail
        for template in invalid_templates:
            print(f"Validating '{directory}' against '{template}'")
            with open(template, "r") as yamlfile:
                assert (not Template(yamlfile).validate(os.path.join("directories", directory)))
