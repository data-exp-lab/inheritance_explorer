.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/data-exp-lab/inheritance_explorer/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

inheritance_explorer could always use more documentation, whether as part of the
official inheritance_explorer docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/data-exp-lab/inheritance_explorer/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `inheritance_explorer` for local development.

1. Fork the `inheritance_explorer` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/inheritance_explorer.git

3. Install your local copy into a virtualenv. Assuming you have v
irtualenvwrapper installed, this is how you set up your fork for local
development::

    $ mkvirtualenv inheritance_explorer
    $ cd inheritance_explorer/
    $ python setup.py develop

4. (optional) Set up extra packages and pre-commit. There are number of packages
useful for development in ``requirements_dev.txt``. You can also use pre-commit to
make sure your changes will pass the style-related CI tests::

    $ python -m pip install -r requirements_dev.tx
    $ pre-commit install

5. Now, to make changes, create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

6. When you're done making changes, check that your changes pass the
   tests:

    $ pytest -v

7. Commit your changes and push your branch to GitHub. Note that if you
have installed pre-commit, the pre-commit linting will run and you may need
to re-add any changed files before the commit succeeds::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

8. Submit a pull request through the GitHub website.

