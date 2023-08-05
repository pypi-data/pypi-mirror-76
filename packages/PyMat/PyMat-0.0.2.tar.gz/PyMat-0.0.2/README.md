# Matrix

*Mathematical matrix module for Python*

## Requirements
- Python 3

## Usage
Create a Matrix by specifying dimensions or passing in a list of lists.
```python
matrix_dimension = Matrix(10, 10)
matrix_listlist = Matrix([[1, 2], [3, 4], [5, 6], [7, 8]])
```

*Note*: All functions and operations will create a new Matrix instance, similar
to the behaviour of Pandas' Dataframes.

## Operations

### Addition

Constant addition:
```python
matrix: Matrix
k: int

matrix + k
```

Matrix addition:
```python
a_matrix: Matrix
b_matrix: Matrix

a_matrix + b_matrix
```

### Multiplication

Constant multiplication:
```python
matrix: Matrix
k: int

matrix * k
```

Matrix multiplication:
```python
a_matrix: Matrix
b_matrix: Matrix

a_matrix * b_matrix
```

### Transposing
```python
matrix: Matrix

matrix.transpose()
```

## Examples
```
A: Matrix = 
13 83 42 69 73 35 14 43 50 58
 9 16 25 58 51 70 52 68 83 65
72 52  4 84 12 10 30 90 55  3
60 71 47 20 60 93 45 50  9 46
84  6 58 71 90 49 49 97  9 58

B: Matrix = 
96 85 52  5 81  35 54 72 67 10
98 90 71 64 56  70 60  4 92 20
 9 47 42 13 42  35 31 33 46 54
45 26 29 25 66  17 89 42 18 46
79 86 36 59 51 100 65 13 25 39

C: Matrix = 
 7  6 64 23 40
92 24 55 75 74
83 88 55 52 74
68 14 52 64  2
57 21 73 33 81
40 60 27 11 86
 2 88 98 95 85
37 12 24 76 77
44 37 58 92 89
12  4 79 94 37

k: int = 2
```
---
```python
A + k
```
```
15 85 44 71 75 37 16 45 52 60
11 18 27 60 53 72 54 70 85 67
74 54  6 86 14 12 32 92 57  5
62 73 49 22 62 95 47 52 11 48
86  8 60 73 92 51 51 99 11 60
```
---
```python
A + B
```
```
109 168 94  74 154  70  68 115 117 68
107 106 96 122 107 140 112  72 175 85
 81  99 46  97  54  45  61 123 101 57
105  97 76  45 126 110 134  92  27 92
163  92 94 130 141 149 114 110  34 97
```
---
```python
A * k
```
```
 26 166  84 138 146  70  28  86 100 116
 18  32  50 116 102 140 104 136 166 130
144 104   8 168  24  20  60 180 110   6
120 142  94  40 120 186  90 100  18  92
168  12 116 142 180  98  98 194  18 116
```
---
```python
A * C
```
```
25981 14195 27455 30568 29928
20313 17444 28137 32726 33109
18262  9827 21729 26678 23510
22241 18397 28027 26659 34208
22651 17617 32715 31758 34323
```
---
```python
A.transpose()
```
```
13  9 72 60 84
83 16 52 71  6
42 25  4 47 58
69 58 84 20 71
73 51 12 60 90
35 70 10 93 49
14 52 30 45 49
43 68 90 50 97
50 83 55  9  9
58 65  3 46 58
```
