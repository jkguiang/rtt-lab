import json
import argparse

from hgg.helpers import loop_helper

if __name__ == "__main__":
    """
    This script is an all-purpose looper which performs a selection and writes
    all events passing this selection to a pandas dataframe
    """
    parser = argparse.ArgumentParser()

    # Physics content
    parser.add_argument(
        "--samples",
        help = "path to json file containing samples & metadata",
        type = str,
        default = "data/samples_and_scale1fb.json"
    )
    parser.add_argument(
        "--selections",
        help = "preselection(s) to perform looping for",
        type = str,
        default = "HHggTauTau_InclusivePresel"
    )
    parser.add_argument(
        "--years",
        help = "csv list of years",
        type = str,
        default = "2016,2017,2018"
    )
    parser.add_argument(
        "--select_samples",
        help = "csv list of samples to run over (should be a subset of samples in args.samples)",
        type = str,
        default = "all"
    )

    # --options points to a json file containing options for looping
    # this could include things like additional scaling of bkg samples,
    # application of reweighting procedures, etc
    parser.add_argument(
        "--options",
        help = "path to json file containing looping options",
        type = str,
        default = "data/HH_ggTauTau_default.json"
    )
    parser.add_argument( #TODO
        "--systematics",
        help = "include systematics variations", 
        action = "store_true"
    )

    # Book-keeping
    parser.add_argument(
        "--output_tag",
        help = "tag to identify these plots/tables/ntuples",
        type = str,
        default = "test"
    )
    parser.add_argument(
        "--output_dir",
        help = "dir to place outputs in", 
        type = str,
        default = "outputs/hgg_test/"
    )

    # Technical
    parser.add_argument(
        "--batch",
        help = "run locally vs. on dask vs. condor",
        type = str,
        default = "local"
    )
    parser.add_argument(
        "--nCores",
        help = "number of cores to run locally on",
        type = int,
        default = 8
    )
    parser.add_argument(
        "--debug",
        help = "debug level",
        type = int,
        default = 0
    )
    parser.add_argument(
        "--fast",
        help = "loop over minimal set of samples (for debugging purposes)",
        action = "store_true"
    )
    parser.add_argument(
        "--dry_run",
        help = "don't submit jobs",
        action = "store_true"
    )

    # RTT
    parser.add_argument(
        "-o", "--output_json", 
        type=str, default="",
        help="Name of output JSON on client"
    )
    parser.add_argument(
        "--server", 
        type=str, default="172.17.0.2:1094",
        help="<IP>:<port> of server"
    )

    args = parser.parse_args()

    looper = loop_helper.RTTLoopHelper(**vars(args))
    report = looper.run()

    # Write out report
    if args.output_json:
        with open(args.output_json, "w") as f_out:
            json.dump(report, f_out)
    else:
        print("Runtime: {} seconds".format(report["runtime"]))
