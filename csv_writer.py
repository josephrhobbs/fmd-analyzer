# CSV Writer

class OutputFile(object):
    """
    An abstraction over an output CSV file
    """
    def __init__(self, path, columns):
        """
        Initialize a CSV file, given its file path and column names
        """
        self.rows = [[str(c) for c in columns]]
        self.path = path

    def add(self, row):
        """
        Add a row to this CSV file
        """
        self.rows.append(row)

    def save(self):
        """
        Write this CSV to the given file path
        """
        # Convert to string
        output = "\n".join(
            [",".join(
                [str(v) for v in row]
            ) for row in self.rows]
        )

        with open(self.path, "w") as f:
            f.write(output)

    def __get__(self, i):
        """
        Access a value by row and column
        """
        # Unpack row index and column name
        r, cname = i

        # Find column index
        c = self.rows[0].index(cname)

        return self.rows[r+1][c]

    def __getitem__(self, i):
        """
        Access a value by row and column

        Note: row index starts at zero!
        """
        # Unpack row index and column name
        r, cname = i

        # Find column index
        c = self.rows[0].index(cname)

        return self.rows[r+1][c]

    def __iter__(self):
        """
        Convert this CSV into an iterable
        """
        return iter(self.rows[1:])

    def __setitem__(self, i, value):
        """
        Set a value by row and column

        Note: row index starts at zero!
        """
        # Unpack row index and column name
        r, cname = i

        # Find column index
        c = self.rows[0].index(cname)

        self.rows[r+1][c] = value