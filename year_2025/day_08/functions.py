import enum
import math


class Junction:
    def __init__(self, x: int, y: int, z: int, index: int) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.circuit_index: int | None = None
        self.index: int = index

    def __repr__(self) -> str:
        return f"ID{self.index}: [{self.x}, {self.y}, {self.z}] C({self.circuit_index})"

    def distance(self, other: "Junction") -> float:
        d = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)
        return d


class Distance:
    def __init__(self, junction_1: Junction, junction_2: Junction, distance: float) -> None:
        self.j1 = junction_1
        self.j2 = junction_2
        self.distance = distance

        if self.j1.index > self.j2.index:
            self.j1, self.j2 = self.j2, self.j1

    def __repr__(self) -> str:
        return f"{self.j1}-{self.j2}: {self.distance}"


class Playground:
    def __init__(self) -> None:
        self.junctions: list[Junction] = []
        self.distances: list[Distance] = []
        self.circuits: list[list[Junction]] = []
        self.connections: list[Distance] = []

    def load_playground(self, playground: str) -> None:
        rows = playground.split("\n")
        for i, row in enumerate(rows):
            x, y, z = row.split(",")
            j = Junction(int(x), int(y), int(z), i)
            self.junctions.append(j)

    def setup_playground(self) -> None:
        self.distances = []
        self.circuits = []
        self.connections = []
        for j, row in enumerate(self.junctions):
            for i, col in enumerate(self.junctions):
                if i > j:
                    self.distances.append(Distance(row, col, row.distance(col)))

        self.distances = sorted(self.distances, key=lambda x: x.distance)
        for i, junction in enumerate(self.junctions):
            junction.circuit_index = i
            self.circuits.append([junction])

    def connect_mins(self) -> Distance:
        min_info = self.distances.pop(0)
        # print(f"Found min: {min_info}")
        j1 = min_info.j1
        j2 = min_info.j2

        if j1.circuit_index is not None and j2.circuit_index is not None:
            if j1.circuit_index != j2.circuit_index:
                self.connect_circuits(j1.circuit_index, j2.circuit_index)
            # else:
            # print("Both already in ")
        elif j1.circuit_index is not None:
            # print("J1 already in c")
            circuit_index = j1.circuit_index
            j2.circuit_index = circuit_index
            self.circuits[circuit_index].append(j2)
        elif j2.circuit_index is not None:
            # print("J2 already in c")
            circuit_index = j2.circuit_index
            j1.circuit_index = circuit_index
            self.circuits[circuit_index].append(j1)
        else:
            # print("Neither")
            circuit_index = len(self.circuits)
            j1.circuit_index = circuit_index
            j2.circuit_index = circuit_index
            self.circuits.append([j1, j2])

        self.connections.append(min_info)
        # for i, c in enumerate(self.circuits):
        #     print(f"\t{i},len{len(c)} {c}")

        return min_info

    def connect_circuits(self, c1_index: int, c2_index: int) -> None:
        # print(f"Connecting circuits {c1_index} and {c2_index}")
        # for i, circ in enumerate(self.circuits):
        # print(f"Before: {i}: {circ}")
        if c2_index < c1_index:
            c1_index, c2_index = c2_index, c1_index

        # move junctions
        circuit_to_pop = self.circuits.pop(c2_index)
        for j in circuit_to_pop:
            j.circuit_index = c1_index
            self.circuits[c1_index].append(j)

        # recalculate all indices
        for c in range(c2_index, len(self.circuits)):
            circuit = self.circuits[c]
            for j in circuit:
                j.circuit_index = c

        # for i, circ in enumerate(self.circuits):
        #     print(f"After: {i}: {circ}")

    def connect_mins_times(self, times: int) -> None:
        while len(self.connections) < times:
            m = self.connect_mins()

    def connect_mins_all(self) -> None:
        while len(self.circuits) > 1:
            self.connect_mins()

    def get_circuit_size(self, cords: int):
        self.setup_playground()
        self.connect_mins_times(cords)
        longest_circuits = sorted(self.circuits, key=lambda x: len(x), reverse=True)
        size = len(longest_circuits[0])
        for i in range(1, 3):
            size *= len(longest_circuits[i])
        return size

    def one_circuit_size(self) -> int:
        self.setup_playground()
        self.connect_mins_all()
        last_connection_j1 = self.connections[-1].j1
        last_connection_j2 = self.connections[-1].j2
        size = last_connection_j1.x * last_connection_j2.x
        return size


playground = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""

# p = Playground()
# p.load_playground(playground)
# print(p.get_circuit_size(10))
# print("AGANE")
# print(p.one_circuit_size())
# for c in p.circuits:
#     print(len(c))
# print(p.connections)
# longest_circuits = sorted(p.circuits, key=lambda x: len(x), reverse=True)
# for c in longest_circuits:
#     print(len(c))
# print(p.get_circuit_size())
