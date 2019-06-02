# code duplication finder

This package allows to traverse a list of repositories to find similiarities among the repos
to avoid copyrights collision or to check the quality of the code.

The default language it checks is scala, but this can be configured

## Installation
First install pmd:

``` sh
$ wget https://github.com/pmd/pmd/releases/download/pmd_releases%2F6.15.0/pmd-bin-6.15.0.zip
$ unzip pmd-bin-6.15.0.zip
$ alias cpd="$HOME/pmd-bin-6.15.0/bin/run.sh cpd"
```
Remember to add the alias to your .bashrc

## Configuration
Requirements: 

- Github access token(default: GITHUB_ACCESS_TOKEN environment variable)
- text file with a list of repositories to check(default: repos.txt)

## How to Run

python dope.py

### setting specific filename

python dope.py --repo_list bla.txt

### setting specific access token

python dope.py --token deadbeef

### setting specific language

python dope.py --language python

Note: The run will generate a folder named clones and eventually delete it, since the program clones repos, then the assumption is that there is enough harddrive space.
