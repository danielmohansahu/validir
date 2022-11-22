# validir

A command line Python tool / package for directory validation: making sure a directory structure matches an expected template.

---

## Example Usage

`validir` checks a local directory structure against a YAML template like the following:

```yaml
# contents of template.yaml
flags:                    # top-level flags used during the verification process
  allow_extra: false      # whether or not to consider the presence of extra files and directories an error
  check_hidden: false     # whether or not to check hidden files (i.e. files starting with '.')
root:                     # beginning of expected directory structure
- optional: ["*"]         # we expect a directory called 'optional' which can have anything in it
- whoops: []              # the whoops folder must be present and completely empty
- required:               # the required directory is, well, required
  - metadata:             # the metadata directory is required
    - "*.ext"             # metadata must have the extension .ext ...
    - "sample*"           # ... or start with the keyword "sample"
  - textfiles:            # textfiles is another required directory
    - "text*.txt"         # textfiles must be named text and end with the .txt extension
    - "text*.yaml"        # people can also store corresponding yaml files
  - required.txt          # the required file is required, naturally
```

To verify a local directory against this template, run the following:

```bash
validir validate {DIRECTORY} template.yaml
```

Validir also provides an API to generate templates from a given directory. This is intended as a bootstrapping process which allows users to refine a pre-existing directory structure instead of starting from scratch:

```bash
validir generate {DIRECTORY}
```

For more information about any command line options, call `validir --help`.

---

## Installation

**Via Package Manager**

Todo!

**Via Source**

To install locally, clone this repository and run the following:

```bash
git clone https://github.com/danielmohansahu/validir.git
python3 -m pip install ./validir
```

Installation verification is done via [tox](https://tox.wiki/en/latest/). To run the test suite:

```bash
# from within validir directory
tox
```

## Errata

PEP8 checks:

```bash
pycodestyle --ignore=E201,E202,E203,E266 --max-line-length=100 --indent-size=2 .
```
