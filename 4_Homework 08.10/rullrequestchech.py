import argparse

import requests
import sys

from GitHubModels.GitHub import GitHubRepository



def getApiPullRequestURLs(url):
    return url.replace("https://", "https://api.").replace("github.com/", "github.com/repos/")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="Pull request statistics ",
                                     usage="Get pull request statistics from github repo")
    # repos: https://github.com/microsoft/vscode
    # https://github.com/iptv-org/iptv
    # https://github.com/SudhanPlayz/Discord-MusicBot
    parser.add_argument('-r', '--repo', help=' Set repository', type=str, default='https://github.com/SudhanPlayz/Discord-MusicBot')
    parser.add_argument('-s', '--state', help=' Set pages state filter', type=str, default='open')
    parser.add_argument('-p', '--pages', help=' Set pages limit', type=int, default=50)
    parser.add_argument('-so', '--sortorder', help=' Set output order values (name, count)', type=str, default='name')
    parser.add_argument('-sd', '--sortdirection', help=' Set output order direction', type=bool, default=True)
    parser.add_argument('-t', '--token', help=' Set authorization token', type=str, default='')

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

    headers = {}

    if args.token != '':
        headers["Authorization"] = f"token {args.token}"

    pullRequestApiUrl = getApiPullRequestURLs(args.repo)

    response = requests.get(pullRequestApiUrl, headers=headers)

    if(response.status_code != 200):
        print(f"Unavailable api {pullRequestApiUrl}")
        sys.exit(-4)

    print(response.json())

    data = response.json()

    repo = GitHubRepository(data)
    repo.LoadData(args.pages, args.state, headers)
    #print(repo.getPrintMessage())
    print(repo.printMainReport(args.sortorder, args.sortdirection))
    input("Press any key to get next report")
    print(repo.printCustomReport(args.sortorder, args.sortdirection))





