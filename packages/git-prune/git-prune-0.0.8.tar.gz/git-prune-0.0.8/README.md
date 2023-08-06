# git-prune

![license](https://img.shields.io/github/license/mashape/apistatus.svg)
![pythonver](https://img.shields.io/badge/python-3.5%2B-blue.svg)
![git-prune-ver](https://img.shields.io/badge/version-0.0.8-lightgrey.svg)

Clean up your local git branches to match the remote with one command. This tool checks your remote location for current branches, compares this list against the local git branches, and gives you the option to remove all orphaned local branches.

### Installation

`pip3 install git-prune`

### Usage

`git-prune` -- Prunes local branches in the current working directory.

`git-prune -d /Path/to/repository` -- Prunes local branches in the provided directory.
