""" Class used to load, verify, and save directory templates.
"""

# future
from __future__ import annotations

# STL
import typing

class Template:
  def __init__(self, stream):
    # I am a stub
    ...

  def validate(self, dirname : str) -> bool:
    """ Validate the given directory against our schema. """
    # I am a stub
    return True
    
  @staticmethod
  def construct(dirname : str) -> Template:
    """ Factory method to construct from a directory. """
    # I am a stub
    return Template("""Stubby""")