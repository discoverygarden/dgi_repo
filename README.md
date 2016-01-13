# dgi_repo

## Introduction

This is a drop in replacement for Fedora in the context of most of Islandora.

## Requirements

This module requires the following:

* [Python 3.4.3+](https://www.python.org/)
* [falcon](http://falconframework.org/)
* [PostgreSQL](http://www.postgresql.org/)

## Installation

On Ubuntu 14.04.3: `sudo apt-get -y install python3 build-essential python3-pip && sudo pip3 install -e ./`

## Troubleshooting/Issues

Having problems or solved a problem? Contact [discoverygarden](http://support.discoverygarden.ca).

## Maintainers/Sponsors

Current maintainers:

* [discoverygarden](http://www.discoverygarden.ca)

## Development

The package is well documented internally, a quick way to deploy docs is to run
the command `pydoc3 -p 1234` and visit  `http://HOST:1234/dgi_repo`.

One can run the entire test suit from the project directory with
`python3 -m unittest discover -v`.

If you would like to contribute to this module, please check out our helpful
[Documentation for Developers](https://github.com/Islandora/islandora/wiki#wiki-documentation-for-developers)
info, [Developers](http://islandora.ca/developers) section on Islandora.ca and
contact [discoverygarden](http://support.discoverygarden.ca).

## License

None, licensing is TBD. If you are not an employee of DGI and have obtained this
software from someone other than DGI please contact DGI.
