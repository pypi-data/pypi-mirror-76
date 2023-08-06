Intro
======
|pypi| |bld| |cvg| |black|

Rye is a python task automation tool. It is `one`_ `of`_ a `long`_
`list`_ of other projects. The question at this point should be, why not
just use one of thos other tools?
The answer is that I had a workflow in mind, but couldn't quite get any
of the other tools to do it.

* Read from a simple config file
* Maintain a set of virtualenvs for each environment
* Update those environments when my pyproject.toml or poetry.lock files changed.
* Run all my tasks in parallel
* Let tasks share environments where that makes sense (lint and typing?)
* Work with poetry
* Allow installing dependencies and the package separately (for Dockerfile caching)

I was trying to set this up without thinking it through a ton, and kept fighting with
tox's built in defaults. No way to install packages without the source code. Using
poetry involved some truly ugly hacks. No auto-update of environments, and hard to share
environments between tasks. I did like that it depended on a config file with a lot of
built in behaviors that you could inherit from!

I looked at stuff like Nox and Invoke- Nox required more programming then tox and still
had a bunch of defaults I'd have to figure out how to override. Invoke would have just
been working from scratch.

What I really wanted was a makefile- list tasks, specify dependencies for those tasks,
and rebuild them when the dependencies change. The actual commands to run should
be completely configurable. So Rye was born. It uses pyproject.toml as configuration.
It will automatically keep your virtual environments in sync with your config files-
no matter the tool you're using. It has a good set of default behaviors you can pull in.
Best of all, every step of the process is completely configurable- if you want!


.. code-block:: toml

	# pyproject.toml
	[tool.rye]
	default_tasks = ["test", "lint", "format", "typing"]

	[tool.rye."task.pytest"]
	target_environments = ["poetry.py37", "poetry.py36"]

	[tool.rye."poetry.py36"."task.pytest"]
	commands = [["pytest", "tests", "--no-cov"]]

	[tool.rye."task.lint"]
	target_environments = ["poetry.py37"]
	commands = [["pylint", "src/rye", "tests"]]

	[tool.rye."task.format"]
	target_environments = ["poetry.py37"]
	commands = [
		["black", ".", "--check"],
		["isort", "-rc", "-tc", "--check-only", "src", "tests"],
	]

	[tool.rye."task.typing"]
	target_environments = ["poetry.py37"]
	commands = [
		["mypy", "src/rye", "--ignore-missing-imports"],
	]

OR, YAML

.. code-block:: yaml

    default_tasks:
      - test
      - lint
      - format
      - typing

    task.pytest:
      target_environments:
        - poetry.py37
        - poetry.py36

    poetry.py36:
      task.pytest:
        commands:
         - ["pytest", "tests", "--no-cov"]

    task.lint:
      target_environments:
        - poetry.py37
      commands:
        - ["pylint", "src/rye", "tests"]

    task.format:
      target_environments:
        - poetry.py37
      commands:
        - ["black", ".", "--check"]
        - ["isort", "-rc", "-tc", "--check-only", "src", "tests"]

    task.typing:
      target_environments:
        - poetry.py37
      commands:
        - ["mypy", "src/rye", "--ignore-missing-imports"]


.. code-block:: bash

	$ rye
	Running tasks- ['poetry.py37', 'TASK poetry.py37#lint', 'TASK poetry.py37#format', 'TASK poetry.py37#typing']
	ENV poetry.py37 > Preparing Env
	ENV poetry.py37 > Already using interpreter /home/pbecotte/venvs/rye/bin/python3.7
	ENV poetry.py37 > Using base prefix '/usr'
	ENV poetry.py37 > New python executable in /home/pbecotte/PycharmProjects/rye/.rye/py37/bin/python3.7
	ENV poetry.py37 > Also creating executable in /home/pbecotte/PycharmProjects/rye/.rye/py37/bin/python
	ENV poetry.py37 > Installing setuptools, pip, wheel...

Read the full documentation at https://rye.readthedocs.io/en/latest/
Or check out the source at https://gitlab.com/pjbecotte/rye

Installation
==================

You can install Rye from pypi-

::

	pip install rye

.. |cvg| image:: https://gitlab.com/pjbecotte/rye/badges/master/coverage.svg
.. |bld| image:: https://gitlab.com/pjbecotte/rye/badges/master/pipeline.svg
.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
.. |pypi| image:: https://badge.fury.io/py/rye.svg

.. _one: https://github.com/theacodes/nox
.. _of: https://github.com/tox-dev/tox
.. _long: https://github.com/fabric/fabric
.. _list: https://www.gnu.org/software/make/
