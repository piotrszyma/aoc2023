# Day 8
from dataclasses import dataclass
import enum
import itertools
import pathlib


class Instruction(enum.StrEnum):
    LEFT = enum.auto()
    RIGHT = enum.auto()

    @staticmethod
    def from_string(v: str) -> "Instruction":
        match v:
            case "L":
                return Instruction.LEFT
            case "R":
                return Instruction.RIGHT
            case _:
                raise ValueError(f"Unexpected instruction string {v}")

@dataclass
class Node:
    symbol: str
    left: str
    right: str

    @staticmethod
    def from_string(s: str) -> 'Node':
        """From 'AAA = (BBB, CCC)' string."""
        node_symbol, neighbours_raw = s.split(" = ")
        neighbours_raw = neighbours_raw[1:-1]
        left, right = neighbours_raw.split(", ")
        return Node(symbol=node_symbol, left=left, right=right)

    def neighbour(self, instruction: Instruction) -> str:
        if instruction == Instruction.LEFT:
            return self.left
        elif instruction == Instruction.RIGHT:
            return self.right
        else:
            raise ValueError(f"unexpected instruction {instruction}")


def main():
    data = pathlib.Path("day8_input.txt").read_text()

    instructions_raw, nodes_all_raw = data.split("\n\n")
    instructions = [Instruction.from_string(i) for i in instructions_raw]
    nodes_raw = nodes_all_raw.split('\n')

    node_id_to_node: dict[str, Node] = {}

    for node_raw in nodes_raw:
        node = Node.from_string(node_raw)
        node_id_to_node[node.symbol] = node

    current_id = 'AAA'
    steps = 0

    for next_move in itertools.cycle(instructions):
        node = node_id_to_node[current_id]
        neighbour_id = node.neighbour(next_move)

        current_id = neighbour_id
        steps += 1

        if current_id == 'ZZZ':
            break

    print(steps)


if __name__ == "__main__":
    main()
