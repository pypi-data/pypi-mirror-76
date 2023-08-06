import os
import sys
import yaml
from file import File


class Template:
    def __init__(self, loc, request):
        self.loc = loc
        self.request = request
        self.files = []
        self.template_yml = None

    def load(self):
        template_file = open(self.loc, "r")
        self.template_yml = yaml.load(template_file, Loader=yaml.FullLoader)
        template_file.close()

        for file in self.template_yml["files"]:
            self.files.append(File(file, self.request))

    def generate(self):
        if self.request.data_generation_requested():
            try:
                if not self.template_yml:
                    self.load()

                for file in self.files:
                    file.generate()
            except FileNotFoundError as e:
                print("ERROR: Template not found at " + self.loc)
                sys.exit(-1)

    def location(self):
        return self.loc

    def is_valid(self):
        return os.path.isfile(self.loc)
