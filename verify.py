import csv
import requests
import sys

from typing import List, Tuple, NewType
from termcolor import cprint

UrlTuple = NewType("UrlTuple", Tuple[str, str])


def transform(url: str) -> str:
    # Implementation of url transformation
    return url


def calculatePercentage(correct: List, incorrect: List) -> float:
    return round((len(correct) / (len(correct) + len(incorrect))) * 100, 2)


def verify_destinations(urls: List[UrlTuple]) -> bool:
    correct = []
    failed = []

    for origin, expected_destination in urls:
        response = requests.get(origin)
        actual_destination = transform(response.url)

        if actual_destination == expected_destination:
            print(
                f"Origin: {origin}\nExpected Destination: \n{expected_destination}\nActual Destination: \n{actual_destination}"
            )
            cprint("Verification successful!\n", "green")
            correct.append(origin)
        else:
            print(f"Status code: ", response.status_code)
            print(
                f"Origin: {origin}\nExpected Destination: \n{expected_destination}\nActual Destination: \n{actual_destination}"
            )
            cprint("Verification failed!\n", "red")
            failed.append(origin)

    print("List of failures: \n" + "\n".join(failed))
    print(f"Correct %: {calculatePercentage(correct, failed)}")

    return len(failed) == 0


if len(sys.argv) < 2:
    print("Usage: python script.py <file_path>")
    sys.exit(1)

file_path = sys.argv[1]

# Retrieve URLs from CSV file and construct complete URLs
url_list = []
with open(file_path, "r") as file:
    reader = csv.reader(file)
    for row in reader:
        path = row[0]
        expected_destination = row[1]
        url_list.append((path, expected_destination))

# Remove header
url_list.pop(0)

verify_destinations(url_list)
