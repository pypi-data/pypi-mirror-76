import os
import git
import click
import requests
from datetime import datetime

from goBack.commands import goBack
from init.commands import init
from save.commands import save
from ignore.commands import ignore
from compare.commands import compare
from lesson.commands import lesson

def run_config(command):
    api_endpoint = 'https://firestore.googleapis.com/v1/projects/gitutor/databases/(default)/documents/metrics/'

    path = os.path.dirname(__file__)
    config_file = path + '/.gitutor_config'

    with open(config_file, 'r') as _:
        flag = int(_.read())

    if flag == 1:
        fields = {
            "fields": {
                "command": {"stringValue": command},
                "date": {"timestampValue": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}
            }
        }

        response = requests.post(api_endpoint, json = fields)

        with open(config_file, 'w') as _:
            _.write('0')


class CustomGroup(click.Group):
    def invoke(self, ctx):
        ctx.obj['args'] = tuple(ctx.args)
        super(CustomGroup, self).invoke(ctx)

@click.group(cls=CustomGroup)
@click.pass_context
def cli(ctx):
    """ 
    Git the easy way.

    If you want to access gitutor tutorials run 

        $ gt lesson

    Any issues, questions or bugs you can reach us at support@gitutor.io
    """
    #Check ctx was initialized
    ctx.ensure_object(dict)

    run_config(ctx.invoked_subcommand)
    
    if ('--help' not in ctx.obj['args']) and (ctx.invoked_subcommand != 'init') and ctx.invoked_subcommand != 'lesson':
        try:
            repo = git.Repo(".", search_parent_directories=True)
            ctx.obj['REPO'] = repo
            #print( f"Location {repo.working_tree_dir}" )
            #print(f"Remote from init: {repo.remote('origin').url} ")
        except Exception as e:
            click.echo('Ups! You\'re not inside a git repo')
            #print("not git repo")
            exit()

cli.add_command(init)
cli.add_command(goBack)
cli.add_command(save)
cli.add_command(ignore)
cli.add_command(compare)
cli.add_command(lesson)

def main():
    cli(obj={})

if __name__ == '__main__':
    cli(obj={})
