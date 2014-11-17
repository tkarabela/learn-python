#!/usr/bin/env python3

"""
Wages

Features:
object-oriented programming
recursion
prettyprinting

"""

class Employee:
    def __init__(self, name):
        self.name = name
        self.subordinates = set() # cannot write empty set as {}, that would be an empty dict

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

    def count_subordinates(self):
        # this only works when any person has at most one direct boss,
        # otherwise we would count them separately for each boss

        n = len(self.subordinates) # direct subordinates

        for person in self.subordinates:
            n += person.count_subordinates() # indirect subordinates

        return n

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
    irwin = Employee("Irwin")

    bill.subordinates.update({anne, mary, morgan})
    mary.subordinates.update({tom, paul})
    morgan.subordinates.update({irwin, paul, tom})
    tom.subordinates.update({gerry})

    for employee in [bill, anne, mary, morgan, gerry, tom, paul, irwin]:
        print(employee.name, "earns", employee.wage(), "CZK and has", employee.count_subordinates(), "subordinates")

    print("\nHierarchy from Bill's point of view:")
    bill.print_hierarchy()

    print("\nHierarchy from Tom's point of view:")
    tom.print_hierarchy()

if __name__ == "__main__":
    main()
