import argparse

import requests
import sys

from GitHubModels.GitHub import GitHubRepository



def getApiPullRequestURLs(url):
    return url.replace("https://", "https://api.").replace("github.com/", "github.com/repos/")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="Pull request statistics ",
                                     usage="Get pull request statistics from github repo")
    parser.add_argument('-r', '--repo', help=' Set repository', type=str, default='https://github.com/trekhleb/javascript-algorithms')
    parser.add_argument('-s', '--state', help=' Set pages state filter', type=str, default='open')
    parser.add_argument('-p', '--pages', help=' Set pages limit', type=int, default=500)

    args = parser.parse_args()

    if not args.repo:
        print(f"Repo is undefined")
        sys.exit(-1)

    if requests.get(args.repo).status_code != 200:
        print(f"Repo is unavailable, closed or doesn't exists")
        sys.exit(-1)

    if args.pages < 1:
        print(f"Pages number should be more then 1")
        sys.exit(-3)

    pullRequestApiUrl = getApiPullRequestURLs(args.repo)

    response = requests.get(pullRequestApiUrl)

    if(response.status_code != 200):
        print(f"Unavailable api {pullRequestApiUrl}")
        sys.exit(-4)

    print(response.json())

    data = response.json()

    repo = GitHubRepository(data)
    repo.loadPulls(args.pages)
    repo.loadLabels(args.pages)
    repo.LoadContributors(args.pages)

    print('123')




