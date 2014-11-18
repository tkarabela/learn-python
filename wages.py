#!/usr/bin/env python3

"""
Wages

Features:
object-oriented programming
recursion
tree traversal
prettyprinting

"""

class Employee:
    def __init__(self, name):
        self.name = name
        self.subordinates = set() # cannot write empty set as {}, that would be an empty dict
        self.boss = None

    def wage(self):
        n = self.count_subordinates()

        if n == 0:
            return 12000
        elif n <= 2:
            return 15000
        elif n < 10:
            return 25000
        else:
            return 40000

    def add_subordinates(self, *people):
        for person in people:
            if person in self.subordinates:
                raise ValueError("Person %s is already a subordinate" % person.name)
            elif person.boss is not None:
                raise ValueError("Person %s has a different boss (%s)" % (person.name, person.boss.name))
            else:
                person.boss = self
                self.subordinates.add(person)

    def count_subordinates(self):
        # this only works when any person has at most one direct boss (which is our case),
        # otherwise we would count them separately for each boss

        n = len(self.subordinates) # direct subordinates

        for person in self.subordinates:
            n += person.count_subordinates() # indirect subordinates

        return n

    def count_superiors(self):
        if self.boss is None:
            return 0
        else:
            return self.boss.count_superiors() + 1

    def print_hierarchy(self, level=0):
        print(level*"\t", "-", self.name)
        for person in self.subordinates:
            person.print_hierarchy(level+1)


def main():
    bill = Employee("Bill Boss")
    anne = Employee("Anne Assistant")
    mary = Employee("Marry Manager")
    morgan = Employee("Morgan Manager")
    gerry = Employee("Gerry")
    tom = Employee("Tom")
    paul = Employee("Paul")
    ronald = Employee("Ronald")
    irwin = Employee("Irwin")

    bill.add_subordinates(anne, mary, morgan)
    mary.add_subordinates(tom, ronald)
    morgan.add_subordinates(irwin, paul)
    tom.add_subordinates(gerry)

    for employee in [bill, anne, mary, morgan, gerry, tom, paul, irwin]:
        print(employee.name, "earns", employee.wage(), "CZK and has", employee.count_subordinates(), "subordinates")

    print("\nHierarchy from Bill's point of view:")
    bill.print_hierarchy()

    print("\nHierarchy from Tom's point of view:")
    tom.print_hierarchy()

    print()
    for person in [anne, bill, gerry]:
        print(person.name, "has", person.count_superiors(), "superiors")

if __name__ == "__main__":
    main()
