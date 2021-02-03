echo "Pulling and tagging images"

docker pull twosixlabsmagicwand/mw-client-smartswarm
docker tag twosixlabsmagicwand/mw-client-smartswarm mw-client-smartswarm

docker pull twosixlabsmagicwand/mw-client-rtt-tracker
docker tag twosixlabsmagicwand/mw-client-rtt-tracker mw-client-rtt-tracker

docker pull twosixlabsmagicwand/mw-cic-converter
docker tag twosixlabsmagicwand/mw-cic-converter mw-cic-converter

docker pull twosixlabsmagicwand/mw-attack-sht-slowread
docker tag twosixlabsmagicwand/mw-attack-sht-slowread mw-attack-sht-slowread

docker pull twosixlabsmagicwand/mw-attack-synflood
docker tag twosixlabsmagicwand/mw-attack-synflood mw-attack-synflood

docker pull twosixlabsmagicwand/mw-attack-sockstress
docker tag twosixlabsmagicwand/mw-attack-sockstress mw-attack-sockstress

docker pull twosixlabsmagicwand/mw-attack-apachekill
docker tag twosixlabsmagicwand/mw-attack-apachekill mw-attack-apachekill

docker pull twosixlabsmagicwand/mw-attack-sht-slowloris
docker tag twosixlabsmagicwand/mw-attack-sht-slowloris mw-attack-sht-slowloris

docker pull twosixlabsmagicwand/mw-attack-httpflood
docker tag twosixlabsmagicwand/mw-attack-httpflood mw-attack-httpflood

docker pull twosixlabsmagicwand/mw-sut-apachewp
docker tag twosixlabsmagicwand/mw-sut-apachewp mw-sut-apachewp

docker pull twosixlabsmagicwand/mw-sut-apachewp-plain
docker tag twosixlabsmagicwand/mw-sut-apachewp-plain mw-sut-apachewp-plain 

docker pull twosixlabsmagicwand/mw-attack-goloris
docker tag twosixlabsmagicwand/mw-attack-goloris mw-attack-goloris


echo "Done pulling and tagging images"
