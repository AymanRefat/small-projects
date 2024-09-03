import argparse as arg
from app.event_parser import EventParsers
from app.api import get_events 

def main():
		parser = arg.ArgumentParser(description="This is a simple script to get the github activity of a user")
		parser.add_argument("username", help="The username of the user")
		args = parser.parse_args()
		print(f"The username you entered is {args.username}")
			# get the events
		data = 	get_events(args.username)
		if data  == []:
			print("No events found")
			exit(0)
		else : 
			event_parser	= EventParsers(data)
			event_parser.display_data()


if __name__ == "__main__":
	main()