import os
from collections import defaultdict

INPUT_FILE = "AdventOfCode//2024//inputs//01.txt"


def read_input(path: str) -> tuple[list[int], list[int]]:
    with open(path, "r") as file:
        data = file.read().splitlines()

    list1 = []
    list2 = []
    for line in data:
        numbers = line.split("   ")
        list1.append(int(numbers[0]))
        list2.append(int(numbers[1]))
    return (list1, list2)


def problem_1(path: str) -> int:
    list1, list2 = read_input(path)

    list1 = sorted(list1)
    list2 = sorted(list2)
    distance = 0
    for num1, num2 in zip(list1, list2):
        distance += abs(num1 - num2)
    return distance


def problem_2(path: str) -> int:
    list1, list2 = read_input(path)

    key_mapping = {num: 0 for num in list1}
    similarity_score = 0

    for num in list2:
        if key_mapping.get(num) is not None:
            key_mapping[num] += 1
            similarity_score += num

    return similarity_score


if __name__ == "__main__":
    path = os.path.join(os.getcwd(), INPUT_FILE)

    # Get the solution of problem1
    distance = problem_1(path)
    similarity_score = problem_2(path)

    print("The total distance between ordered elements of the two lists is:", distance)
    print("The similarity score is: ", similarity_score)
