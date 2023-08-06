import re

from template import Template


class Request:
    def __init__(self, argv=None):
        self.argv = argv
        self.generate_data = False
        self.process_data = False
        self.data_file = "data.csv"
        self.template = Template("template.yml", self)
        self.partition_size = 1000
        self.parallel_processes = 1
        self.parse_args()

    def parse_args(self):
        if not self.argv:
            self.generate_data = True
            self.process_data = True
        else:
            for arg in self.argv:
                if arg in ["", "g", "gen", "generate"]:
                    self.generate_data = True
                elif re.match("l:\d+", arg):
                    self.parallel_processes = int(arg.split(':')[1])
                elif re.match("s:\d+", arg):
                    self.partition_size = int(arg.split(':')[1])
                elif re.match("t:[a-zA-Z0-9_/]", arg):
                    self.template = Template(arg.split(':')[1], self)

                if arg in ["", "p", "proc", "process"]:
                    self.process_data = True

    def data_generation_requested(self):
        return self.generate_data

    def data_processing_requested(self):
        return self.process_data
