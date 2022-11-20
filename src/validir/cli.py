""" Convenience function wrappers around core Template operations.
"""

# future
from __future__ import annotations

# STL
import typing
import argparse

# YAML
import yaml

# Custom
from .template import Template

def parse_args():
    parser = argparse.ArgumentParser("VALIDate DIRectory structures from a pre-defined template.")
    subparsers = parser.add_subparsers(help="commands")

    validate_parser = subparsers.add_parser('validate', help='Validate a given directory.')
    validate_parser.add_argument('dirname', help='Root of directory to validate.')
    validate_parser.add_argument('template', help='Template file (yaml format).')
    validate_parser.set_defaults(func=lambda args: validate(args.dirname, args.template))

    generate_parser = subparsers.add_parser('generate', help='Generate a template file from a target directory.')
    generate_parser.add_argument('dirname', help='Root of directory to validate.')
    generate_parser.add_argument('output', help='Output file (yaml format).')
    generate_parser.add_argument('--process-hidden', action="store_true", help="Don't skip hidden files and directories.")
    generate_parser.set_defaults(func=lambda args: generate_from_directory(args.dirname, args.output, not args.process_hidden))
    
    return parser.parse_args()
     
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
  
  if (success := template.validate(dirname)):
    print(f"Directory {dirname} matches template {templatefile}")
  else:
    print(f"Directory {dirname} DOES NOT MATCH template {templatefile}")
  return success

def main():
  args = parse_args()
  args.func(args)
