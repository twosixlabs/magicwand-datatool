#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Pull all Docker Images for Magicwand-Datatool
#
# Common Arguments:
# -h, --help
#     Print help and exit
#
# Example Call:
#    bash pull_images.sh
# -----------------------------------------------------------------------------


###
# Arguments
###


# Parse CLI Arguments
while [ $# -gt 0 ]
do
    key="$1"

    case $key in
        -h|--help)
        echo "Example Call: bash pull_images.sh"
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

echo "Pulling Images"

docker pull twosixlabsmagicwand/mw-client-smartswarm
docker pull twosixlabsmagicwand/mw-client-rtt-tracker
docker pull twosixlabsmagicwand/mw-cic-converter
docker pull twosixlabsmagicwand/mw-attack-sht-slowread
docker pull twosixlabsmagicwand/mw-attack-synflood
docker pull twosixlabsmagicwand/mw-attack-sockstress
docker pull twosixlabsmagicwand/mw-attack-apachekill
docker pull twosixlabsmagicwand/mw-attack-sht-slowloris
docker pull twosixlabsmagicwand/mw-attack-httpflood
docker pull twosixlabsmagicwand/mw-sut-apachewp
docker pull twosixlabsmagicwand/mw-sut-apachewp-plain
docker pull twosixlabsmagicwand/mw-attack-goloris
docker pull twosixlabsmagicwand/mw-attack-sht-rudeadyet

echo "Done pulling images"
