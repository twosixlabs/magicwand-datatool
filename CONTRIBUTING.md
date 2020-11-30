# Contributing to Magicwand

**NOTE: This document is a "getting started" summary for contributing to the Magicwand project.** Please make sure to read this page carefully to ensure the review process is as smooth as possible and to ensure the greatest likelihood of having your contribution be merged.


## How to Contribute

Magicwand is an open source project that is supported by a community who will gratefully and humbly accept any contributions you might make to the project. Large or small, any contribution makes a big difference; and if you've never contributed to an open source project before, we hope you will start with Magicwand!

Principally, Magicwand development is about the addition and creation of new traffic generation images. We'll discuss in detail how to add new images later.

Beyond creating images, there are many ways to contribute:

* Submit a bug report or feature request on GitHub Issues.
* Assist us with user testing.
* Add a new attack to our repository
* Add to the documentation or help with our website, 
* Write unit or integration tests for our project.
* Answer questions on our issues, mailing list, Stack Overflow, and elsewhere.
* Translate our documentation into another language.
* Write a blog post, tweet, or share our project with others.
* Teach someone how to use Magicwand.

As you can see, there are lots of ways to get involved and we would be very happy for you to join us! The only thing we ask is that you abide by the principles of openness, respect, and consideration of others as described in the [Python Software Foundation Code of Conduct](https://www.python.org/psf/codeofconduct/).

## Getting Started on GitHub

Magicwand is hosted on GitHub at TODO_INSERT_GITHUB_URL

The typical workflow for a contributor to the codebase is as follows:

1. **Discover** a bug or a feature by using Magicwand.
2. **Discuss** with the core contributes by TODO_INSERT_GITHUB_URL [adding an issue](#).
3. **Fork** the repository into your own GitHub account.
4. Create a **Pull Request** first thing to TODO_INSERT_GITHUB_URL [connect with us]() about your task.
5. **Code** the feature, write the documentation, add your contribution.
6. **Review** the code with core contributors who will guide you to a high-quality submission.
7. **Merge** your contribution into the Magicwand codebase.

We believe that *contribution is collaboration* and therefore emphasize *communication* throughout the open source process. We rely heavily on GitHub's social coding tools to allow us to do this. For instance, we use GitHub's [milestone](https://help.github.com/en/articles/about-milestones) feature to focus our development efforts for each Magicwand semester, so be sure to check out the issues associated with our TODO_INSERT_GITHUB_URL [current milestone]()!

Once you have a good sense of how you are going to implement the new feature (or fix the bug!), you can reach out for feedback from the maintainers by creating a TODO_INSERT_GITHUB_URL [pull request](). Please note that if we feel your solution has not been thought out in earnest, or if the PR is not aligned with our TODO_INSERT_GITHUB_URL[current milestone]() goals, we may reach out to ask that you close the PR so that we can prioritize reviewing the most critical feature requests and bug fixes.

Ideally, any pull request should be capable of resolution within 6 weeks of being opened. This timeline helps to keep our pull request queue small and allows Magicwand to maintain a robust release schedule to give our users the best experience possible. However, the most important thing is to keep the dialogue going! And if you're unsure whether you can complete your idea within 6 weeks, you should still go ahead and open a PR and we will be happy to help you scope it down as needed.

If we have comments or questions when we evaluate your pull request and receive no response, we will also close the PR after this period of time. Please know that this does not mean we don't value your contribution, just that things go stale. If in the future you want to pick it back up, feel free to address our original feedback and to reference the original PR in a new pull request.

### Forking the Repository

The first step is to fork the repository into your own account. This will create a copy of the codebase that you can edit and write to. Do so by clicking the **"fork"** button in the upper right corner of the Magicwand GitHub page.

Once forked, use the following steps to get your development environment set up on your computer:

1. Clone the repository.

    After clicking the fork button, you should be redirected to the GitHub page of the repository in your user account. You can then clone a copy of the code to your local machine.

    ```
    $ git clone https://github.com/[YOURUSERNAME]/TODO_INSERT_GITHUB_URL
    $ cd magicwand
    ```

    Optionally, you can also [add the upstream remote](https://help.github.com/articles/configuring-a-remote-for-a-fork/) to synchronize with changes made by other contributors:

    ```
    $ git remote add upstream TODO_INSERT_GITHUB_URL
    ```

    See "Branching Conventions" below for more on this topic.


2. Switch to the develop branch.

    The Magicwand repository has a `develop` branch that is the primary working branch for contributions. It is probably already the branch you're on, but you can make sure and switch to it as follows:

    ```
    $ git fetch
    $ git checkout develop
    ```

At this point you're ready to get started writing code!

### Branching Conventions

The Magicwand repository is set up in a typical production/release/development cycle as described in "[A Successful Git Branching Model](http://nvie.com/posts/a-successful-git-branching-model/)." The primary working branch is the `develop` branch. This should be the branch that you are working on and from, since this has all the latest code. The `master` branch contains the latest stable version and release, _which is pushed to PyPI_. No one but maintainers will push to master or develop.

**NOTE:** All pull requests should be into the `magicwand/develop` branch from your forked repository.

You should work directly in your fork and create a pull request from your fork's develop branch into ours. We also recommend setting up an `upstream` remote so that you can easily pull the latest development changes from the main Magicwand repository (see [configuring a remote for a fork](https://help.github.com/articles/configuring-a-remote-for-a-fork/)). You can do that as follows:

```
$ git remote add upstream https://github.com/TODO_INSERT_GITHUB_URL`
$ git remote -v
origin    https://github.com/YOUR_USERNAME/YOUR_FORK.git (fetch)
origin    https://github.com/YOUR_USERNAME/YOUR_FORK.git (push)
upstream  https://github.com/TODO_INSERT_GITHUB_URL (fetch)
upstream  https://github.com/TODO_INSERT_GITHUB_URL (push)
```

When you're ready, request a code review for your pull request. Then, when reviewed and approved, you can merge your fork into our main branch. Make sure to use the "Squash and Merge" option in order to create a Git history that is understandable.

**NOTE to maintainers**: When merging a pull request, use the "squash and merge" option and make sure to edit the both the subject and the body of the commit message so that when we're putting the changelog together, we know what happened in the PR. I recommend reading [Chris Beams' _How to Write a Git Commit Message_](https://chris.beams.io/posts/git-commit/) so we're all on the same page!

Core contributors and those who are planning on contributing multiple PRs might want to consider using feature branches to reduce the number of merges (and merge conflicts). Create a feature branch as follows:

```
$ git checkout -b feature-myfeature develop
$ git push --set-upstream origin feature-myfeature
```

Once you are done working (and everything is tested) you can submit a PR from your feature branch. Synchronize with `upstream` once the PR has been merged and delete the feature branch:

```
$ git checkout develop
$ git pull upstream develop
$ git push origin develop
$ git branch -d feature-myfeature
$ git push origin --delete feature-myfeature
```

Head back to Github and checkout another issue!

## Developing Magicwand Components 

In this section, we'll discuss the basics of developing magicwand components. This of course is a big topic, but hopefully these simple tips and tricks will help make sense.

### Magicwand Components

There are four basic types of components

- **Attacks** are components that attempt to shut down the SUT with malicious traffic
- **Benign** are components that send benign traffic to the SUT
- **SUT** The System under test that retrieves the attack and benign traffic
- **Sensors** are components that do auxiliary tasks such as RTT monitoring 

Creating a new component requires the following 

- Docker Image,
- Docker-compose script
- JSON configuration file,
- MwComponent python class
- MwRunner Updates

A barebones implementation is as follows...


#### Docker Image

This image will run a python script on start to send traffic to the SUT. You will need a Dockerfile, a begin-test.sh script, a python script, and a docker-compose.yml.  
The image can be placed in the `images` folder

```Dockerfile
FROM ubuntu:18.04
RUN apt-get update && apt-get install net-tools python3 python3-pip iproute2 vim -y
RUN pip3 install --upgrade pip; pip install requests


ADD begin-test.sh /usr/local/bin/
ADD example.py /usr/local/bin/
RUN chmod a+x /usr/local/bin/begin-test.sh
WORKDIR /usr/local/bin/
CMD ["./begin-test.sh"]
```


**begin-test.sh**
```bash
#!/bin/sh

_term() {
    echo [begin-test.sh] Example Caught SIGTERM signal!
    pkill -f python3.6\ example
}

trap _term TERM

#CLIENT OR ATTACK 
LOCAL_IP=`ip route show | grep src | cut -f 9  -d ' '`
echo "ip,type,subtype" >> /home/ip_map_rtt.csv
echo "$LOCAL_IP,client,rtt" >> /home/ip_map_client.csv

echo "timestamp,rtt" >> /home/rtt_stats.csv

echo "[begin-test.sh] python rtt_tracker.py"
python3.6 rtt_tracker.py

tail -f /dev/null
```

**example.py**
```python
import requests
import os
import time
import datetime


TARGET_URL = os.environ['TEST_TARGET']
DUR = os.environ['TEST_DURATION']
MY_PARM = os.environ['MY_PARM']
def main():

    counter = 0
    start = time.time()

    while counter < int(DUR):

        #curr_time = datetime.datetime.now().strftime("%H:%M:%S")

        try:
            r = requests.get("http://"+TARGET_URL,timeout=2)
            roundtrip = r.elapsed.total_seconds()            
        except:
            roundtrip = 2

        time.sleep(int(MY_PARM))
        counter += 1

if __name__ == "__main__":
    main()

```


#### MwComponent Folder

The following files will be placed inside the appropriate MwComponent folder in `magicwand-data-generator/magicwand/magicwand_components`   
This example will be for benign so our folder iwll be `magicwand-data-generator/magicwand/magicwand_components/benign/example_client/`


##### Docker-compose script

This is an example docker-compose script, that will start the component during runtime

**exmaple.yml**
```
  mw-client-example:
    image: MY_IMAGE:latest
    privileged: true
    depends_on:
      - "mw-sut-apachewp"
    environment:
      - TEST_DURATION=${CURR_TEST_DURATION}
      - MY_PARAM=${CURR_MY_PARAM}
      - TEST_TARGET=mw-sut-apachewp:80
    volumes:
      - ./${CURR_RUN}:/home/
```
Add this file to the `magicwand-data-generator/magicwand/magicwand_components/benign/example_client/example_client.yml`

##### MwComponent

This module contains the execution logic for our example client. It inherits from the MwComponent abstract class. Here is a full example
```python
"""
    Purpose:
        This file contains the class for example client
"""
import logging
import os
import time

from typing import Any, Dict
from magicwand.magicwand_components.mw_component import MwComponent
from magicwand.magicwand_utils.magicwand_utils import get_logger
from magicwand.magicwand_utils.magicwand_utils import load_json


class ExampleClient(MwComponent):

    name = "example_client"

    def __init__(self, log_level=logging.INFO) -> None:
        """
        Purpose:
            Init Component
        Args:
            log_level: Verbosity of the logger
        Returns:
            self: The MwComponent
        """
        # get logger
        # self._logger = get_logger("mw-log", log_level)
        super().__init__(log_level=log_level)

        # set config to expected spot
        self._config = load_json("magicwand_components/benign/example_client.json")

    @property
    def config(self) -> Dict[str, Any]:
        """
        Purpose:
            Get config
        Args:
            N/A
        Returns:
            config: The json config for the component
        """
        return self._config

    @config.setter
    def config(self, val: Dict[str, Any]) -> None:
        """
        Purpose:
            Set config
        Args:
            val: value of the config
        Returns:
            N/A
        """
        self.config = val

    def set_env_variables(self) -> int:
        """
        Purpose:
            Set environment variables 
        Args:
            N/A
        Returns:
            stats: 0 if worked, -1 if failed
        """
        try:
            os.environ["MY_PARM"] = str(self.config["MY_PARM"])
        except Exception as error:
            self.logger.error(error)
            return -1

        return 0

    def verify(self, config: Dict[str, Any], post_run_data: Dict[str, Any]) -> bool:
        """
        Purpose:
            Verify if the component worked during the run
        Args:
            config: Run config options
            post_run_data: Data for verifications
        Returns:
            passed: True if passed, False if failed
        """
        return True

```

Add this file to the `magicwand-data-generator/magicwand/magicwand_components/benign/example_client/example_client.py`

##### JSON configuration file

Here is an example JSON file

```json
{"benign":"example_client", "compose-file": "magicwand_components/benign/example_client.yml", "MY_PARM": 2}
```

Add this file to the `magicwand-data-generator/magicwand/magicwand_components/benign/example_client/example_client.json`


##### Final steps

We need to add some code to extra spots as well.

Create a `__init__.py` and add

```python
from .example_client import *
```

Also add this to benign's `__init__.py`

```python
from .example_client import *
```

In mw_runner.py add to the component dictionaries

```python
mw_components: Mapping[str, Type[MwComponent]] = {
    "apachekill": Apachekill,
    "sockstress": Sockstress,
    "goloris": Goloris,
    "sht_rudeadyet": Sht_rudeadyet,
    "sht_slowread": Sht_slowread,
    "sht_slowloris": Sht_slowloris,
    "httpflood": Httpflood,
    "synflood": Synflood,
    "mw_locust": MwLocust,
    "mw_rtt_sensor": MwRttSensor,
    "mw_apache_wp": MwApacheWp,
    "example_client": ExampleClient    <------ Update
}


valid_values = {
    "attack": [
        "apachekill",
        "sockstress",
        "goloris",
        "sht_rudeadyet",
        "sht_slowread",
        "sht_slowloris",
        "httpflood",
        "synflood",
    ],
    "benign": ["mw_locust","example_client"],          <------ Update
    "sut": ["mw_apache_wp"],
    "rtt": ["mw_rtt_sensor"],
}
```


#### Test your component

Once all of these are in place and your image is built. You can rebuild Magicwand

```bash
pip install --editable .
```

Create a new project

```bash
magicwand init --project new_example
```

Start your example

```bash
#make new config file

{
  "benign": "example_client",
  "sut": "mw_apache_wp",
  "rtt": "mw_rtt_sensor",
  "run_type": "example_client-only",
}


magicwand run --config configs/example_client.json
```

I know this is daunting and may require some give and take. Feel free to leave an issue on the GitHub page if you need help creating a new image or attack. We will also improve the process to add new images as well.

