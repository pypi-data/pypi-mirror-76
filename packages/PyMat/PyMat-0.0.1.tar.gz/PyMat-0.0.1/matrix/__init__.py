from typing import List, Optional, Union


class Matrix:
    def __init__(self,
                 rows: Union[int, List],
                 cols: Optional[int] = None,
                 default: Optional[int] = 0):
        if isinstance(rows, list):
            self.rows = len(rows)
            self.cols = max([len(row) for row in rows])

            self.data = [[default for _ in range(self.cols)] for _ in
                         range(self.rows)]
            self.widths = [len(str(default)) for _ in range(self.cols)]

            self.load(rows)

        else:
            if cols is None:
                cols = rows

            self.rows, self.cols = (rows, cols)
            self.data = [[default for _ in range(cols)] for _ in range(rows)]
            self.widths = [len(str(default)) for _ in range(cols)]

    def __add__(self, other):
        if isinstance(other, int):
            return Matrix(
                [[self[i, j] + other for j in range(self.cols)] for i in
                 range(self.rows)])

        if isinstance(other, Matrix):
            if self.rows == other.rows and self.cols == other.cols:
                return Matrix(
                    [[self[i, j] + other[i, j] for j in range(self.cols)] for i
                     in range(self.rows)])
            raise ValueError()

        raise TypeError()

    def __getitem__(self, item):
        r, c = item

        rs = list(range(self.rows))[r] if isinstance(r, slice) else [r]
        cs = list(range(self.cols))[c] if isinstance(c, slice) else [c]

        if len(rs) == 1 and len(cs) == 1:
            return self.data[r][c]

        return Matrix([[self[i, j] for j in cs] for i in rs])

    def __mul__(self, other):
        if isinstance(other, int):
            return Matrix(
                [[self[i, j] * other for j in range(self.cols)] for i in
                 range(self.rows)])

        if isinstance(other, Matrix):
            if self.cols == other.rows:
                return Matrix([[sum(
                    [self[i, j] * other[j, k] for j in range(self.cols)]) for k
                                                 in range(other.cols)] for i in
                                                range(self.rows)])
            raise ValueError()

        raise TypeError()

    def __setitem__(self, key, value):
        r, c = key

        self.widths[c] = max(self.widths[c], len(str(value)))
        self.data[r][c] = value

    def __str__(self):
        return "\n".join(
            [" ".join(
                [
                    f"{self[i, j]: >{self.widths[j]}}"
                    for j in
                    range(self.cols)
                ]
            ) for i in range(self.rows)]
        )

    def load(self, load_list: List[List[int]]):
        for i, row in enumerate(load_list):
            for j, col in enumerate(row):
                self[i, j] = col

    def multi_single_index(self, index):
        if isinstance(index, int):
            return [index // self.rows, index % self.rows]
        else:
            return index[0] * self.cols + index[1]

    def transpose(self):
        return Matrix([[self[i, j] for i in range(self.rows)] for j in
                       range(self.cols)])
