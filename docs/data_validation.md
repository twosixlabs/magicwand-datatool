# Data Validation

The key purpose of this tool is to provide high-quality, reliable, and reproducible data sets for low-and-slow DDoS attacks. To validate each data generation run, our tool conducts a series of checks. While we have been systematic and methodical in crafting these checks to make them as comprehensive as possible, we imagine that we weren't totally exhaustive.

## Motivating Questions

Through the data validation process, we aim to address the following questions:

1. Is the attack functioning as intended?
2. Are all the components of the experiment run functioning?
3. Are all the collection sensors functioning?
4. Did the run complete? Did we capture all of the expected data?

### Is the attack functioning as intended?

Our primary usage for this dataset was in the development of a machine-learning-based low-and-slow DDoS defense. Each of the attacks we have included could be converted into a volumetric (connection- or packet-based) attack, simply by ramping up the parameters of the attack (e.g. number of threads to use). If so, the generated data would not properly represent a low-and-slow attack.

<!-- TODO: add in discussion of how we approach this --> 

!!! note 
    There are certainly applications of these data sets where the volumetric attacks traits are exhibited. To achieve this behavior, you will need to use a custom [run configuration](data.md#run_tunedjson).

Here are some examples of attack signatures (Different for each attack) we check for during each experiment:

- Did attack work as expected?
    - apachekill
        -  is the attack client sending overlapped bytes?
    - sockstress: is attack client sending RSTs?
        - is the attack client sending RSTs?

- Did we see the expected data sent/received

### Are all of the components of the experiment run functioning?

For each experiment we check for evidence that each of these components is functioning.

!!! note 
    These checks have **NOT** be implemented in 1.0.0


Client Signatures:

- Did the benign client work as expected?
- Did the client do what we configured it to do
- Were the settings, right?

SUT Signatures:

- Did the SUT work as expected?
- Were there any unexpected incoming/outgoing connections?
- Did the SUT appear to send back valid HTTP data?

### Are all the sensors functioning correctly?

For each experiment we check for evidence that our sensor was up and running.

Evidence of sensors functioning

- Is a PCAP generated?

Resources:

- Did we RTT Stats?
- Did we capture Apache server stats (CPU,Memory,etc..)?

### Did the run complete? Did we capture all the expected data?

For each experiment we check for evidence that the run completed and produced data

Test Run: 

- Did we see all expected IPs in the PCAP
- are there IPs in the PCAP that aren't in ip_attr_map.csv?

Higher Level Metrics:

- RTTs as expected

Run Data:

- Were all files generated?
- Was everything captured as expected and not corrupted?
- was there anything unexpected in the data?

<!-- Tune using volumetric attacks?

- Connection-volumetric
- Packet-volumetric
- Data-volumetric (not considered for now) -->
