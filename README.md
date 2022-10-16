# Meta Hacker Cup 2022 - B1

## Problem

Given an m by n sized array, where each element in an array can take either 
the values `.` or `^`, do the following
1. Check if there exists a solution where for every `^`, there are ate least 
two neighbouring `^`.
2. If such a solution exists, provide an example of the solution

## Solution

### Observations

Before starting on the problem, the following observations were made that
simplified the problem
1. If there is only 1 row or only 1 column, and at least 1 `^`, there is no
possible solution
2. If there are no `^`, the solution is always possible
3. The question does not require us to check if the provided array is already
a solution, hence there is no need to check the provided array
4. By putting 8 `^` around each `^` in the original array, we are guaranteed
to solve the problem

### Steps
First, parse the input file, and convert each problem into a binary number, where
`0` represents `.`, and `1` represents `^`.

Example:
```
3 3
.^.
.^.
...
```
would be represented as `0b010010000`.

Second, check if a solution exists. If there is at most 1 row or 1 column and 
the binary number is greater than 0, then no solution exists.

Third, decompose the binary number into a list of individual bits. Using the 
example above, we get `0b10000000` and `0b10000`

Forth, using a combination of left and right shifts given the number of rows
and columns, we create a new binary number that represents having 8 `^`
surrounding the original `^`. Using the example above again:

For `0b10000000`, we get `0b111111000`, which would look like this after 
transformation
```
^^^
^^^
...
```

For `0b10000`, we get `0b111111111`, which would look like this after 
transformation
```
^^^
^^^
^^^
```

Fifth, for each of these new binary operations, we run the bitwise or operation
on the original binary number, and we get 
```
^^^
^^^
^^^
```

Sixth, the result is then written into the `loutput.txt` file.

## Running the script
To run the script, do
```bash
python3 main.py "./second_friend_input.txt"
```
