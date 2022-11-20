""" Convenience function wrappers around core Template operations.
"""

# future
from __future__ import annotations

# STL
import typing

# YAML
import yaml

# Custom
from .template import Template

def generate_from_directory(dirname : str, output : str) -> None:
  """ Construct a Template file for the given directory.
  """
  # construct core template
  template = Template.generate(dirname)

  # write to file
  with open(output, "w") as yamlfile:
    yaml.dump(template.dump(), yamlfile)
  print(f"Wrote extracted template from '{dirname}' to '{output}'")

def validate(dirname : str, templatefile : str) -> bool:
  """ Validate the given directory against the given template. """
  template = Template.generate(templatefile)
  return template.validate(dirname)
