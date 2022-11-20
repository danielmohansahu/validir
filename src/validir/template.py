""" Class used to load, verify, and save directory templates.
"""

# future
from __future__ import annotations

# STL
import typing
from collections import defaultdict

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
  def construct(dirname : str) -> Template:
    """ Factory method to construct from a directory. """
    # I am a stub
    return Template("""Stubby""")