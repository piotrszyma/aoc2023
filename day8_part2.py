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

    def is_start(self) -> bool:
        return self.symbol[-1] == 'A'

    def is_end(self) -> bool:
        return self.symbol[-1] == 'Z'


def main():
    data = pathlib.Path("day8_input.txt").read_text()

    instructions_raw, nodes_all_raw = data.split("\n\n")
    instructions = [Instruction.from_string(i) for i in instructions_raw]
    nodes_raw = nodes_all_raw.split('\n')

    node_symbol_to_node: dict[str, Node] = {}

    for node_raw in nodes_raw:
        node = Node.from_string(node_raw)
        node_symbol_to_node[node.symbol] = node

    start_nodes = [n for n in node_symbol_to_node.values() if n.is_start()]

    current_nodes = start_nodes

    steps = 0

    for next_move in itertools.cycle(instructions):
        is_end = True
        next_current_nodes: list[Node] = []
        for current_node in current_nodes:
            node = node_symbol_to_node[current_node.symbol]
            neighbour_id = node.neighbour(next_move)

            next_node = node_symbol_to_node.get(neighbour_id)
            assert next_node

            next_current_nodes.append(next_node)
            if is_end and not next_node.is_end():
                is_end = False


        current_nodes = next_current_nodes
        steps += 1

        if is_end:
            break

    print(steps)


if __name__ == "__main__":
    main()
