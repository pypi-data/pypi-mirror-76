import sys
from timeit import default_timer as timer


def timed_run(f, step_name, *args):
    print(step_name + "... ")
    sys.stdout.flush()

    start = timer()
    ret_val = f(*args)
    end = timer()
    sys.stdout.write("done in ")
    print(str(end - start) + " seconds.")
    return ret_val
