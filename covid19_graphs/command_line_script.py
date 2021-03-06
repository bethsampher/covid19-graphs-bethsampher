"""tool to download and process COVID-19 data"""
import argparse
import logging
from covid19_graphs.covid19_processing import Covid19Processing


def parse_command_line_args(test_override=None):
    """Parse options returning the args namespace

    Sets up the command line using argparse including the help message.
    Here, a single sequence string for output directory is required.

    test_override is an optional list of arguments (this is for testing).

    returns the args namespace that can be used for control
    """
    parser = argparse.ArgumentParser(description=__doc__)
    help_ = 'directory for output files '
    parser.add_argument('out_dir', metavar='OUT_DIR', help=help_)
    help_ = 'option to specify for graphs'
    parser.add_argument('-g', '--graphs', action='store_true', help=help_)
    help_ = 'turn on debug message logging output'
    parser.add_argument('-d', '--debug', action='store_true', help=help_)
    if test_override is not None:
        args = parser.parse_args(test_override)
    else:
        args = parser.parse_args()
    return args


def main():
    """ main function invoked by covid19 script"""
    args = parse_command_line_args()
    # turn on debug level logging if user specifies --debug
    if args.debug:
        logging.basicConfig(level=logging.DEBUG,
                            format='debug %(message)s')
    print(__doc__)
    out_dir = args.out_dir
    logging.debug('args namespace: %s', args)
    logging.debug('will output to directory: %s', out_dir)
    c_process = Covid19Processing(out_dir)
    c_process.download_from_github()
    c_process.store_data_for_csv()
    c_process.create_out_dir()
    c_process.write_csv_files()
    if args.graphs:
        c_process.remove_unrecognised_column()
        c_process.make_axes()
        c_process.create_graph_dir()
        c_process.write_png_files()
