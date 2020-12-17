# Releasing

Our approach to releasing new versions is quite simple. A new version will be released everytime there's a push to master branch. 

We've managed to have all the process to bump version for next release in the different files fully automated by using [github actions](https://github.com/features/actions). 

We currently have 2 github actions configured in this repo, which will be triggered when:

* There's a pull request.
    * If the PR is to a non master branch, this action will run standard checks like nosetests, flake8, bandit and safety to ensure everything is good with the code.
    * If the PR is to the master branch, this action will run standard checks, automatically bump release version number in appropriate files and commit those changes to the pull request branch.
* There are changes pushed to master branch.
    * This action will run standard checks, create the wheel, the release/tag using the version previously bumped and publish the artefact to Pypi

To bump version in files prior to release, we use [bump2version](https://github.com/c4urself/bump2version). The configuration for it to know what is the current version, what files need to have the version bumped up and what is the next version is in `setup.cfg`. 

```ini
[bumpversion]
current_version = 1.2.2
commit = True
tag = False
new_version = 2.0.0

[bumpversion:file:setup.py]
search = version='{current_version}'
replace = version='{new_version}'

[bumpversion:file:setup.cfg]
search = current_version = '{current_version}'
replace = current_version = '{new_version}'

[bumpversion:file:corsair_scan/corsair_scan.py]
search = __version__ = '{current_version}'
replace = __version__ = '{new_version}'

...
```

With this configuration, we are specifying that only those three files need to have the version bumped before release. By default, `bump2version` bumps a minor version (ie . from 1.2.2 to 1.3.0), but if we want it to be a major version or a patch bump, we only need to specify the `new_version` attribute in the configuration with the version we want to use for the release. 

**Note**: Master and develop branches are protected. It means that we require commits to be pushed through pull requests, status checks to pass before merging and restrict who can push to those branches. We aimed to have the release process fully automated, but because issues described [here](https://github.community/t5/GitHub-Actions/How-to-push-to-protected-branches-in-a-GitHub-Action/td-p/29609) or [here](https://github.community/t5/GitHub-Actions/Automatic-version-update-in-protected-branch/m-p/56469#M9895) when using github actions for this, we decided that disabling this protection in **develop** branch just when a PR from develop to master is submitted would be a good approach for us, so that the action that bumps the versions and commits the changes back can complete successfuly. 
