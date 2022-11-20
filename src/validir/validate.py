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

def generate_from_directory(dirname : str, output : str = None, skip_hidden : bool = True):
  """ Construct a Template for the given directory.
  
  Args:
    dirname:      The directory to use as a template.
    output:       A file to save output; if not specified the template object is returned.
    skip_hidden:  Whether or not to ignore hidden files.
  """
  # construct core template
  template = Template.construct(dirname, skip_hidden)

  if output is None:
    return template
  else:
    # write to file
    with open(output, "w") as yamlfile:
      yaml.dump(template.dump(), yamlfile)
    print(f"Wrote extracted template from '{dirname}' to '{output}'")

def validate(dirname : str, templatefile : str) -> bool:
  """ Validate the given directory against the given template. """
  template = Template.generate(templatefile)
  return template.validate(dirname)
