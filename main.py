import json
import sys
import requests


def to_json(json_object, file_path):
    file_path += '.json'
    with open(file_path, 'w') as outfile:
        json.dump(json_object, outfile)


def get_next_url(link_header):
    if link_header:
        links = link_header.split(', ')
        for link in links:
            if 'rel="next"' in link:
                return link[link.index('<') + 1:link.index('>')]  # Extract the URL
    return None


def retrieve_issues_sync(repo_owner, repo_name):

    # The endpoint uses pagination when serving issues with the default page length set to 30.
    # We will set it to the max (100) and make subsequent requests if needed until we get all the issues
    #   using the 'Link' header.

    issues = []
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues?milestone=*&state=all&assignee=*&per_page=30"
    while url is not None:
        response = requests.get(url)

        match response.status_code:
            case 200:
                issues.extend(response.json())
                link_header = response.headers.get("Link")
                url = get_next_url(link_header)
            case 404:
                url = None
                print(f"""Repository {repo_owner}/{repo_name} not found""")
            case _:
                url = None
                print(f"""Couldn't retrieve issues for repository {repo_owner}/{repo_name}
                            \rStatus code: {response.status_code}
                            \rReason: {response.reason}\n""")
    if len(issues) != 0:
        to_json(issues, f"issues_{repo_owner}_{repo_name}")
        print(f"""Successfully retrieved {len(issues)} issues for repository {repo_owner}/{repo_name}
                                    \rSee issues data in issues_{repo_owner}_{repo_name}""")


if __name__ == "__main__":
    # Must use Python 3.10 or higher
    if sys.version_info < (3, 10):
        raise Exception("Must use Python 3.10 or higher")

    retrieve_issues_sync(sys.argv[1], sys.argv[2])