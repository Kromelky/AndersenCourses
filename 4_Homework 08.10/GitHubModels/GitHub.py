import requests


def removeLastParam(url: str):
    if url.endswith("}"):
        ret_string = url[:url.rindex("{")]
        return ret_string
    return url


class GitHubRepository:

    def __init__(self, json):
        self.name = json["name"]
        self.contrib_url = json["contributors_url"]
        self.labels_url = json["labels_url"]
        self.pulls_url = json["pulls_url"]
        self.contribs = []
        self.labels = []
        self.pulls = []

    def LoadData(self, pages):
        # self.LoadContributors(pages)
        # self.loadLabels(pages)
        self.loadPulls(pages)

    def loadListByPages(self, url, pages, className):
        page = 1
        lst = []
        response = requests.get(f'{url}?per_page={pages}&page={page}')
        if response.status_code != 200:
            print(f"Error loading pages")
        while len(response.json()) > 0:
            print(f"Page={page} ", end='')
            if pages % 10 == 0:
                print()
            lst += [globals()[className](item, self) for item in response.json()]
            response = requests.get(f'{url}?per_page={pages}&page={page}')
            if response.status_code != 200:
                print(f"Error loading pages")
            page += 1
        return lst

    def loadPulls(self, pages):
        pulls_url = removeLastParam(self.pulls_url)
        print(f"Loading pull requests: {pulls_url}")
        self.pulls = self.loadListByPages(pulls_url, pages, 'GitHubPullRequests')

    def loadLabels(self, pages):
        labels_url = removeLastParam(self.labels_url)
        print(f"Loading pull requests: {labels_url}")
        self.labels = self.loadListByPages(labels_url, pages, 'GitHubLabel')

    def LoadContributors(self, pages):
        cuntrib_url = removeLastParam(self.contrib_url)
        print(f"Loading Contributors: {cuntrib_url}")
        self.contribs = self.loadListByPages(cuntrib_url, pages, 'GitHubUsers')

    def addUser(self, json):
        user = GitHubUsers(json, self)
        self.contribs.append(user)
        return user

    def addLabel(self, json):
        label = GitHubLabel(json, self)
        self.labels.append(label)
        return label

    def getPrintMessage(self, shift=1):
        tabs = '\t' * shift
        messages = [f'{tabs}Repo name: {self.name}', f'{tabs}Labels:']
        messages += [f'\t{tabs}{lbl.getPrintMessage(shift + 1)}' for lbl in self.labels]
        messages.append(f'{tabs}PRS:')
        messages += [f'\t{tabs}{pr.getPrintMessage(shift + 1)}' for pr in self.pulls]
        messages.append(f'{tabs}Contibutors:')
        messages += [f'\t{tabs}{usr.getPrintMessage(shift + 1)}' for usr in self.contribs]
        return '\n'.join(messages)

    def printMainReport(self):
        return ""


class GitHubPullRequests:

    def __init__(self, json, repo):
        self.repo = repo
        self.id = json['id']
        self.number = json['number']
        self.state = json['state']
        self.labels = []
        for val in json['labels']:
            ins = True
            for lab in repo.labels:
                if lab.id == val['id']:
                    self.labels.append(lab)
                    ins = False
                    break
            if ins:
                lab = repo.addLabel(val)
                self.labels.append(lab)
        self.user = None
        for user in repo.contribs:
            if user.id == json['user']['id']:
                self.user = user
                break
        if self.user is None:
            self.user = repo.addUser(json['user'])

    def getPrintMessage(self, shift=1):
        tabs = '\t' * shift
        messages = [f'{tabs}PR: {self.number}']
        messages += [f'\t{tabs}{lbl.getPrintMessage(shift + 1)}' for lbl in self.labels]
        messages.append(f'\t{tabs}{self.user.getPrintMessage(shift + 1)}')
        return "\n".join(messages)


class GitHubLabel:

    def __init__(self, json, repo):
        self.repo = repo
        self.id = json['id']
        self.name = json['name']
        self.color = json['color']

    def __eq__(self, other):
        return self.id == other.id

    def getPrintMessage(self, shift=1):
        tabs = '\t' * shift
        return f'{tabs}Label: {self.name}'


class GitHubUsers:

    def __init__(self, json, repo):
        self.repo = repo
        self.id = json['id']
        self.login = json['login']
        self.type = json['type']
        self.totalContributions = 0
        if 'contributions' in json:
            self.totalContributions = json['contributions']

    def __eq__(self, other):
        return self.id == other.id

    def getPrintMessage(self, shift=1):
        tabs = '\t' * shift
        return f'{tabs}User: {self.login}'
