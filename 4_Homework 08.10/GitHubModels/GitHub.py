import datetime

import requests

from datetime import datetime


def removeLastParam(url: str):
    if url.endswith("}"):
        ret_string = url[:url.rindex("{")]
        return ret_string
    return url


def getUnlabeledDict():
    return {'id': 0, 'name': 'Unlabeled', 'color': 'ffffff'}


class GitHubRepository:

    def __init__(self, json):
        self.name = json["name"]
        self.contrib_url = json["contributors_url"]
        self.labels_url = json["labels_url"]
        self.pulls_url = json["pulls_url"]
        self.comment_url = json["comments_url"]
        self.contribs = []
        self.labels = [GitHubLabel(getUnlabeledDict(), self)]
        self.pulls = []

    def LoadData(self, pages, state, headers):
        # self.loadLabels(pages, state, headers)
        # self.LoadContributors(pages, state, headers)
        self.loadPulls(pages, state, headers)

    def loadListByPages(self, url, pages, className, state, headers):
        page = 1
        lst = []
        geturl = f'{url}?per_page={pages}&page={page}&state={state}'

        response = requests.get(geturl, headers=headers)
        if response.status_code != 200:
            print(f"Error loading pages")
        while len(response.json()) > 0:
            print(f"Page={page} ", end='\r')
            page += 1
            lst += [globals()[className](item, self) for item in response.json()]
            geturl = f'{url}?per_page={pages}&page={page}&state={state}'

            response = requests.get(geturl, headers=headers)
            if response.status_code != 200:
                print(f"Error loading pages")
                break
        return lst

    def loadPulls(self, pages, state, headers):
        pulls_url = removeLastParam(self.pulls_url)
        print(f"Loading pull requests: {pulls_url}")
        self.pulls = self.loadListByPages(pulls_url, pages, 'GitHubPullRequests', state, headers)

    def loadLabels(self, pages, state, headers):
        labels_url = removeLastParam(self.labels_url)
        print(f"Loading pull requests: {labels_url}")
        self.labels = self.loadListByPages(labels_url, pages, 'GitHubLabel', state, headers)

    def LoadContributors(self, pages, state, headers):
        cuntrib_url = removeLastParam(self.contrib_url)
        print(f"Loading Contributors: {cuntrib_url}")
        self.contribs = self.loadListByPages(cuntrib_url, pages, 'GitHubUsers', state, headers)

    def addUser(self, json):
        user = GitHubUsers(json, self)
        self.contribs.append(user)
        return user

    def addLabel(self, json):
        label = GitHubLabel(json, self)
        self.labels.append(label)
        return label

    def getPrintMessage(self, shift=0):
        tabs = '\t' * shift
        messages = [f'{tabs}Repo name: {self.name}', f'{tabs}Labels:']
        messages += [f'{tabs}{lbl.getPrintMessage(shift + 1)}' for lbl in self.labels]
        messages.append(f'{tabs}PRS:')
        messages += [f'{tabs}{pr.getPrintMessage(shift + 1)}' for pr in self.pulls]
        messages.append(f'{tabs}Contibutors:')
        messages += [f'{tabs}{usr.getPrintMessage(shift + 1)}' for usr in self.contribs]
        return '\n'.join(messages)

    def printMainReport(self, order, revers):
        messages = [f"{'Users'.ljust(30)}{'PrCount'.ljust(20)}"]
        if order == 'name':
            self.contribs.sort(key=lambda x: x.login, reverse=revers)
        elif order == 'count':
            self.contribs.sort(key=lambda x: len(x.pr), reverse=revers)
        labelheader = ''
        for Label in self.labels:
            labelheader += f'{Label.name.ljust(20)}'
        messages[0] += labelheader
        for usr in self.contribs:
            row = f"{usr.login.ljust(30)}{str(len(usr.pr)).ljust(20)}"
            for Label in self.labels:
                row += f'{str(len([x for x in usr.pr if Label in x.labels])).ljust(20)}'
            messages.append(row)
        return "\n".join(messages)

    def printCustomReport(self, order, revers):
        now = datetime.now()
        messages = ["Time of unclosed PR", f"{'Users'.ljust(30)}{'Unclosed time'.ljust(20)}"]
        if order == 'name':
            self.contribs.sort(key=lambda x: x.login, reverse=revers)
        elif order == 'count':
            self.contribs.sort(key=lambda x: min([now] + [node.created_at for node in x.pr if node.state == "open"]),
                               reverse=revers)

        for usr in self.contribs:
            for pr in list(filter(lambda x: (x.state == 'open'), usr.pr)):
                datediff = str(now - pr.created_at)
                row = f"{pr.user.login.ljust(30)}{datediff[:datediff.rindex('.')].ljust(20)}"
                messages.append(row)
        return "\n".join(messages)


class GitHubPullRequests:

    def __init__(self, json, repo):
        self.repo = repo
        self.id = json['id']
        self.number = json['number']
        self.state = json['state']
        self.created_at = datetime.strptime(json["created_at"], "%Y-%m-%dT%XZ")
        self.labels = []
        if len(json['labels']) > 0:
            for val in json['labels']:
                ins = True
                for lab in repo.labels:
                    if lab.id == val['id']:
                        self.labels.append(lab)
                        lab.pr.append(self)
                        ins = False
                        break
                if ins:
                    lab = repo.addLabel(val)
                    self.labels.append(lab)
                    lab.pr.append(self)
        else:
            self.labels.append(repo.labels[0])
            repo.labels[0].pr.append(self)
        self.user = None
        for user in repo.contribs:
            if user.id == json['user']['id']:
                self.user = user
                self.user.pr.append(self)
                break
        if self.user is None:
            self.user = repo.addUser(json['user'])
            self.user.pr.append(self)

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
        self.pr = []

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
        self.pr = []
        if 'contributions' in json:
            self.totalContributions = json['contributions']

    def getLogin(self):
        return self.login

    def __eq__(self, other):
        return self.id == other.id

    def getPrintMessage(self, shift=1):
        tabs = '\t' * shift
        return f'{tabs}User: {self.login}'
