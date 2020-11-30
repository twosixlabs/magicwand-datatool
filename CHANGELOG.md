# CHANGELOG

## v0.4.0

- Removed view runs
- Added CIC convert command
- CIC conversion done post run automatically
- Documentation updated
- General code clean up


## v0.3.0
- Code refactor release, no new features 

## v0.2.0

- Updated documentation
- Quality of Life Improvements
- Variable for Locust stagger start time

## v0.1.0

Lots of changes, this is a release that would be safe for external users to test.

### Added new attacks
* httpflood
* synflood

### Code refactored
* less yaml files
* smaller json config files
* removed dead code and files

### Locust configuration 
* added random keep alive toggle
* added random start time for locust clients

### SUT configuration
* can configure snap length for pcap capture

### Documentation 
* Updated mkdocs

### Data Verification 
* added data tests for apachekill
* added ip check tests

### Data viewer updated
 * Better readability
 * always up to date



## v0.0.2

- Added mkdocs-based documentation	
- Added tests	
  - Test that `init` executed properly	
  - Test that an apachekill `run` created the correct files	
- Added new attacks 	
  - sockstress	
  - slowhttptest (slowloris, rudy, slowread)	
  - goloris	
- Added version tagging for data generated	
- Added local image building
