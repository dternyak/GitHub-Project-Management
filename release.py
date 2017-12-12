import sys
from operator import itemgetter

import requests

from config import APP_CLIENT_ID, APP_CLIENT_SECRET, GITHUB_API, PRS_FILENAME
from util import write_to_file, handle_file_creation, buffer_list_of_dicts

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def get_author_name(commit):
    # error checking due to github's behavior for marketplace bots like greenkeeper using different formats
    try:
        author_name = commit["author"]["login"]
    except TypeError:
        author_name = "?"
    return author_name


def is_valid_commit_message(commit):
    commit_message = commit["commit"]["message"]
    blacklisted_strings = ["Merge pull request", "chore", "fix(package)"]
    is_valid = True
    for each in blacklisted_strings:
        if each in commit_message:
            is_valid = False
            break
    return is_valid


def get_formatted_info_about_commit(commit):
    formatted_data = {
        "message": commit["commit"]["message"],
        "author": commit["commit"]["author"]["name"],
        "date": commit["commit"]["author"]["date"]
    }
    return formatted_data


def accumulate_commits(commits, filtered_commits, since_sha):
    found_since_sha = False
    for commit in commits:
        if since_sha in commit["sha"]:
            found_since_sha = True
            break
        else:
            filtered_commits.append(commit)
    return [found_since_sha, filtered_commits]


def get_commits_since_sha(owner, repo, branch, since_sha):
    found_since_sha = False
    page = 1
    filtered_commits = []
    while not found_since_sha:
        commits = get_commits_on_branch(owner, repo, branch, page)
        if not commits:
            raise ValueError('Unable to find SHA {}'.format(since_sha))
        found_since_sha, filtered_commits = accumulate_commits(commits, filtered_commits, since_sha)
        page += 1
    return filtered_commits


def get_formatted_commits_since_sha(owner, repo, branch, since_sha):
    commits_since_sha = get_commits_since_sha(owner, repo, branch, since_sha)
    return [
        get_formatted_info_about_commit(commit) for commit in commits_since_sha if is_valid_commit_message(commit)
    ]


def get_commits_on_branch(owner, repo, branch, page, limit=200):
    params = {
        'client_id': APP_CLIENT_ID,
        'client_secret': APP_CLIENT_SECRET
    }
    endpoint = GITHUB_API + '/repos/{}/{}/commits?sha={}&limit={}&page={}'.format(owner, repo, branch, limit, page)
    headers = {'Accept': 'application/vnd.github.cloak-preview'}
    req = requests.get(endpoint, params=params, headers=headers)
    return req.json()


def handle_output(since_sha, sorted_formatted_commits, output_file):
    if not output_file:
        output_file = PRS_FILENAME
    output = StringIO()
    output.write('---------------------------------------\n')
    output.write("Showing commits merged into develop after: {}\n".format(since_sha))
    output.write('---------------------------------------\n')
    output.write("Total Merged PRs: {}\n".format(len(sorted_formatted_commits)))
    output.write('---------------------------------------\n')
    buffer_list_of_dicts(output, sorted_formatted_commits)
    contents = output.getvalue()

    full_output_file_path = handle_file_creation(output_file)
    write_to_file(full_output_file_path, contents)
    sys.stdout.write(
        "Success! Release review has been successfully written to file: /outputs/{} :)\n".format(output_file)
    )

    output.close()


def strip_t_from_commit(commit):
    commit["date"] = commit["date"].split('T')[0]
    return commit


def strip_t_from_commits(commits):
    return list(map(strip_t_from_commit, commits))


def kick_off_release_review(owner, repo, branch, since_sha, output_file):
    formatted_commits = get_formatted_commits_since_sha(owner, repo, branch, since_sha)
    sorted_formatted_commits = sorted(formatted_commits, key=itemgetter('date'), reverse=False)
    stripped_formatted_commits = strip_t_from_commits(sorted_formatted_commits)
    handle_output(since_sha, stripped_formatted_commits, output_file)
