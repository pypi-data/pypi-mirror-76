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

A version control system is a tool that saves checkpoints (called commits) of
a file or a set of files over time. A collection of files tracked by git is
called a repository (or repo).

Git is distributed because it's possible to have copies of a repository on
different machines in which checkpoints are saved independently.
Github is a service for storing repositories that act as a source of truth.

On the next lesson you'll learn the basic workflows for git
Gitutor provides beginner friendly commands that wrap git.
Start by using the simple commands.
On the extended tutorial you'll be shown what happens behind the scenes and
what are the actual git commands being used.
'''
    },
    'Single user workflow': {
        'description': 'One person works on the repo',
        'content': '''\
The first and simplest workflow is a single person working on the repository.

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
    'Multiple users workflow': {
        'description': 'Multiple people on the repo',
        'content': '''\
The simplest workflow for colaboration is the following:

1.  Initialize a repository as shown in Single User Workflow
    or download a copy of a repo with the url from the repo's github page
    with the following git command:

    $git clone url-of-github-repo

    For example:

    $git clone https://github.com/artemisa-mx/demoRepository.git

2. Grant or ask for write permisions to the github repo

3. Work on your project

4. Create checkpoint to save changes.

    $gt save

5.  If no conflict occurs go to step 3.

6.  If a merge conflict occurs, gitutor will output the names of the
    conflicted files. Solve the conflicts and then create a checkpoint to save
    the conflict resolution:

    $gt save

    Repeat from step 3

    Else, if you don't want to resolve the conflict right away, abort:

    $gt save --abort-merge

    Your checkpoint will only be saved locally.

When creating a checkpoint on step 4, you can alteratively use:

    $gt save -l

This will save the checkpoint only on your local machine and wont download
changes from github, avoiding any conflict. When you are ready to sync your
local and remote repo use the command without the -l flag.


Learn how to grant write permisions and how to resolve conflicts on the
extended version of the lesson : https://gitutor.io/guide/one-branch.html
'''

    },
}
