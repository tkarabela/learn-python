#!/usr/bin/env python3

"""
Latin Squares

Backtracking solver for Latin Squares.

Features:
list-of-lists
multiple constructors via @classmethod
recursion

References:
http://en.wikipedia.org/wiki/Latin_square

"""

class Square:
    """
    A Latin Square.

    A Latin Square is N x N table of N symbols with no duplicates in rows or columns,
    in this case symbols are integers 0, ..., N-1,
    blank cells are allowed (represented with None),
    there is a solve() method to fill blank cells so that Latin Square is produced (if possible)

    """
    def __init__(self, n=3):
        self.n = n
        self.fields = [[None for j in range(n)] for i in range(n)]
        self.free_in_row = [set(range(n)) for i in range(n)]
        self.free_in_col = [set(range(n)) for j in range(n)]


    @classmethod
    def from_string(cls, text):
        """Only works for squares N <= 10"""
        lines = text.splitlines(keepends=False)
        n = len(lines[0])

        if len(lines) != n or not all(len(line) == n for line in lines):
            raise ValueError("Cannot read non-square shape")

        square = cls(n) # new instance of Square
        for i in range(n):
            for j in range(n):
                c = lines[i][j]
                if c.isdigit():
                    square.set_field(i, j, int(c))
                else:
                    pass # field is empty

        return square

    def set_field(self, i, j, value):
        choices = self.get_choices(i, j)

        if value not in range(self.n):
            raise ValueError("Possible values are integers 0..%d, not %r" % (self.n-1, value))
        if self.fields[i][j] is not None:
            raise ValueError("Field %d,%d already has value %r" % (i, j, self.fields[i][j]))
        elif not value in choices:
            raise ValueError("Field %d,%d can only be %r, not %r" % (i, j, choices, value))

        self.fields[i][j] = value
        self.free_in_row[i].remove(value)
        self.free_in_col[j].remove(value)

    def reset_field(self, i, j):
        value = self.fields[i][j]

        if value is None:
            raise ValueError("Field %d,%d is already empty" % (i, j))

        self.fields[i][j] = None
        self.free_in_row[i].add(value)
        self.free_in_col[j].add(value)

    def get_empty_field(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.fields[i][j] is None:
                    return i, j
        raise KeyError("No empty field")

    def get_choices(self, i, j):
        return self.free_in_row[i] & self.free_in_col[j]

    def solve(self):
        try:
            i, j = self.get_empty_field()
        except KeyError:
            return True

        for value in self.get_choices(i, j):
            self.set_field(i, j, value)
            if self.solve():
                return True
            self.reset_field(i, j)

        return False

    def __repr__(self):
        lines = []
        for i in range(self.n):
            line = []
            for j in range(self.n):
                value = self.fields[i][j]
                if value is None:
                    line.append("{:>2}".format("."))
                else:
                    line.append("{:>2}".format(value))
            lines.append(" ".join(line))
        return "\n".join(lines)


INPUT = """
...1
.1..
..3.
.2..
""".strip()

def main():
    square = Square.from_string(INPUT)
    square.solve()
    print(square)

if __name__ == "__main__":
    main()
