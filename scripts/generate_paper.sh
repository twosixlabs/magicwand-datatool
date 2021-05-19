#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Generate Joss Paper
#
# Common Arguments:
# -h, --help
#     Print help and exit
#
# Example Call:
#    bash generate_paper.sh
# -----------------------------------------------------------------------------


###
# Arguments
###

# Get Path
BASE_DIR=$(cd $(dirname ${BASH_SOURCE[0]}) >/dev/null 2>&1 && pwd)

# Parse CLI Arguments
while [ $# -gt 0 ]
do
    key="$1"

    case $key in
        -h|--help)
        echo "Example Call: bash generate_paper.sh"
        exit 1;
        ;;
        *)
        echo "ERROR unknown argument \"$1\""
        exit 1
        ;;
    esac
done

###
# Main Execution
###

echo "Generating Paper"
docker run --rm \
    --volume $BASE_DIR/../paper:/data \
    --user $(id -u):$(id -g) \
    --env JOURNAL=joss \
    openjournals/paperdraft