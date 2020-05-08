# Hydrogit

![splash](splash.png)

Hydrogit is a wrapper around the Hydrogen tool that automates the process of pulling and building source code versions.
Currently, CMake and GNU Automake/configure are supported.

## Overview

Hydrogit works in the following steps:

1. Clone code from github or a local project folder
1. Extract the given versions by commit ID
1. Add annotations to target LLVM IR and build the project

## Results

Hydrogit was able to build the following notable projects with CMake:

- Lua https://github.com/LuaDist/lua​
- GLEW https://github.com/Perlmint/glew-cmake​
- OpenSSL https://github.com/janbar/openssl-cmake​

We were also able to build GNU findutils(https://savannah.gnu.org/git/?group=findutils) from source with Make.
And it only took 10 minutes to build the MVICFG! :)

The results for lua and findutils are given as .dot and .pdf in `results`.

### Reproducing

With the CMake projects mentioned, the results can be run by pulling from the GitHub repository.

Make projects are less standardized by nature, so often will require some configuration beforehand.
While the tool will work for projects that only require the classic `./configure && make`, any other
customization will have to happen offline.

For findutils, we pulled the code and ran the `bootstrap` script because it takes a very long time
to build otherwise (it crawls Savannah's git repositories to check which version of gnulibs it needs).
The included `findutils` folder holds our version after having run `./bootstrap`.

## Usage

The project was built using `Python 3.8`.
All Python dependencies are in the Python standard library.

To build CMake projects, Hydrogit depends on another project hosted on Github:
https://github.com/compor/llvm-ir-cmake-utils.
It's linked as a submodule, but to get it you have to clone this repository with `git clone --recursive`.
If you already cloned but forgot `--recursive`, load it with `git submodule update --init`.

### To Run

**Run with** `python hydrogit.py`.
The program requires at least three positional arguments, in this order:

- URL/directory from which to clone code
- `>=2` commit ID's, in version order(i.e. earliest first)

Note running with the verbose(`-v`) flag slows down the program quite a bit.
If a build fails, you must be running with `-v` to see the cause of the error.
Examples of running the program are given in `USAGE.md`.

### Command line options

General options:
```
-h, --help            show this help message and exit
-L, --local           clone from a local dir
-v, --verbose         show CMake output
-l LANGUAGE, --language LANGUAGE
                    compile with this language - should be C or CXX
```

CMake-specific options:
```
-C, --cmake           build with CMake
```

Make-specific options:
```
-r RULE_NAME, --rule RULE_NAME
                    name of the Makefile rule to build
```
