# Day 1

def main():
    with open("day1.input.txt", "r") as f:
        total = 0

        for line in f:
            if not line.strip():
                break

            left_idx = 0
            right_idx = len(line) - 1
            first: str | None = None
            last: str | None = None

            while True:
                if first is None and line[left_idx].isdigit():
                    first = line[left_idx]

                if last is None and line[right_idx].isdigit():
                    last = line[right_idx]

                if first and last:
                    break

                left_idx += 1
                right_idx -= 1

            assert first and last

            num = int(first + last)

            total += num

        print(total)




if __name__ == "__main__":
    main()
