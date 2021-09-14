import argparse
import requests
import sys

def getApiPullRequestURL(url):
    return '123'



if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="Pull request statistics ",
                                     usage="Get pull request statistics")
    parser.add_argument('-r', '--repo', help=' Set repository', type=str, default='https://github.com/Kromelky/AndersenCourses')

    args = parser.parse_args()

    if not args.repo:
        print(f"Repo is undefined")
        sys.exit(-1)


    pullRequestApiUrl = getApiPullRequestURL()


