# Contributing

Contributions are welcome, and they are greatly appreciated\! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at https://github.com/santandersecurityresearch/corsair_scan/issues

If you are reporting a bug, please include:

  - Your operating system name and version.
  - Any details about your local setup that might be helpful in
    troubleshooting.
  - Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and
"help wanted" is open to whoever wants to implement it.

### Implementing Features

Look through the GitHub issues for features. Anything tagged with
"enhancement" and "help wanted" is open to whoever wants to implement
it.

### Write Documentation

corsair_scan could always use more documentation, whether as part of
the official corsair_scan docs, in docstrings, or even on the web in
blog posts, articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at
https://github.com/santandersecurityresearch/corsair_scan/issues

If you are proposing a feature:

  - Explain in detail how it would work.
  - Keep the scope as narrow as possible, to make it easier to
    implement.
  - Remember that this is a volunteer-driven project, and that
    contributions are welcome :)

## Get Started\!

Ready to contribute? Here's how to set up
<span class="title-ref">corsair_scan</span> for local development.

1.  Fork the corsair_scan repo on GitHub.

2.  Clone your fork locally:
    
        $ git clone git@github.com:your_name_here/corsair_scan.git

3.  Install your local copy into a virtualenv. Assuming you have
    virtualenvwrapper installed, this is how you set up your fork for
    local development:
    
        $ mkvirtualenv corsair_scan
        $ cd corsair_scan/
        $ python setup.py develop

4.  Create a branch for local development:
    
        $ git checkout -b name-of-your-bugfix-or-feature
    
    Now you can make your changes locally.

5.  When you're done making changes, check that your changes pass flake8, bandit, safety
    and the tests. You can run it either in your local environment, or pushing code to your repo, 
    
    as it will trigger the pipeline that include all those steps.
    
    ```
    $ flake8 corsair_scan tests
    $ pytest --cov=corsair_scan --cov-report=html --cov-fail-under=85
    $ bandit . -r
    $ safety check
    ```
    
    All those dependencies are included in requirements_dev.txt. 
    
6. Commit your changes and push your branch to GitHub:

       $ git add .
       $ git commit -m "Your detailed description of your changes."
       $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1.  The pull request should include tests.
2.  If the pull request adds functionality, the docs should be updated.
    Put your new functionality into a function with a docstring, and add
    the feature to the list in README.md.
3.  The pull request should work for Python 3.7 and 3.8
