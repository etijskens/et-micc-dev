# -*- coding: utf-8 -*-
"""Command line interface publish (no sub-commands)."""
import os
import sys
import subprocess
from contextlib import contextmanager
from types import SimpleNamespace
from pathlib import Path

import click
import pygit2

from et_micc.project import Project
try:
    from __version__ import __version__ as et_micc_dev_version
except:
    et_micc_dev_version = "version unknown"

@contextmanager
def in_directory(path):
    """Context manager for changing the current working directory while the body of the
    context manager executes.
    """
    previous_dir = os.getcwd()
    os.chdir(str(path)) # the str method takes care of when path is a Path object
    yield os.getcwd()
    os.chdir(previous_dir)


def is_repo_clean(repo):
    """
    :param str repo: path to project directory containing .git.
    :returns: True of False
    """
    click.echo("\nVerifying that git repo " + click.style(f"[{repo}]",fg='cyan') + " is clean ...")
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
    
    
def execute(cmd, env=None, cwd=None, input_=None):
    """Executes a list of OS commands.
    
    :param list cmds: an OS command (=list of str) 
    :returns int: return code of first failing command, or 0 if all
        commanbds succeed.
    """
    click.echo(click.style(f"\n[{cwd}]", fg='cyan') + f" > {' '.join(cmd)}")
    completed_process = subprocess.run(cmd, capture_output=True, env=env, cwd=cwd, input=input_)
    if completed_process.returncode:
        fg = 'bright_red'
    else:
        fg = 'green'
        
    if completed_process.stdout:
        click.secho('(stdout)\n' + completed_process.stdout.decode('utf-8'), fg=fg)
    if (completed_process.returncode==0 and 
        completed_process.stderr
    ):
        click.secho(' (stderr)\n' + completed_process.stderr.decode('utf-8'), fg=fg)
    if completed_process.returncode:
#         click.secho(f"Exit code = {completed_process.returncode}", fg=fg)
        return completed_process.returncode
    return 0


# def commit_version(repo,new_version):
#     """
#     :param str repo: path to project directory containing .git.
#     :returns: True of False
#     """
#     author = pygit2.Signature('Engelbert Tijskens', 'engelbert.tijskens@uantwerpen.be')
# 
#     repo = pygit2.Repository(repo)
#     tree = repo.TreeBuilder().write()
#     repo.create_commit(
#         "refs/heads/master", # the name of the reference to update
#         author, author, f"Publishing v{new_version}.",
#         tree, # binary string representing the tree object ID
#         [] # list of binary strings representing parents of the new commit
#     )
    
    
@click.command()
@click.option( '-r', '--rule'
             , help="semver rule"
             , default='patch'
             )
@click.option( '--dry-run'
             , help="bumpversion --dry-run"
             , default=False, is_flag=True
             )
@click.version_option(version=et_micc_dev_version)
def main(rule,dry_run):
    """CLI to publish et-micc and et-micc-build in an orderly manner."""
    
    if 0==is_repo_clean("../et-micc"):
        return 1
    
    if not is_repo_clean("../et-micc-build"):
        return 1

    if not rule:
        click.secho("[Error]\nNo rule specified.",fg='bright_red')
        return 1
    
    options_micc = SimpleNamespace(
        project_path=Path('../et-micc').resolve(),
        rule = rule,
        dry_run = dry_run,
        verbosity = 1,
        clear_log = False,
    )
    options_micc_build = SimpleNamespace(
        project_path=Path('../et-micc-build').resolve(),
        rule = rule,
        dry_run = dry_run,
        verbosity = 1,
        clear_log = False,
    )
    project_micc       = Project(options_micc)
    project_micc_build = Project(options_micc_build)
    project_micc      .version_cmd()
    project_micc_build.version_cmd()
    # update the dependency:
    print(project_micc.version)
    if not dry_run:
        project_micc_build.pyproject_toml['tool']['poetry']['dependencies']['et-micc'] = project_micc.version
        project_micc_build.pyproject_toml.save()
    else:
        return 0

    click.echo("\nPublishing ....")
    n_issues = 0
    
    exit_code1 = execute(['poetry', 'publish', '--build'], cwd="../et-micc"      , input_=b'y\n')
    if exit_code1:
        n_issues += 1
    
    exit_code2 = execute(['poetry', 'publish', '--build'], cwd="../et-micc-build", input_=b'y\n')
    if exit_code2:
        n_issues += 1

    if n_issues:
        click.secho(f"\nFix {n_issues} publishing issues and run this command again.",fg='bright_red')
    else:
        click.secho("\n-*# SUCCESS #*-",fg='green')

    return n_issues
    
#     commit=True
#     if commit:
#         commit_version("../et-micc",project_micc.version)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
#eof
