# Day 9
import pathlib

def _generate_sequences(dataset: list[int]) -> list[list[int]]:
    sequences: list[list[int]] = [dataset]
    while True:
        current_level_sequence = sequences[-1]
        if all(n == 0 for n in current_level_sequence):
            break

        next_dataset = []
        for left, right in zip(current_level_sequence[:-1], current_level_sequence[1:]):
            next_dataset.append(right - left)

        sequences.append(next_dataset)

    return sequences



def main():
    data = pathlib.Path("day9_input_test.txt").read_text()
    datasets_raw = data.split('\n')
    datasets: list[list[int]] = []
    for dataset_raw in datasets_raw:
        dataset = [int(n) for n in dataset_raw.split(' ')]
        datasets.append(dataset)

    for dataset in datasets:
        sequences = _generate_sequences(dataset)
        filled_by_one =

if __name__ == "__main__":
    main()
