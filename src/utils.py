import getopt
import sys
from models import SimpleModel


def usage(defaut_trace):
    print("Usage: ")
    print("       -t/--trace [trace file] , default trace file "+defaut_trace)
    print("       -m/--model [model name] , no default model ")
    print("       -h or --help")


def parse_args(argv, df_trace_path):
    try:
        opts, args = getopt.getopt(argv[1:], "t:h", ["trace", "help"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage(df_trace_path)
        sys.exit(2)
    
    model_name = None
    trace_path = df_trace_path
    for opt, arg in opts:
        if opt == "-t":
            trace_path = arg
        if opt == "-m":
            model_name = arg
        elif opt in ("-h", "--help"):
            usage(df_trace_path)
            sys.exit()
        else:
            assert False, "unhandled option"

    return (model_name, trace_path)
