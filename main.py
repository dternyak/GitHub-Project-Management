import sys

import click

from release import kick_off_release_review
from sprint import kick_off_sprint_plan


@click.command()
@click.option('--repo')
@click.option('--org')
@click.option('--sprint', required=False)
@click.option('--branch', required=False)
@click.option('--since-sha', required=False)
@click.option('--utility', '-u', type=click.Choice(['sprint', 'release']), multiple=False, required=True)
@click.option('--output-file', required=False)
def kick_off(repo, org, sprint, branch, since_sha, utility, output_file):
    if utility == 'sprint':
        if not sprint:
            sys.stderr.write("--sprint argument is required when using the sprint utility!\n")
        else:
            kick_off_sprint_plan(repo, org, sprint, output_file)

    elif utility == "release":
        kick_off_release_review(repo, org, branch, since_sha, output_file)


if __name__ == '__main__':
    kick_off()
