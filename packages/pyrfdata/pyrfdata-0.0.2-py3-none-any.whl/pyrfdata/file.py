import os

from multiprocessing.pool import Pool
from cell_generator import CellGenerator
from partition import partition
import util


class File:
    def __init__(self, spec, request):
        self.original_spec = spec
        self.spec = None
        self.request = request
        self.delim = ','
        self.location = spec["name"]
        self.sequence_generators = {}
        self.generators = {}
        self.data = []

    def generate(self):
        self.spec = self.expand_spec()
        self.data = util.timed_run(self.generate_data, "actually generating data")
        util.timed_run(self.write_data, "writing data")

    def expand_spec(self):
        spec = {"name": self.original_spec["name"],
                "rows": self.original_spec["rows"]}
        cols = []
        for col_spec in self.original_spec["cols"]:
            if "repeat" not in col_spec:
                cols.append(col_spec)
            else:
                names = self.column_name(col_spec)

                for name in names:
                    new_col_spec = col_spec.copy()
                    del new_col_spec["repeat"]
                    new_col_spec["name"] = name
                    cols.append(new_col_spec)
        spec["cols"] = cols
        return spec

    def write_data(self):
        f = open(self.location, "w", encoding="utf-8")
        for row in self.data:
            f.write(row)
            f.write(os.linesep)
        f.close()

    def generate_data(self):
        data = []
        self.column_names = self.create_title_row()
        data.append(self.column_names)
        rows = int(self.spec["rows"])

        partitions = partition(rows, self.request.partition_size)

        for p in partitions:
            start = p["start"]
            self.generators[start] = {}
            for col_spec in self.spec["cols"]:
                self.generators[start][col_spec["name"]] = CellGenerator(col_spec["generator"], start)

        pool = Pool(processes=self.request.parallel_processes)
        async_results = []
        for p in partitions:
            async_results.append(pool.apply_async(util.timed_run, [self.generate_partition, "generating partition " + str(p), p]))

        for async_result in async_results:
            data.extend(async_result.get())
        return data

    def generate_partition(self, p):
        data = []
        for r in range(p["start"], p["end"]+1):
            data.append(self.create_row(self.create_cell, p["start"]))
        return data

    def create_title_row(self):
        return self.create_row(self.column_name)

    def create_row(self, create_function, partition_start=None):
        generators = None if partition_start not in self.generators else self.generators[partition_start]
        row = []
        for col_spec in self.spec["cols"]:
            generator = None if not generators else generators[col_spec["name"]]
            cell_value = create_function(col_spec, generator)
            if isinstance(cell_value, list):
                row.extend(cell_value)
            else:
                row.append(cell_value)

        return self.delim.join(row)

    def create_cell(self, col_spec, generator=None):
        c = CellGenerator(col_spec['generator'])
        if generator:
            c = generator

        count = 1 if 'repeat' not in col_spec else int(col_spec['repeat'])
        values = []
        for i in range(count):
            values.append(c.generate())
        return values

    def column_name(self, col_spec, generator=None):
        if isinstance(col_spec['name'], dict):
            prefix = col_spec['name']['generator']['params']['prefix']
            if 'repeat' in col_spec:
                col_spec['name']['repeat'] = col_spec['repeat']

            self.sequence_generators[prefix] = CellGenerator(col_spec['name']['generator'])
            return self.create_cell(col_spec['name'], self.sequence_generators[prefix])

        elif isinstance(col_spec['name'], str):
            return col_spec['name']

        else:
            print("what? ", col_spec)