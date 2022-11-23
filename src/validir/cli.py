""" Convenience function wrappers around core Template operations.
"""

# future
from __future__ import annotations

# STL
import os
import sys
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
    validate_parser.set_defaults(func=validate)

    generate_parser = subparsers.add_parser('generate',
                                            help='Generate a template file from a directory.')
    generate_parser.add_argument('dirname', help='Root of directory to validate.')
    generate_parser.add_argument('output', help='Output file (yaml format).')
    generate_parser.add_argument('--check-hidden', action="store_true",
                                 help="Also check 'hidden' files.")
    generate_parser.add_argument('--allow-extra', action="store_true",
                                 help="Consider the presence of extra files an error.")
    generate_parser.set_defaults(func=generate)

    return parser.parse_args()


def generate(args):
  """ Generate a template from the given directory. """

  # sanity checks
  assert (os.path.isdir(args.dirname)), "Input directory must be, well, a directory."

  # construct core template
  print(f"Generating template from '{args.dirname}'")
  template = Template.construct(args.dirname, args.check_hidden, args.allow_extra)

  # write to file
  with open(args.output, "w") as yamlfile:
    yaml.dump(template.dump(), yamlfile)
  print(f"Wrote extracted template from '{args.dirname}' to '{args.output}'")


def validate(args):
  """ Validate the given directory against the given template. """

  # sanity checks
  assert (os.path.isdir(args.dirname)), "Input directory must be, well, a directory."

  with open(args.template, "r") as yamlfile:
    if (success := Template(yamlfile).validate(args.dirname)):
      print(f"Directory {args.dirname} matches template {args.template}")
      sys.exit(0)
    else:
      print(f"Directory {args.dirname} DOES NOT MATCH template {args.template}")
      sys.exit(1)

def main():
  args = parse_args()
  args.func(args)
