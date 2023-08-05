welcome_message ='''\
Here is a list of short lessons to get you going. You can read
the extended version of this tutorial on https://gitutor.io/guide/
'''
lessons = {
    'Introduction': {
        'description': 'Learn the basic concepts',
        'content': '''\
The basic concepts of git:

Git is a free and open source distributed version control system

A version control system is a tool that saves checkpoints (called commits) of a file or a set of files over time. 
A collection of files tracked by git is called a repository (or repo).

Git is distributed because it's possible to have copies of a repository on different machines in which checkpoints 
are saved independently. Github is a service for storing repositories that act as a source of truth.

On the next lesson you'll learn the basic workflows for git 
Gitutor provides beginner friendly commands that wrap git. 
Start by using the simple commands. 
On the extended tutorial you'll be shown what happens behind the scenes and what are the actual git commands being used.
'''
    },
    'First workflow': {
        'description': 'One person works on the repo',
        'content': '''\
The first and most simple workflow is a single person working on the repository.

1. Change directory into the root folder of your project
 
    $cd myProject

2. Initialize your project's folder as a git repo 

    $gt init

3. Work on your project

4. Create checkpoint to save your changes 
 
    $gt save

Repeat from step 3.

Extended lesson: https://gitutor.io/guide/one-branch.html
''' 

    },
}