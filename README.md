# mass-data-generator

Mass data generator for dev pruposes. This module creates a csv with as many records as needed.


&nbsp;  
&nbsp;  
## README Map

- Start with [Set-up and install](#set-up-and-install).
- To run locally, go to [Run from command line](#run-from-command-line).
- To use the main class, skip to [The main class](#the-main-class).
- For automatic tests, skip to [Automatic tests](#automatic-tests).
- If you prefer Docker, go to [Containerise with Dockerfile](#containerise-with-the-dockerfile).
- To run Docker Compose, skip to [Docker Compose](#run-the-docker-compose) instructions.
- About logs, please move to the corresponding topic, [Logs](#logs).
- Instructions on advanced/technical documentation, go to [Documentation](#documentation).
- Or click to skip to the [To do](#to-do) list.


## Set-up and install
_Note: To run automatically via Docker, Docker Compose or run automatic tests using Makefile, skip this chapter._  
_Note: I recommend using [virtualenv](https://realpython.com/python-virtual-environments-a-primer/) to run py manually._

Install the requirements:

    $ python3 -m pip install -r requirements.txt

Please check the [config file](config.py) to personalise variables as needed.

_Note: The [config file](config.py) should not be in a public repo, but once there are no secret keys in this project, the file was published to facilitate the instantiation. Normally, copying and editing [config template](config.py.tpl) would be recommended._


## Run from command line
_Note: By default, the proxy runs on port 5000. This can be changed in the [config file](config.py)._

From the project's root directory, please run the following command and follow instructions:

    $ python3 -m APP

At this point, we should be able to browse: http://localhost:5000/  
Please remember to hit Ctrl+c to stop the web server when done.


## The main class
_Note: to run from Python console, please refer to [Set-up and install](#set-up-and-install) first._

With the python console and the [APP class](APP/__init__.py), we can get things running:

    $ python3
    >>> from APP import APP
    >>> c = APP()
    >>> c.main_def()


## Automatic tests
Python tests are available using unittest via Makefile or manually.  

_Note: to run tests manually, please refer to [Set-up and install](#set-up-and-install) first._  
_Note: to run tests using Makefile, virtualenv must be already installed._  
_Note: depending on how the app is started, it may require ` sudo chmod o+w logs/* `._

Python tests are available manually or using Makefile.

- Run ` python3 -m unittest tests/test_* `.
- Or use make as in ` make test ` to setup, run the tests and clean up.


## Containerise with the Dockerfile
_I assume that you have docker engine running. If not, please see [Get Docker](https://docs.docker.com/get-docker/)._

If you rather run the proxy in a single container, run:

    $ docker run --rm -d -p 5000:5000 --name proxy $(docker build -f Dockerfile -t proxy . -q)

To know IP and Port to the containerised app:

    $ docker inspect proxy | grep -e IPAddr.*[0-9] -e HostPort | sed 's/[^0-9\.]//g' | sort -u

After this, we should be able to browse: http://\<container IP\>:5000/  

To stop container and clean image, use:

    $ docker stop proxy && docker image rm proxy


## Run the Docker compose
_I assume that you have docker compose installed. If not, please see [Install Docker Compose](https://docs.docker.com/compose/install/)._

There are Makefile rules to simplify this option. See the list of commands:

- ` $ make ` to build and run (up) the application.
    - or run `$ make build; make run ` _(note: run already calls build)_.
- ` $ make stop ` and ` make start ` to start the container.
- ` $ make rm ` to remove compose service, container, image.

The default HTTP proxy PORT is 5000 and set in [.env](.env). The port can be changed:

    $ HTTP_PORT=8080 make up


## Logs
By default, logs are recorded in the 'logs' directory in the project's root. However,
if you [Containerise](#containerise-with-the-dockerfile) the app, 
logs will be inside the container. And if you [Docker Compose](#run-the-docker-compose),
the container will use the hosts' dirs as in [Run from command line](#run-from-command-line).

Please see [docs/logs](docs/logs) if you wish to access samples of the generated logs.


## Documentation
Please try from python console:

    $ python3
    >>> import proxy
    >>> help(proxy)

Or try from command line:

    $ python3 -c "import proxy; help(proxy.config)"

All documentation can be found in [docs](docs).


## To do

* Automatic rotation of log files.
* Improve docstring.

