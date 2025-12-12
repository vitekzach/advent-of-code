import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from functools import cache


@dataclass
class Device:
    id: int
    name: str
    is_output: bool
    out_to: list["Device"] = field(default_factory=list)

    def __repr__(self) -> str:
        return f'({self.id}) "{self.name}" {self.out_to} o:{self.is_output}'


class Board:
    def __init__(self) -> None:
        self.devices: list[Device] = []
        self.paths: list[tuple[str, ...]] = []
        self.fast_lookup: dict[str, list[str]] = {}
        self.finished_nodes: dict[str, list[tuple[str, ...]]] = defaultdict(list)
        self.bad_nodes: list[str] = []
        self.cached_paths_count: int = 0

    def __getitem__(self, key: str | int) -> Device:
        # print(f"lookup for {key}")
        if isinstance(key, int):
            if key >= len(self.devices):
                raise IndexError("Out of index")
            return self.devices[key]
        elif isinstance(key, str):
            inst = [x for x in self.devices if x.name == key]
            if len(inst) == 0:
                raise KeyError("No such device")
            if len(inst) > 1:
                raise KeyError("Device name not unique")
            return inst[0]

    def load_board(self, repr: str) -> None:
        lines = repr.split("\n")
        all_matches = []
        for line in lines:
            matches = re.findall(re.compile(r"([a-z]+): ([a-z ]+)"), line)
            all_matches.append(matches[0])

        unique_names = [x[0] for x in all_matches]
        if "out" not in unique_names:
            unique_names.append("out")
        for i, d in enumerate(unique_names):
            device = Device(i, d, d == "out")
            self.devices.append(device)

        for match in all_matches:
            match_d_name = match[0]
            match_d = self[match_d_name]
            outs = match[1].split(" ")
            self.fast_lookup[match_d_name] = outs
            for out in outs:
                out_d = self[out]
                match_d.out_to.append(out_d)
        self.fast_lookup["out"] = []
        # for d in self.devices:
        #     print(d.name, [x.name for x in d.out_to])

    @cache
    def cached_paths(self, next: str, goal: str):
        return 1 if next == goal else sum(self.cached_paths(n, goal) for n in self.fast_lookup[next])

    def find_paths(self, next_node_name: str, current_path: tuple[str, ...], goal_node: str = "out") -> None:
        current_path = current_path + (next_node_name,)
        # print(f"cp: {current_path}")

        if next_node_name == goal_node:
            print(f"Hit for {goal_node}! paths: {self.paths}")
            self.paths.append(current_path)
            print(f"After: {self.paths}")
            return

        counter = Counter(current_path)
        most_commont_count = counter.most_common(1)[0][1]
        if most_commont_count > 1:
            print(f"Cycle detected: {current_path}")

        found_finished_paths = self.finished_nodes[next_node_name]
        if len(found_finished_paths) > 0:
            # print(f"Add these: {found_finished_paths} cp: {current_path}")
            new_paths = [current_path + x for x in found_finished_paths]
            # print(f"Adding there: {new_paths}")
            self.paths.extend(new_paths)
            # found_paths = [x for x in self.paths if next_node_name in x]
            # if len(found_paths) > 0:
            #     print(
            #         f"Looks like we've been here before: \n\tcp:{current_path}\n\tfp:{found_paths}\n\tfn:{self.finished_nodes}"
            #     )
        else:
            for out in self.fast_lookup[next_node_name]:
                # print(f"curren path: {current_path}, next: {out.name}")
                self.find_paths(out, current_path, goal_node)
            # if len(self.finished_nodes[next_node_name]) > 0:
            # print(f"already finished for {next_node_name}?\n\tcp: {current_path}\n\tfp:{self.paths}")
            node_finished_paths = [x[x.index(next_node_name) + 1 :] for x in self.paths if next_node_name in x]
            # print(f"Node {next_node_name} finished\n\tcp:{current_path}\n\tfp:{self.paths}\n\tffp:{node_finished_paths}")

            self.finished_nodes[next_node_name].extend(node_finished_paths)

            print(f"Finished {len(self.finished_nodes.keys())}/{len(self.devices)}.")


# board = """aaa: you hhh
# you: bbb ccc
# bbb: ddd eee
# ccc: ddd eee fff
# ddd: ggg
# eee: out
# fff: out
# ggg: out
# hhh: ccc fff iii
# iii: out"""

# b = Board()
# b.load_board(board)
# b.find_paths("you", [])
# print(len(b.paths))

# board = """svr: aaa bbb
# aaa: fft
# fft: ccc
# bbb: tty
# tty: ccc
# ccc: ddd eee
# ddd: hub
# hub: fff
# eee: dac
# dac: fff
# fff: ggg hhh
# ggg: out
# hhh: out"""

# print("\033c", end="")
# b = Board()
# b.load_board(board)

# possible_paths = [
#     [["svr", "dac"], ["dac", "fft"], ["fft", "out"]],
#     [["svr", "fft"], ["fft", "dac"], ["dac", "out"]],
# ]
# overall_count = 0
# for path in possible_paths:
#     path_count = 1
#     for pair in path:
#         c = b.cached_paths(pair[0], pair[1])
#         path_count *= c
#     overall_count += path_count
# print(overall_count)
# print("board loaded")
# b.find_paths("svr", tuple(), "fft")
# for p in b.paths:
#     print(p)

# print()
# filtered = [x for x in b.paths if "fft" in x and "dac" in x]
# for f in filtered:
#     print(f)
