import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))

from pyrfdata.request import Request
import pyrfdata.util


def main():
    r = Request(sys.argv[1:])
    t = r.template

    pyrfdata.util.timed_run(t.generate, "Generating data")


if __name__ == '__main__':
    main()
