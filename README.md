# dgi_repo

## Introduction

This is a drop in replacement for Fedora in the context of most of Islandora.

## Requirements

This module requires the following:

* [Python 3.4.3+](https://www.python.org/)
* [PostgreSQL](http://www.postgresql.org/)
* [psycopg](https://pypi.python.org/pypi/psycopg2)
* [falcon](http://falconframework.org/)
* [talons](https://pypi.python.org/pypi/talons/)
* [falcon-multipart](https://github.com/yohanboniface/falcon-multipart)
* [lxml](https://pypi.python.org/pypi/lxml)
* [simplejson](https://pypi.python.org/pypi/simplejson/)
* [PyYAML](https://pypi.python.org/pypi/PyYAML)

## Installation

On Ubuntu 14.04.3:

```
sudo apt-get -y install python3 build-essential python3-pip libxml2-dev libxslt1-dev libyaml-dev zlib1g-dev libpq-dev
sudo pip3 install --process-dependency-links -e ./
# Copy and modify the sample configuration file and deploy it to `/etc/dgi_repo/dgi_repo.yml`.
python3 -c "from dgi_repo import utilities; utilities.install();"
```

## Troubleshooting/Issues

Please check out our [wiki](http://code.discoverygarden.ca/dgi_repo/dgi_repo/wikis/home).

Having problems or solved a problem? Contact [discoverygarden](http://support.discoverygarden.ca).

## Maintainers/Sponsors

Current maintainers:

* [discoverygarden](http://www.discoverygarden.ca)

## Development

The package is well documented internally, a quick way to deploy docs is to run
the command `pydoc3 -p 1234` and visit  `http://HOST:1234/dgi_repo`.

One can run the entire test suit from the project directory with
`python3 -m unittest discover -v`.

For quick dev setups to get the endpoint running, `gunicorn` works quite well
(and is easily installed via `pip`). Something like:
`gunicorn -b localhost:8000 --reload --log-level DEBUG dgi_repo.fcrepo3.app:app`
should get you quickly on your feet (feel free to replace `localhost` with
`0.0.0.0` if you need to hit it from another machine.


If you would like to contribute to this module, please check out our helpful
[Documentation for Developers](https://github.com/Islandora/islandora/wiki#wiki-documentation-for-developers)
info, [Developers](http://islandora.ca/developers) section on Islandora.ca and
contact [discoverygarden](http://support.discoverygarden.ca).

## License

None, licensing is TBD. If you are not an employee of DGI and have obtained this
software from someone other than DGI please contact DGI.
