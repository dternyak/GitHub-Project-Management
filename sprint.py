import sys

import requests

from config import APP_CLIENT_ID, APP_CLIENT_SECRET, GITHUB_API, SPRINT_FILENAME
from util import write_to_file, handle_file_creation

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def kick_off_sprint_plan(repo, org, sprint, output_file=None):
    issues = get_issues_in_milestone(repo, org, sprint)
    filtered_issues = convert_issues_to_canonical_format(issues)
    mapped_issues = get_mappped_issue_by_assignee(filtered_issues)
    if not output_file:
        output_file = SPRINT_FILENAME
    output_issue_plan(mapped_issues, sprint, output_file)


def get_issues_in_milestone(owner, repo, sprint):
    params = {
        'milestone': sprint,
        'client_id': APP_CLIENT_ID,
        'client_secret': APP_CLIENT_SECRET
    }
    endpoint = GITHUB_API + '/repos/{}/{}/issues'.format(owner, repo)
    headers = {'Accept': 'application/vnd.github.cloak-preview'}
    req = requests.get(endpoint, params=params, headers=headers)
    return req.json()


def convert_issues_to_canonical_format(issues):
    return [{
        "title": issue["title"],
        "assignee": issue["assignee"]["login"],
        "url": issue["html_url"]
    } for issue in issues]


def get_mappped_issue_by_assignee(canonical_issues):
    mapped_issues = {}
    for issue in canonical_issues:
        if issue["assignee"] not in mapped_issues:
            mapped_issues[issue["assignee"]] = []
        mapped_issues[issue["assignee"]].append(issue)
    return mapped_issues



def build_buffered_output(output, sprint, mapped_issues):
    message = "Here are the tasks for sprint {}.\n\n".format(sprint)
    output.write(message)

    for dev, issues in mapped_issues.items():
        output.write("*{}*\n".format(dev))
        for issue in issues:
            output.write("{}: ({})\n".format(issue["title"], issue["url"]))
        output.write("\n")

    contents = output.getvalue()
    return contents


def output_issue_plan(mapped_issues, sprint, output_file):
    output = StringIO()
    contents = build_buffered_output(output, sprint, mapped_issues)
    full_output_file_path = handle_file_creation(output_file)
    write_to_file(full_output_file_path, contents)
    output.close()
    sys.stdout.write("Success! Sprint plan has been successfully written to file: /outputs/{} :)\n".format(output_file))
