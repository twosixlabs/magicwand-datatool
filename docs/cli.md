# MAGICWAND Data Generator CLI

This document will go over the functions in the Magicwand CLI 

```buildoutcfg
Usage: magicwand [OPTIONS] COMMAND [ARGS]...

  Magicwand data generation tool

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  calibrate  Calibrate the magicwand tool
  convert    Convert any pcap file to a CIC csv file
  init       Create and initialize magicwand folder
  run        Start a run to generate data
```

## Initialize Project (`init`)

The init command creates a magicwand project

```buildoutcfg
Usage: magicwand init [OPTIONS]

  Create magicwand project

Options:
  --project TEXT Folder to create  [required]
  --help         Show this message and exit.
```

Example use
```buildoutcfg
magicwand init --project test
```

## Execute Runs (`run`)

The run command starts the experiment using the JSON file for N number of runs saved to a folder inside data_runs.

```buildoutcfg
Usage: magicwand run [OPTIONS]

  Run command

Options:
  --config TEXT    JSON file with run parameters [required]
  --count INTEGER  Number of runs  [required]
  --data_version TEXT    Folder to save runs  [required]
  --help           Show this message and exit.
```

Example use
```bash
magicwand run --config configs/mw_locust-apachekill.json --count 5 --data_version test_runs 
```

## Calibrate Runs (`calibrate`)

The calibrate command tunes attacks to create the desired effects based on hardware resources.

```buildoutcfg
Usage: magicwand calibrate [OPTIONS]

  Calibrate Magicwand

Options:
  --ratio TEXT   Ratio config file
  --attack TEXT  Attack to tune, valid options: apachekill
                 [required]
  --help         Show this message and exit.
```

Example use
```bash
magicwand calibrate --attack apachekill
```


## Convert PCAPs (`convert`)

The convert command turns PCAP files to a CIC CSV file


```buildoutcfg
Usage: magicwand convert [OPTIONS]

  Convert any pcap file to a CIC csv file

Options:
  --pcap TEXT        PCAP to convert  [required]
  -o, --output TEXT  Output .csv filename
  -f, --force        Force output file to be overwritten if it already exists.
  --help             Show this message and exit.
```

Example use
```bash
magicwand convert --pcap my_pcap.pcap
```
