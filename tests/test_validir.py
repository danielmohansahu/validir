""" Unit Test for validation of Template Input/Output (i.e. reading / writing from files).
"""

# pytest
import pytest

# YAML
import yaml

# validir
from validir.template import Template
from validir.validate import generate_from_directory

# define some valid and invalid documents
simple_valid_docs = [
"""root:
    - foo
""",
"""root:
    - foo:
        - bar1
"""
]
simple_invalid_docs = [
"""root:
    foo:
        bar
""",
"""foo:
    - bar
""",
"""foo:
"""
]

def test_load():
    # make sure we succeed when loading these simple objects
    for doc in simple_valid_docs:
        try:
            Template(doc)
        except Exception as e:
            assert False, f"Load failure: {e}"

    # make sure we fail when loading these simple invalid objects
    for doc in simple_invalid_docs:
        with pytest.raises(Exception):
            Template(doc)

    # make sure we succeed when loading this more complex version
    with open("samples/sample_template_1.yaml", "r") as yamlfile:
        try:
            Template(yamlfile)
        except Exception as e:
            assert False, f"Load failure: {e}"

def test_transitive():
    # make sure we can load from and dump to file without changing anything
     
    with open("samples/sample_template_1.yaml", "r") as yamlfile:
        stream = yamlfile.read()

    # save nominal yaml load
    original = yaml.safe_load(stream)

    # make sure we can actually parse this!
    try:
        t = Template(stream)
    except Exception as e:
        assert False, f"Load failure: {e}"

    # compare parsed version to original
    parsed = t.dump()
    assert (parsed["root"] == original["root"])

def test_simple_directory():
    """ Construct a variety of templates from a sample directory; validate against real directory. """
    # the subject of our analysis
    directory = "simple_directory"
    
    # generate template
    template_hidden = generate_from_directory(directory, skip_hidden=False)
    template_no_hidden = generate_from_directory(directory, skip_hidden=True)
    
    # compare to "ground truth"
    with open("expected/simple_directory_hidden.yaml", "r") as yamlfile:
        assert yaml.safe_load(yamlfile)["root"] == template_hidden.dump()["root"]
    with open("expected/simple_directory_no_hidden.yaml", "r") as yamlfile:
        assert yaml.safe_load(yamlfile)["root"] == template_no_hidden.dump()["root"]
    
    # perform validation against real data
    assert (template_hidden.validate(directory))
    assert (template_no_hidden.validate(directory))

    # now make sure we catch missing files
    assert (not template_hidden.validate("missing_directory", allow_extra=True))
    assert (not template_no_hidden.validate("missing_directory", allow_extra=True))
    
    # and make sure we catch extra files (if we're being strict)
    assert (not template_hidden.validate("missing_directory", allow_extra=False))
    assert (not template_no_hidden.validate("missing_directory", allow_extra=False))
