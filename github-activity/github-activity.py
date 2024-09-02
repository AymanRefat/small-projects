import argparse as arg 
import requests as r 
from collections import Counter


class GithubActivityDisplayer:

		def __init__(self, data_list: list[dict]):
				self.data_list = data_list
				self.started:list[dict] = [ ]
				self.pushed:list[dict] = [ ]
				self.issue:list[dict] = [ ]
				self.forked:list[dict] = [ ]
				self.pull_request:list[dict] = [ ]
				self.create:list[dict] = [ ]
				self.delete:list[dict] = [ ]
				self.release:list[dict] = [ ]
				self.other:list[dict] = [ ]
				for data in data_list:
					if data['type'] == "WatchEvent":
						self.started.append(data)
					elif data['type'] == "PushEvent":
						self.pushed.append(data)
					elif data['type'] == "IssuesEvent":
						self.issue.append(data)
					elif data['type'] == "ForkEvent":
						self.forked.append(data)
					elif data['type'] == "PullRequestEvent":
						self.pull_request.append(data)
					elif data['type'] == "CreateEvent":
						self.create.append(data)
					elif data['type'] == "DeleteEvent":
						self.delete.append(data)
					elif data['type'] == "ReleaseEvent":
						self.release.append(data)
					else:
						self.other.append(data)
		
		def display_pushed(self):
			"""print the number of push events and how many commits for each repo"""
			if len(self.pushed) == 0:
				return
			print("Pushed: ")
			repo_counter_commits = Counter()
			for data in self.pushed:
				repo_counter_commits[data['repo']['name']] += len(data['payload']['commits'])
			for repo, commits in repo_counter_commits.items():
				print(f"  - Repo: {repo}, Commits: {commits}")


		def display_started(self):
			"""print the number of started events and the repo"""
			print("Started: ")
			if len(self.started) == 0:
				return
			for data in self.started:
				print(f"  - Repo: {data['repo']['name']}")
		
		def display_issue(self):
			"""print the number of issues events and the action"""
			if len(self.issue) == 0:
				return
			print("Issues: ")
			for data in self.issue:
				print(f"  - Action: {data['payload']['action']}")
		
		def display_forked(self):
			"""print the number of forked events and the repo"""
			if len(self.forked) == 0:
				return
			print("Forked: ")
			for data in self.forked:
				print(f"  - Repo: {data['repo']['name']}")
		
		def display_pull_request(self):
			"""print the number of pull request events and the action"""
			if len(self.pull_request) == 0:
				return
			print("Pull Requests: ")
			for data in self.pull_request:
				print(f"  - Action: {data['payload']['action']}")
		
		def display_create(self):
			"""print the number of create events and the ref_type"""
			if len(self.create) == 0:
				return
			print("Created: ")
			for data in self.create:
				print(f"  - Ref Type: {data['payload']['ref_type']}")
		
		def display_delete(self):
			"""print the number of delete events and the ref_type"""
			if len(self.delete) == 0:
				return
			print("Deleted: ")
			for data in self.delete:
				print(f"  - Ref Type: {data['payload']['ref_type']}")

		def display_release(self):
			"""print the number of release events and the action"""
			if len(self.release) == 0:
				return
			print("Released: ")
			for data in self.release:
				print(f"  - Action: {data['payload']['action']}")

		def display_other(self):
			"""print the number of other events and the type"""
			if len(self.other) == 0:
				return
			print("Other: ")
			for data in self.other:
				print(f"  - Type: {data['type']}")
		


		def display_all(self): 
				"""call all the functions that start with display"""
				print("Output: ")
				for attr in dir(self):
					if attr.startswith("display_") and callable(getattr(self, attr)) and attr != "display_all":
						getattr(self, attr)()
				



def main():
		parser = arg.ArgumentParser(description="This is a simple script to get the github activity of a user")
		parser.add_argument("username", help="The username of the user")
		args = parser.parse_args()
		print(f"The username you entered is {args.username}")

		res = r.get(f"https://api.github.com/users/{args.username}/events")
		if res.status_code != 200:
			print(f"Error fetching data: {res.status_code}")
			exit(1)
		else : 
			data = res.json()
			if len(data) == 0:
				print("No data found")
				exit(0)
			else:
				d = GithubActivityDisplayer(data)
				d.display_all()


if __name__ == "__main__":
	main()