import requests


def removeLastParam(url: str, pages):
    if url.endswith("}"):
        ret_string = f'{url[:url.rindex("{")]}?per_mage={pages}'
        return ret_string
    return f'{url}?per_mage={pages}'


class GitHubRepository:

    def __init__(self, json):
        self.name = json["name"]
        self.contrib_url = json["contributors_url"]
        self.labels_url = json["labels_url"]
        self.pulls_url = json["pulls_url"]
        self.contribs = []
        self.labels = []
        self.pulls = []

    def loadPulls(self, pages):
        pulls_url = removeLastParam(self.pulls_url, pages)
        print(f"Loading pull requests: {pulls_url}")
        response = requests.get(pulls_url)
        self.labels = [GitHubLabels(item, self) for item in response.json()]
        return

    def loadLabels(self, pages):
        labels_url = removeLastParam(self.labels_url, pages)
        print(f"Loading pull requests: {labels_url}")
        response = requests.get(labels_url)
        if response.status_code != 200:
            print(f"Error loading labels")
        self.labels = [GitHubPullRequests(item, self) for item in response.json()]

    def LoadContributors(self, pages):
        cuntrib_url = removeLastParam(self.contrib_url, pages)
        print(f"Loading Contributors: {cuntrib_url}")
        response = requests.get(cuntrib_url)
        if response.status_code != 200:
            print(f"Error loading Contributors")
        self.labels = [GitHubUsers(item, self) for item in response.json()]
        pass

    def addUser(self, json):
        user = GitHubUsers(json)
        self.contribs.append(user)
        return user

    def printMainReport(self):
        return ""



class GitHubPullRequests:

    def __init__(self, json, repo):
        self.repo = repo
        self.id = json['id']
        self.number = json['number']
        self.state = json['state']
        self.labels = [lab for lab in repo.labels if lab in json['labels']]
        for user in repo.contribs:
            if user.id == json['user']['id']:
                self.user = user
        if self.user is None:
            self.user = repo.addUser(json['user'])


class GitHubLabels:

    def __init__(self, json, repo):
        self.repo = repo
        self.id = json['id']
        self.name = json['name']
        self.color = json['color']

    def __contains__(self, item):
        return item.id


class GitHubUsers:

    def __init__(self, json, repo):
        self.repo = repo
        self.id = json['id']
        self.login = json['login']
        self.type = json['type']
        self.totalContributions = json['contributions']