"""
Consider the sequence:
1, 1, 1, 3, 5, 9, 17, ...
where each successive term is the sum of the three preceding
terms.
How would you write a function fib3() to compute the n-th
term of this sequence?
Examples:
fib3(2) = 1
fib3(6) = 9
"""


def fib(num: int):
    a, b = 0, 1
    for i in range(0, num):
        c = a + b
        a, b = b, c
    return c


def fib3(num):
    a, b, c = 1, 1, 1
    for i in range(3, num):
        d = a + b + c
        a = b
        b = c
        c = d
    if num <= 3:
        return 1
    else:
        return d


"""
A ranking system generates ranking for two content types: course and degrees. The course ranking and degree ranking are two sorted arrays c and d, in descending order.
E.g.
c = [0.91, 0.88, 0.80, 0.51, 0.42]
d = [0.83, 0.79, 0.77, 0.56, 0,43, 0.40]

where
- element in each array represent the ranking score of a unique content for that content type. Score is normalized between 0-1
- element's index represents the unique content id
- a unique content can be represented in the form of a string "contenttype-index".
In the above example, for courses, we have course_1 with a ranking score 0.91, course_2 with a ranking score 0.88 and so on.
For degree, we have degree_1 with a ranking score 0.83, degree_2 with a ranking score 0.79 and so on.

Merge the course and degree ranking into one sorted array in descending order and return the content id `contenttype_index` for the sorted array. If there is a tie between course and degree, we prioritize course over degree

Example 1:
Input:
c = [0.91, 0.88, 0.80, 0.79, 0.51, 0.42]
d = [0.83, 0.79, 0.77, 0.56, 0.43, 0.40]
Output:
['course_0', 'course_1', 'degree_0', 'course_2', 'course_3', 'degree_1', 'degree_2', 'degree_3', 'course_4', 'degree_4', 'course_5', 'degree_5']
"""


def course_degree(c, d):
    output = []

    c_pointer, d_pointer = 0, 0
    while c_pointer < len(c) and d_pointer < len(d):
        c_idx, d_idx = c[c_pointer], d[d_pointer]
        if c_idx >= d_idx:
            output.append(f"course_{c_pointer}")
            c_pointer += 1
        elif c_idx < d_idx:
            output.append(f"degree_{d_pointer}")
            d_pointer += 1
    if c_pointer == len(c):
        for i in range(d_pointer, len(d)):
            output.append(f"degree_{i}")
    if d_pointer == len(d):
        for i in range(c_pointer, len(c)):
            output.append(f"course_{i}")
    return output


if __name__ == "__main__":
    out = fib3(6)
    # print(out)

    c = [0.91, 0.88, 0.80, 0.79, 0.51, 0.42]
    d = [0.83, 0.79, 0.77, 0.56, 0.43, 0.40]
    output = course_degree(c, d)
    print(output)
