# Day 6

from dataclasses import dataclass
from functools import reduce
import operator
import pathlib
import re

@dataclass
class RaceRecord:
    time: int
    distance: int

def main():
    data = pathlib.Path("day6_input.txt").read_text()
    line_time, line_distance = data.split("\n")
    time_raw = line_time.replace("Time:", "")
    time = int("".join(time_raw.split()))

    distance_raw = line_distance.replace("Distance:", "")
    distance = int("".join(distance_raw.split()))

    times = [time]
    distances = [distance]

    records = [RaceRecord(t, d) for (t, d) in zip(times, distances)]

    opts_per_record = []

    for record in records:
        opts = 0
        for i in range(record.time):
            time_spent_waiting = i
            speed_after_btn_release = time_spent_waiting
            time_left = record.time - time_spent_waiting
            distance_made = time_left * speed_after_btn_release
            if distance_made > record.distance:
                opts += 1
        opts_per_record.append(opts)

    multipled = reduce(operator.mul,  opts_per_record)
    print(multipled)

if __name__ == "__main__":
    main()
