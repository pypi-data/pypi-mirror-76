import sys

from request import Request
from data_processor import DataProcessor
import util


def main():
    r = Request(sys.argv[1:])
    t = r.template

    p = DataProcessor(r)

    util.timed_run(t.generate, "Generating data")
    util.timed_run(p.run, "Processing data")


if __name__ == '__main__':
    main()
