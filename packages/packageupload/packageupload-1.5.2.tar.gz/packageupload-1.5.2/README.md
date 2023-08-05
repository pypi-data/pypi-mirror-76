# PackageUpload
 
 ### **The most easy way to upload your packages to PyPI!**
 
 [![PyPI version](https://badge.fury.io/py/packageupload.svg)](https://pypi.org/project/packageupload/)
 [![PyPI - Downloads](https://img.shields.io/pypi/dm/packageupload)](https://pypistats.org/packages/packageupload)
 [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/packageupload)](https://pypi.org/project/packageupload/)
 [![PyPI - Status](https://img.shields.io/pypi/status/packageupload)](https://pypi.org/project/packageupload/)
 [![GitHub - License](https://img.shields.io/github/license/Animenosekai/packageupload)](https://github.com/Animenosekai/packageupload/blob/master/LICENSE)
 [![GitHub issues](https://img.shields.io/github/issues-raw/Animenosekai/packageupload)](https://github.com/Animenosekai/packageupload/issues)
 [![GitHub top language](https://img.shields.io/github/languages/top/Animenosekai/packageupload)](https://github.com/Animenosekai/packageupload)

## Table of Content
- [Installation](#installation)  
- [What is PackageUpload?](#whatis)
- [Usage](#usage)
- [Development](#development) 
- [Legals](#legals)
 
 
<a name="installation"/>

## Installation
You can install this library with **`PIP`**, the Python Package Manager

Simply type `pip install packageupload` in your terminal/command-line prompt.

> This library has four third-pary dependencies installed automatically with `pip install packageupload`.

<a name="whatis"/>

## What is PackageUpload?
It is a simple python script that will help you upload your packages on PyPI (because it's boring to build setup.py and upload it manually)

> You just have to launch `packageupload` from your command-prompt/terminal!


<a name="usage"/>

## Usage

---

### PREREQUISITE

**You first need to create a repository for your package on GitHub and to upload it to GitHub.**

**Then you need to create a release for this repository.**

**You also need a PyPI account (obviously)**

---

### Instructions

#### Open the package directory in your command-prompt (or `cd`to it).

#### Run `packageupload`

---

### Options

#### Usage

- `packageupload <option1> <option2>`

#### Available Options

- `nocleanup`: To leave everything without cleaning up the directory to its first state.

- `keepsetup`: To leave the setup.py file (not needed if nocleanup)

- `customclassifiers`: To add custom classifiers to your setup file

- `customurl`: To add a the website URL for the package (if you want something other than the GitHub Repository)

- `customsetup`: If you want to customize your setup with other sections (i.e. entry_points, ...)

---

### Functions

- **`start(keepsetup, nocleanup, customclassifiers, customurl)`**

**It will guide you and help you upload your packages on PyPI**

Arguments:

    cleanup (optional, default: True): Wether you want to clean and keep the directory as if nothing happened after uploading the package to PyPI (> bool)

    keepsetup (optional, default: False): Wether you want to keep setup.py after the upload is done or not (not needed if cleanup = False). (> bool)

    customclassifiers (optional, default: True): Wether you want to add custom classifiers or not. (> bool)

    customurl (optional, default: False): Wether you have a website other than the GitHub repo for the package and that you to add it. (> bool)

    upgrade (optional, default: False): If True, it will not check the availability of the name.


> Returns 0 if everything is fine and uploaded correctly to PyPI

> Returns 1 if an error occured while cleaning the package directory

> Returns 2 if an error occured while uploading the package.

> Returns 3 if an error occured while building the package.

> Returns 4 if an error occured while verifying the module/packaging the module.

> Returns 5 if an error occured while creating the setup file.

> Returns 6 if you aborted.

> Returns 7 if an error occured while downloading the package with `pip`

---
- **`setup(customurl)`**

**Creates a setup.py file.**

Arguments:

    customurl (optional, default: False): Wether you have a website other than the GitHub repo for the package and that you to add it. (> bool).

    upgrade (optional, default: False): If True, it will not check the availability of the name.
    
> Returns 0 if success 1 if failed (> integer)

---
- **`module_verification()`**

**To package the module and its files.**

Arguments:

    there is no argument to pass.

> Returns 0 if success, 1 if failed (> integer)

---
- **`build()`**

**To build the package.**

Arguments:

    there is no argument to pass.

> Returns 0 if success, 1 if failed (> integer)

---
- **`upload()`**

**To upload a built package to PyPI.**

Arguments:

    there is no argument to pass.

> Returns 0 if success, 1 if failed (> integer)

---
- **`clean(keepsetup)`**

**Cleans the package directory.**

Arguments:

    keepsetup (optional, default: False): Wether you want to keep setup.py or not. (> bool)

> Returns 0 if success, 1 if failed (> integer)

---
- **`download()`**

**Installs the package using `pip`.**

Arguments:

    there is no argument to pass.

> Returns 0 if success, 1 if failed (> integer)

---

<a name="development"/>

## Development
PackageUpload is in constant development and fixes are made on a regular basis (but I also try to add some new features ehe)

#### If you have any issues, questions, development problem: feel free to ask in the issues section.

If you want to help us and join me here is a quick guide.

### Files
`__init.py__` is the main module

`README.md` is the text file you're currently reading, with all the documentations and explanations.

`LICENSE` is a text file with File Center's license

#### Dependencies
The File Center Library has four third-party dependencies.

- `twine`
- `setuptools`
- `filecenter`
- `lifeeasy`

*(`filecenter`and `lifeeasy` are both written by me)*

SetupTools is used to make build the package.

Twine is used to safely upload the package.

FileCenter is used to check files.

LifeEasy is used to make my life easier.

<a name="legals"/>

## Copyrights and Legals

**If you think that there is any kind of copyright infrigements, feel free to ask me to remove it and I will try to do so as soon as possible**

**GitHub** is a brand which belongs to GitHub, Inc. (Microsoft)

**Python** belongs to the Python Software Foundation


> ©Anime no Sekai - 2020 ✨
