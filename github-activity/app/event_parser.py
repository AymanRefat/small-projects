from collections import defaultdict
from app.utiles import load_subclasses_from_module
from app import event_displayers
from app.event_displayers import BaseEventDisplayer

class EventParsers: 
	def __init__(self, data:list[dict]) -> None:
		self.data = data 
		self.event_displayers_classes:list[type] = load_subclasses_from_module(event_displayers, event_displayers.BaseEventDisplayer)
		self.event_displayers_objects:list[BaseEventDisplayer] = [cls() for cls in self.event_displayers_classes]
		self.event_by_type = self.create_event_by_type()
		self.add_events_to_displayers()

	def create_event_by_type(self)->dict:
		"""return a dictionary of events by type"""
		event_by_type = defaultdict(list)
		for event in self.data:
			event_by_type[event['type']].append(event)
		return event_by_type

	def add_events_to_displayers(self)->None:
		"""add events to the displayers"""
		for event_displayer in self.event_displayers_objects:
			event_displayer.add_events(self.event_by_type.get(event_displayer.event_type,[]))


	def display_data(self)->None:
		"""display the data"""
		for event_displayer in self.event_displayers_objects:
			event_displayer.display()
		








