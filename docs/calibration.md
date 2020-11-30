# Calibration

Calibration attempts to find the parameters needed for the runs to exhibit the desired effects of the attack based on current hardware resources.

It does this by following this sequence.


!!! note 
    As of v0.4.0, only `apachekill` can be calibrated

1. Start a run with only client traffic
2. Start a run with only attack traffic
3. Compare various metrics such as RTT and SUT resources
4. If the ratio between the client and attack metrics is good, then save a tuned json file


Example Use
```bash
magicwand calibrate --attack apachekill
```
