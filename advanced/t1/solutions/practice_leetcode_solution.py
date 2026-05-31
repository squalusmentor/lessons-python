"""Эталонное решение практики 2 — задачи с LeetCode."""


def fizz_buzz(n):
    result = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(i))
    return result


def running_sum(nums):
    result = []
    total = 0
    for n in nums:
        total += n
        result.append(total)
    return result


if __name__ == "__main__":
    print("fizz_buzz(15) =", fizz_buzz(15))
    print("running_sum([1, 2, 3, 4]) =", running_sum([1, 2, 3, 4]))
