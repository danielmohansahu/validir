""" Common types used throughout the codebase.
"""

# future
from __future__ import annotations

# STL
import os
import enum
from typing import NamedTuple

class File(NamedTuple):
  """ Core representation of a Node for a File. """
  name : str      # name representation
  hidden: bool    # whether or not this is a hidden filetype
  extension : str # file extension
  
  @staticmethod
  def load(string : str) -> File:
    """ Construct a File object from the given string representation. """
    extension = string.split(os.extsep)[-1] if len(string.split(os.extsep)) == 2 else None
    return File(string, string[0] == ".", extension)
    
  def dump(self) -> str:
    """ Convert to a string representation. """
    return self.name

class Directory(NamedTuple):
  """ Core representation of a Node for a Directory. """
  name : str      # name representation
  hidden: bool    # whether or not this is a hidden filetype
  children : dict # all children; this only applies for dictionaries
  
  @staticmethod
  def load(string : str) -> Directory:
    """ Construct a dictionary object from the given string representation. """
    return Directory(string, string[0] == ".", [])
    
  def dump(self) -> dict:
    """ Recursively generate a dict representation from children. """
    return {self.name : [c.dump() for c in self.children]}
