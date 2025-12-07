import re


class RangeMapping:
    def __init__(self, source_start: int, dest_start: int, mapping_range: int):
        self.source_start = source_start
        self.dest_start = dest_start
        self.differential = dest_start - source_start
        self.range = mapping_range

    def source_in_range(self, source_id: int) -> bool:
        return self.source_start <= source_id < self.source_start + self.range

    def get_mapping(self, source_id) -> int:
        return source_id + self.differential


class ChainLinkManager:
    def __init__(self) -> None:
        self.regex_for_mappings = re.compile(r"\d+")
        self.range_mappings: list[RangeMapping] = list()

    def create_chain_mapping_from_line(self, dest_range_start: int, source_range_start: int, range_length: int) -> None:
        self.range_mappings.append(RangeMapping(source_range_start, dest_range_start, range_length))

    def get_next_in_chain(self, current_id: int) -> int:
        for mapping in self.range_mappings:
            if mapping.source_in_range(current_id):
                return mapping.get_mapping(current_id)
        return current_id


class ChainManager:
    def __init__(self, input_file: str = "input.txt") -> None:
        self.seed_line_pattern = re.compile(r"seeds: (?:\d+[ ]*)+")
        self.seed_patter = r"\d+"

        self.chain = ["seed", "soil", "fertilizer", "water", "light", "temperature", "humidity", "location"]
        self.seed_to_soil_mananger = ChainLinkManager()
        self.soil_to_fertilizer_mananger = ChainLinkManager()
        self.fertilizer_to_water_mananger = ChainLinkManager()
        self.water_to_light_mananger = ChainLinkManager()
        self.light_to_temperature_mananger = ChainLinkManager()
        self.temperature_to_humidity_mananger = ChainLinkManager()
        self.humidity_to_location_mananger = ChainLinkManager()

        self.mapping_pattern = re.compile(
            r"(?P<source>\w+)-to-(?P<destination>\w+) map:\n(?:(?P<dest_start>\d+) (?P<source_start>\d+) (?P<range>\d+)\n)+"
        )

        self.parse_file(input_file)
        self.part_1_answer = self.part_1_get_closest_location()
        print(f"Part 1: Closest location is {self.part_1_answer}.")

    def get_relation(self, go_from_id: int, go_from_level: str, go_to_level: str) -> int:
        from_id = self.chain.index(go_from_level)
        to_id = self.chain.index(go_to_level)
        level_id = go_from_id

        walk_list = self.chain[from_id:to_id]
        for level in walk_list:
            manager = self.get_manager(level)
            level_id = manager.get_next_in_chain(level_id)

        return level_id

    def part_1_get_closest_location(self) -> int:
        locations = [(seed_id, self.get_relation(seed_id, "seed", "location")) for seed_id in self.seeds]
        locations = sorted(locations, key=lambda x: x[1])
        return locations[0][1]

    def get_manager(self, member: str) -> ChainLinkManager:
        match member:
            case "seed":
                return self.seed_to_soil_mananger
            case "soil":
                return self.soil_to_fertilizer_mananger
            case "fertilizer":
                return self.fertilizer_to_water_mananger
            case "water":
                return self.water_to_light_mananger
            case "light":
                return self.light_to_temperature_mananger
            case "temperature":
                return self.temperature_to_humidity_mananger
            case "humidity":
                return self.humidity_to_location_mananger

    def parse_file(self, path: str) -> None:
        with open(path, "r") as file:
            inputs = file.read()

        seed_line = re.search(self.seed_line_pattern, inputs)
        seeds_line = seed_line.group(0)

        seeds = re.findall(self.seed_patter, seeds_line)
        self.seeds = [int(seed) for seed in seeds]

        mappings = re.finditer(self.mapping_pattern, inputs)
        for mapping in mappings:
            # get number lines
            span_start, span_end = mapping.span()
            matched_span = inputs[span_start : span_end - 1]
            matched_lines = matched_span.split("\n")[1:]

            mapping_source = mapping.group("source")
            _ = mapping.group("destination")
            manager = self.get_manager(mapping_source)

            for line in matched_lines:
                mapping_dest_start, mapping_source_start, mapping_range = re.findall(self.seed_patter, line)
                mapping_dest_start = int(mapping_dest_start)
                mapping_source_start = int(mapping_source_start)
                mapping_range = int(mapping_range)

                manager.create_chain_mapping_from_line(mapping_dest_start, mapping_source_start, mapping_range)
