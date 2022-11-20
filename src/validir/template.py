""" Class used to load, verify, and save directory templates.
"""

# future
from __future__ import annotations

# STL
import os
import typing
import functools
from collections import defaultdict
from operator import getitem

# YAML
import yaml

# Custom
from .types import Directory, File

def recursively_build_tree(node, dir, skip_hidden):
  # helper function to convert a dictionary of YAML keys to a linked tree structure
  if isinstance(node, str):
    if not (f := File.load(node)).hidden or not skip_hidden:
      dir.children.append(f)
  elif isinstance(node, list):
    for item in node:
      recursively_build_tree(item, dir, skip_hidden)
  elif isinstance(node, dict):
    for key,val in node.items():
      if not (d := Directory.load(key)).hidden or not skip_hidden:
        dir.children.append(d)
        recursively_build_tree(val, dir.children[-1], skip_hidden)
  else:
    raise KeyError("Encountered unexpected key type - only [str, list, dict] are supported.")

class Template:
  def __init__(self, stream):
    # attempt to perform a pure yaml load
    raw = yaml.safe_load(stream)
    
    # validate
    assert "root" in raw, "Missing required keyword 'root'."
    assert isinstance(raw["root"], list), "'root' key must be a list."

    # get other options
    self.skip_hidden = raw.get("skip_hidden", True)

    # recursively convert to our internal tree representation
    self.root = Directory("root", False, [])
    recursively_build_tree(raw["root"], self.root, self.skip_hidden)

  def validate(self, dirname : str) -> bool:
    """ Validate the given directory against our schema. """
    # I am a stub
    return True
    
  def dump(self) -> dict:
    """ Dump internal representation to a dictionary. """
    return self.root.dump()

  @staticmethod
  def construct(dirname : str, skip_hidden : bool = True) -> Template:
    """ Factory method to construct from a directory.
    
    Args:
      dirname:      The directory to use as a template.
      skip_hidden:  Whether or not to consider hidden files.
    """
    # extract all files via os.walk
    intermediary = {"skip_hidden": skip_hidden, "root": []}

    # walk through all directories / files
    for root, dirs, files in os.walk(dirname):

      # remove top level root directory and get list of sub-directories
      roots = root.replace(dirname, "", 1).split(os.sep)[1:]

      # get target node in our dictionary
      handle = intermediary["root"]
      for path in roots:
        handle = next(item[path] for item in handle if (isinstance(item, dict) and path in item))
      
      # naively add directories to their place in the hierarchy
      for directory in dirs:
        handle.append({directory : []})

      # add files based on our desired level of strictness
      for filename in files:
        handle.append(filename)

    # we dump this back into yaml format (which is kinda silly) and use nominal constructor
    return Template(yaml.dump(intermediary))