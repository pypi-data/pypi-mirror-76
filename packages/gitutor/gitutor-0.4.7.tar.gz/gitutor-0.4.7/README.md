# Gitutor

Welcome to Gitutor. This tool is meant to get you up and running using git
in the shortest time possible while learning on the go.

Gitutor is a command line application that wraps git and provides beginner 
friendly versions of git's commands. It makes git easy. 

In this tutorial you'll learn how tu use git with the aid of gitutor. Once 
you feel comfortable using git this way, read what is going on behind gitutor's
commands on the last chapters.

The command line includes a summarized version of this tutorial so you'll always
have it at hand. To access it run: 

    $ gt lesson 

Whenever you execute a comand read it's output, it has useful information.

## Available commands

1. gt init - Initialize your local and remote repository.
2. gt save - Save you changes in the local and remote repository.
3. gt goback - Return to a previous commit.
4. gt compare - Compare the current state with a previous commit.
5. gt ignore - Make git ignore selected files.

## Installation guide

In order to use gitutor without any dependencies version conflicts we recommend installing it using pipx.

Pipx creates a virtual environment for your package and exposes its entry point so you can run gitutor from anywhere. Install pipx and make sure the $PATH is correctly configured

    $ python3 -m pip install --user pipx
    $ pipx ensurepath

Once pipx is installed, run the following to install gitutor

    $ pipx install gitutor

And to upgrade gitutor to its latest version you only need to run

    $ pipx upgrade gitutor

## Additional notes

Before using gitutor you need to have git available in your computer. You can check the installation guide [here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

It's also recommended to store your GitHub credentials so you won't have to authenticate everytime you realize a push or pull. You can do this by running

    $ git config --global credential.helper store

This will store your credentials in a plain-text file (.git-gredentials) under your project directory. If you don't like this you can use any of the following approaches:

On Mac OS X you can use its native keystore with

    $ git config --global credential.helper oskeychain

For Windows you can install a helper called [Git Credential Manager for Windows](https://github.com/Microsoft/Git-Credential-Manager-for-Windows) and then run

    $ git config --global credential.helper manager