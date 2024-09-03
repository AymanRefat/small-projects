from abc import ABC, abstractmethod
from collections import Counter


class BaseEventDisplayer(ABC):
		"""Base class for parsing and displaying data"""
		raise_on_add = True

		def __init__(self):
				self.data = []

		def is_event_type(self, event_type:str)->bool:
				"""return True if the event type matches"""
				return self.event_type == event_type

		def add_event(self, data:dict):
				"""add data to the current data"""
				if data['type'] != self.event_type and self.raise_on_add:
					raise ValueError(f"Invalid event type: {data['type']} for {self.event_type}")
				self.data.append(data)

		def add_events(self, data:list[dict]):
				"""add data to the current data"""
				for event in data:
					self.add_event(event)

		@property
		@abstractmethod
		def event_type(self):
				"""return the event type"""
				pass

		@abstractmethod
		def _display(self):
				"""display the data"""
				pass
		
		def display(self):
				"""display the data"""
				if self.data:
					print(f"{self.event_type}:")
					self._display()

class PushEventDisplayer(BaseEventDisplayer):

	@property
	def event_type(self):
			return "PushEvent"
	
	def _display(self):
			"""print the number of push events and how many commits for each repo"""
			repo_counter_commits = Counter()
			for data in self.data:
				repo_counter_commits[data['repo']['name']] += len(data['payload']['commits'])
			for repo, commits in repo_counter_commits.items():
				print(f"  - Repo: {repo}, Commits: {commits}")



class WatchEventDisplayer(BaseEventDisplayer):
	@property
	def event_type(self):
			return "WatchEvent"
	
	def _display(self):
			"""print the number of started events and the repo"""
			for data in self.data:
				print(f"  - Repo: {data['repo']['name']}")

class IssuesEventDisplayer(BaseEventDisplayer):
	
	@property
	def event_type(self):
			return "IssuesEvent"
	
	def _display(self):
			"""print the number of issues events and the action"""
			for data in self.data:
				print(f"  - Action: {data['payload']['action']}")

class ForkEventDisplayer(BaseEventDisplayer):
	
	@property
	def event_type(self):
			return "ForkEvent"
	
	def _display(self):
			"""print the number of forked events and the repo"""
			for data in self.data:
				print(f"  - Repo: {data['repo']['name']}")

class PullRequestEventDisplayer(BaseEventDisplayer):
	
	@property
	def event_type(self):
			return "PullRequestEvent"
	
	def _display(self):
			"""print the number of pull request events and the action"""
			for data in self.data:
				print(f"  - Action: {data['payload']['action']}")

class CreateEventDisplayer(BaseEventDisplayer):
	
	@property
	def event_type(self):
			return "CreateEvent"
	
	def _display(self):
			"""print the number of create events and the ref_type"""
			for data in self.data:
				print(f"  - Ref Type: {data['payload']['ref_type']}")

class DeleteEventDisplayer(BaseEventDisplayer):
	
	@property
	def event_type(self):
			return "DeleteEvent"
	
	def _display(self):
			"""print the number of delete events and the ref_type"""
			for data in self.data:
				print(f"  - Ref Type: {data['payload']['ref_type']}")

class ReleaseEventDisplayer(BaseEventDisplayer):
	
	@property
	def event_type(self):
			return "ReleaseEvent"
	
	def _display(self):
			"""print the number of release events and the action"""
			for data in self.data:
				print(f"  - Action: {data['payload']['action']}")


