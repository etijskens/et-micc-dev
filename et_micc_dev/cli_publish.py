# -*- coding: utf-8 -*-
"""Command line interface publish (no sub-commands)."""

import sys

import click
import pygit2
from bumpversion.cli import main as bumpversion
from bumpversion.exceptions import WorkingDirectoryIsDirtyException

def is_repo_clean(repo):
    """
    :param str repo: path to project directory containing .git.
    :returns: True of False
    """
    click.echo("\nVerifying that git repo " + click.style(f"[{repo}]",fg='green') + " is clean ...")
    repo = pygit2.Repository(repo)
    status = repo.status()
    for filepath, flags in status.items():
        wt_column = ' '
        index_column = ' '
        untracked_column = ' '
        if flags & pygit2.GIT_STATUS_WT_NEW:
            untracked_column = 'U'
        else:
            if flags & pygit2.GIT_STATUS_WT_MODIFIED:
                wt_column = 'M'
    
            if flags & pygit2.GIT_STATUS_WT_DELETED:
                wt_column = 'D'
    
            if flags & (
                  pygit2.GIT_STATUS_INDEX_NEW
                | pygit2.GIT_STATUS_INDEX_MODIFIED
                | pygit2.GIT_STATUS_INDEX_DELETED
            ):
                index_column = 'I'
        msg = wt_column + index_column + untracked_column
        counter = 0
        if msg!='   ':
            click.echo(click.style(msg,fg='bright_red') + ' ' + filepath)
            counter += 1
        if counter:
            click.secho(f"There are {counter} issues!"              ,fg='bright_red')
            click.secho("Fix the issues and run this command again.",fg='bright_red')
            return False
        
    click.secho("There are 0 issues.\n",fg='green')
    return True
    
    
@click.command()
@click.option('-v', '--verbosity', count=True
             , help="The verbosity of the program."
             , default=1
             )
def main(verbosity):
    """CLI to publish et-micc and et-micc-build in an orderly manner."""
    
    if 0==is_repo_clean("../et-micc"):
        return 1
    
    if not is_repo_clean("../et-micc-build"):
        return 1

    try:
        click.echo("\nVerifying that git repo " + click.style("[et-micc-dev]",fg='green') + " is clean ...")
        bumpversion(['--verbose', '--config-file','.bumpversion.cfg','patch','--dry-run'])
    except WorkingDirectoryIsDirtyException as e:
        print(e)
        click.echo(click.style("Git repo "         ,fg='bright_red') + 
                   click.style("[et-micc-dev] "    ,fg='green') + 
                   click.style("must be clean too.",fg='bright_red')
        )
        click.secho("Fix the issues and run this command again.",fg='bright_red')
        return 1
        
    click.secho("-*# SUCCESS #*-",fg='green')
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
#eof
