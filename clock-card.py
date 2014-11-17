#!/usr/bin/env python3

"""
Clock card

Description:
Suppose we have a set of logs from card readers in a building.
People who work there have to check in whenever they enter (+) or leave (-) the building.
Such an event is logged along with current time and name of the card's holder.
Cards are non-transferable, so there shouldn't be eg. two subsequent enter logs with the same card.
Logs from different card readers are separated by a line with the "#" mark.
Note that a person may exit through a different entrance than the one they used to get in.
The goal is to count total time spent in the building for each card holder.

Features:
encapsulating state in objects
comprehensions
time handling
namedtuple
reading text file
sorting

"""

from datetime import datetime, timedelta
from collections import namedtuple

LOG_FILE = """\
+ 08:00:00 John
+ 08:50:00 Linda
- 09:30:00 John
- 18:20:00 Linda
- 19:00:00 John
#
- 17:00:00 John
+ 18:00:00 John
#
#
+ 08:00:00 Max
+ 09:00:00 Roger
+ 10:00:00 John
- 15:00:00 Roger
- 17:30:00 Max
"""

class Person:
    def __init__(self, name):
        self.name = name
        self.inside = False
        self.entrance_time = None
        self.total_time_inside = timedelta()

    def enter(self, t):
        if self.inside:
            raise ValueError("Person %s is already inside" % self.name)
        else:
            self.inside = True
            self.entrance_time = t

    def exit(self, t):
        if self.inside:
            self.inside = False
            self.total_time_inside += t - self.entrance_time
        else:
            raise ValueError("Person %s is already outside" % self.name)


Event = namedtuple("Event", ["type", "time", "name"])


def read_log(text):
    events = []

    for line in text.splitlines():
        if line == "" or line.startswith("#"): continue
        event_type, time_as_str, person_name = line.split()
        events.append(
            Event(type=event_type,
                  time=datetime.strptime(time_as_str, "%H:%M:%S"),
                  name=person_name))

    return events

def process_log(text):
    events = read_log(text)
    events.sort(key=lambda event: event.time) # sort in ascending order by time

    people = {}

    for event in events:
        person = people.setdefault(event.name, Person(event.name)) # create a Person if they don't exist

        if event.type == "+":
            person.enter(event.time)
        elif event.type == "-":
            person.exit(event.time)
        else:
            raise ValueError("Unknown event type %r" % event.type)

    return people


def main():
    people = process_log(LOG_FILE)

    max_time_inside = max(person.total_time_inside for person in people.values())

    hard_workers = [person for person in people.values()
                    if person.total_time_inside == max_time_inside]

    print("Longest time at work was",
          max_time_inside,
          "which was achieved by",
          ", ".join(person.name for person in hard_workers))

if __name__ == "__main__":
    main()
