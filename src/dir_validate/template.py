""" Class used to load, verify, and save directory templates.
"""

# STL
import os
import typing
import functools
from operator import getitem

# YAML
import yaml

""" Encapsulation of a directory template; loaded via file or string.
"""
class Template:
    # keywords
    FILE_KEY = "$FILES$"

    def __init__(self):
        ...

    @classmethod
    def generate(cls, dirname : str, output : str, strict : bool = False, skip_hidden : bool = True):
        """ Helper function to generate a template file from an existing directory.

        This is intended for use as a first-pass autogeneration from an existing
        desired directory structure. The user can then edit certain hard-to-infer
        details like how to validate the files in each sub-directory.

        Args:
            dirname: Directory to use as a template.
            output:  Filename to save the template.
            strict:  Whether or not to require exact files - default behavior just validates by extension.
            skip_hidden: Ignore hidden files and directories (UNIX path convention)
        """
        # set up helper function to add files to desired level of strictness
        def get_files_strict(files):
            return files
        def get_files(files):
            extensions = set()
            for filename in files:
                split = filename.split(os.extsep,1)
                if len(split) == 2:
                    extensions.add(f"*.{split[-1]}")
                else:
                    extensions.add(f"*.")
            return extensions

        # initialize as a dictionary
        template = {}

        # walk through all directories / files
        for root, dirs, files in os.walk(dirname):
            # bypass hidden files and directories
            if skip_hidden:
                files = [f for f in files if not f[0] == '.']
                dirs[:] = [d for d in dirs if not d[0] == '.']

            # remove top level root directory and get list of sub-directories
            roots = root.replace(dirname, "", 1).split(os.sep)[1:]

            # get target node in our dictionary
            if roots == [""]:
                # handle first root (empty):
                handle = template
            else:
                # otherwise, access the proper place
                handle = functools.reduce(getitem, roots, template)
            
            # naively add directories to their place in the hierarchy
            for directory in dirs:
                handle[directory] = {}

            # add files based on our desired level of strictness
            filenames = get_files_strict(files) if strict else get_files(files)
            if len(filenames) != 0:
                handle[cls.FILE_KEY] = []
                for filename in filenames:
                    handle[cls.FILE_KEY].append(filename)

        # done; write to file
        with open(output, "w") as yamlfile:
            yaml.dump(template, yamlfile)
        print(f"Wrote extracted template from '{dirname}' to '{output}'")
    
