# Day 4

import re


def main():
    with open("day4.input.txt", "r") as f:
        card_id_to_winning_count = {}
        card_id_to_cards_counts = {}
        max_card_idx = -1

        for line in f:
            line = line.strip()
            if not line:
                continue

            card_id_raw, data = line.split(": ")
            _, card_id = re.split(r'\s+', card_id_raw)
            card_id = int(card_id)

            winning_nums_raw, total_nums_raw = data.split(" | ")
            winning_nums = set(re.split(r'\s+', winning_nums_raw))
            total_nums = set(re.split(r'\s+', total_nums_raw))
            winning_user_has = total_nums & winning_nums

            card_id_to_winning_count[card_id] = len(winning_user_has)
            card_id_to_cards_counts[card_id] = 1

            max_card_idx = max(max_card_idx, card_id)

        for card_id in range(1, max(card_id_to_cards_counts.keys()) + 1):
            no_matching_nums = card_id_to_winning_count[card_id]
            count_of_card_with_that_id = card_id_to_cards_counts[card_id]

            for idx in range(1, no_matching_nums + 1):
                assert idx <= max_card_idx
                card_id_to_cards_counts[card_id + idx] += count_of_card_with_that_id

        print(sum(card_id_to_cards_counts.values()))



if __name__ == "__main__":
    main()
