# Day 4

import re


def main():
    with open("day4.input.txt", "r") as f:
        total_points = 0
        for line in f:
            line = line.strip()
            if not line:
                continue

            card_id, data = line.split(": ")
            winning_nums_raw, total_nums_raw = data.split(" | ")
            winning_nums = set(re.split(r'\s+', winning_nums_raw))
            total_nums = set(re.split(r'\s+', total_nums_raw))
            winning_user_has = total_nums & winning_nums

            card_points = 2 ** (len(winning_user_has) - 1) if winning_user_has else 0

            total_points += card_points

        print(total_points)




if __name__ == "__main__":
    main()
