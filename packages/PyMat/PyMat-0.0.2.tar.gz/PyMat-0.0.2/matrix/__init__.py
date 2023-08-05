import csv
from functools import reduce
from typing import List, Optional, Union


class Matrix:
    def __init__(self,
                 rows: Union[int, List],
                 cols: Optional[int] = None,
                 default: Optional[int] = 0):
        if isinstance(rows, list):
            self.rows = len(rows)
            self.cols = max([len(row) for row in rows] or [0])

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

    def __add__(self, other) -> 'Matrix':
        if isinstance(other, (float, int)):
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

    def __getitem__(self, item) -> Union[float, 'Matrix']:
        r, c = item

        rs = list(range(self.rows))[r] if isinstance(r, slice) else [r]
        cs = list(range(self.cols))[c] if isinstance(c, slice) else [c]

        if isinstance(r, int) and isinstance(c, int):
            return self.data[rs[0]][cs[0]]

        return Matrix([[self[i, j] for j in cs] for i in rs])

    def __iter__(self):
        return iter(self.data)

    def __mul__(self, other) -> 'Matrix':
        if isinstance(other, (float, int)):
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

    def __neg__(self):
        return self * -1

    def __pow__(self, power: int, modulo=None):
        return reduce((lambda x, y: x * y), [self for _ in range(power)])

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

    def __sub__(self, other):
        return self + (-other)

    def __truediv__(self, other):
        if isinstance(other, Matrix):
            return self * (other.inverse())

        return self * (1 / other)

    def concat(self, other: 'Matrix') -> 'Matrix':
        if self.cols == 0:
            return other

        if other.cols == 0:
            return self

        if self.cols == other.cols:
            return Matrix(list(self) + list(other))

        raise ValueError()

    def determinant(self) -> float:
        if self.rows == 2 and self.cols == 2:
            return (self[0, 0] * self[1, 1]) - (self[0, 1] * self[1, 0])

        if self.rows == self.cols and self.rows >= 3:
            return sum([
                pow(-1, i) *
                self[0, i] *
                self.remove(0, i).determinant()
                for i in range(self.rows)
            ])

        raise ValueError()

    def inverse(self) -> 'Matrix':
        if self.rows == 2 and self.cols == 2:
            try:
                return Matrix(
                    [[self[1, 1], -self[0, 1]], [-self[1, 0], self[0, 0]]]) * (
                                   1 / self.determinant())
            except ZeroDivisionError:
                raise ValueError()

        if self.rows == self.cols and self.rows >= 3:
            return Matrix([[pow(-1, (i + j)) * self.remove(i, j).determinant()
                            for j in range(self.cols)] for i in
                           range(self.rows)]).transpose() * (
                               1 / self.determinant())

        raise ValueError()

    def join(self, other: 'Matrix') -> 'Matrix':
        if self.rows == other.rows:
            return Matrix([[self[i, j] for j in range(self.cols)] +
                           [other[i, j] for j in range(other.cols)]
                           for i in range(self.rows)])

        raise ValueError()

    def load(self, load_list: List[List[int]]):
        for i, row in enumerate(load_list):
            for j, col in enumerate(row):
                self[i, j] = col

    def multi_single_index(self, index):
        if isinstance(index, int):
            return [index // self.rows, index % self.rows]
        else:
            return index[0] * self.cols + index[1]

    def remove(self, row: int, col: int) -> 'Matrix':
        return self[:row, :col].join(self[:row, col + 1:]).concat(
            self[row + 1:, :col].join(self[row + 1:, col + 1:]))

    def save(self, filename: str, format: str = "csv"):
        if format == "csv":
            with open(filename, "w") as f:
                w = csv.writer(f, delimiter=",")
                for row in self.data:
                    w.writerow(row)

    def transpose(self) -> 'Matrix':
        return Matrix([[self[i, j] for i in range(self.rows)] for j in
                       range(self.cols)])
