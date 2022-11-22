""" Common types used throughout the codebase.
"""

# future
from __future__ import annotations

# STL
import os
import re
import enum
from typing import NamedTuple
from fnmatch import fnmatch

# compile regex to look for fnmatch type strings
RE_FNMATCH_CHARS = re.compile('[?*\[\]]')

class File(NamedTuple):
  """ Core representation of a Node for a File. """
  name : str      # name representation
  hidden: bool    # whether or not this is a hidden filetype
  required: bool  # whether or not this is an explicitly required file
  
  def __eq__(self, other : [File, Directory]) -> False:
    """ Check if we match the given template. """
    if isinstance(other, Directory):
      return False
    # check bidirectionally, since we could be called from either end
    return fnmatch(self.name, other.name) or fnmatch(other.name, self.name)

  @staticmethod
  def load(string : str) -> File:
    """ Construct a File object from the given string representation. """
    return File(string, string[0] == ".", RE_FNMATCH_CHARS.match(string))
    
  def dump(self) -> str:
    """ Convert to a string representation. """
    return self.name
    
class Directory(NamedTuple):
  """ Core representation of a Node for a Directory. """
  name : str      # name representation
  hidden: bool    # whether or not this is a hidden filetype
  required: bool  # whether or not this is an explicitly required directory
  children : dict # all children; this only applies for dictionaries

  def __eq__(self, other : [File, Directory]) -> False:
    """ Check if we match the given template. """
    if isinstance(other, File):
      return False
    # check bidirectionally, since we could be called from either end
    return fnmatch(self.name, other.name) or fnmatch(other.name, self.name)

  @staticmethod
  def load(string : str) -> Directory:
    """ Construct a dictionary object from the given string representation. """
    return Directory(string, string[0] == ".", RE_FNMATCH_CHARS.match(string), [])
    
  def dump(self) -> dict:
    """ Recursively generate a dict representation from children. """
    return {self.name : [c.dump() for c in self.children]}
