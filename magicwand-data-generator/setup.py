"""
Purpose:
    setup.py is executed to build the python package

Copyright:
    This research was developed with funding from the Defense Advanced Research Projects
    Agency (DARPA) under Contract #HR0011-16-C-0060. This document was cleared for
    release under Distribution Statement” A” (Approved for Public Release, Distribution
    Unlimited). The views, opinions, and/or findings expressed are those of the authors
    and should not be interpreted as representing the official views or policies of the
    Department of Defense of the U.S. Government.

    The Government has unlimited rights to use, modify, reproduce, release,
    perform, display, or disclose computer software or computer software
    documentation marked with this legend. Any reproduction of technical data,
    computer software, or portions thereof marked with this legend must also
    reproduce this marking.

    MIT License

    (C) 2020 Two Six Labs, LLC.  All rights reserved.

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

# Python Imports
import os
import re
from setuptools import setup, find_packages


###
# Helper Functions
###


def get_version_from_file(python_version_file="./VERSION"):
    """
    Purpose:
        Get python version from a specified requirements file.
    Args:
        python_version_file (String): Path to the version file (usually
            it is VERSION in the same directory as the setup.py)
    Return:
        requirements (List of Strings): The python requirements necessary to run
            the library
    """

    version = "development"
    if os.path.isfile(python_version_file):
        with open(python_version_file) as version_file:
            version = version_file.readline().strip().strip("\n")

    return version


def get_requirements_from_file(python_requirements_file="./requirements.txt"):
    """
    Purpose:
        Get python requirements from a specified requirements file.
    Args:
        python_requirements_file (String): Path to the requirements file (usually
            it is requirements.txt in the same directory as the setup.py)
    Return:
        requirements (List of Strings): The python requirements necessary to run
            the library
    """

    requirements = []
    with open(python_requirements_file) as requirements_file:
        requirement = requirements_file.readline()
        while requirement:
            if requirement.strip().startswith("#"):
                pass
            elif requirement.strip() == "":
                pass
            else:
                requirements.append(requirement.strip())
            requirement = requirements_file.readline()

    return requirements


def get_requirements_from_packages(packages):
    """
    Purpose:
        Get python requirements for each package. will get requirements file
        in each package's subdirectory
    Args:
        packages (String): Name of the packages
    Return:
        requirements (List of Strings): The python requirements necessary to run
            the library
    """

    requirements = []
    for package in packages:
        package_dir = package.replace(".", "/")
        requirement_files = get_requirements_files_in_package_dir(package_dir)

        for requirement_file in requirement_files:
            package_requirements =\
                get_requirements_from_file(python_requirements_file=requirement_file)
            requirements = requirements + package_requirements

    return list(set(requirements))


def get_requirements_files_in_package_dir(package_dir):
    """
    Purpose:
        From a package dir, find all requirements files (Assuming form requirements.txt
        or requirements_x.txt)
    Args:
        package_dir (String): Directory of the package
    Return:
        requirement_files (List of Strings): Requirement Files
    """

    requirements_regex = r"^requirements[_\w]*.txt$"

    requirement_files = []
    for requirement_file in os.listdir(f"./{package_dir}"):
        if re.match(requirements_regex, requirement_file):
            requirement_files.append(f"./{package_dir}/{requirement_file}")

    return requirement_files


def get_readme(readme_file_location="./README.md"):
    """
    Purpose:
        Return the README details from the README.md for documentation
    Args:
        readme_file_location (String): Project README file
    Return:
        requirement_files (List of Strings): Requirement Files
    """

    readme_data = "Description Not Found"
    if os.path.isfile(readme_file_location):
        with open(readme_file_location, "r") as readme_file_object:
            readme_data = readme_file_object.read()

    return readme_data


###
# Main Functionality
###


def main():
    """
    Purpose:
        Main function for packaging and setting up packages
    Args:
        N/A
    Return:
        N/A
    """

    # Get Version and README
    version = get_version_from_file()
    readme = get_readme()

    # Get Packages
    packages = find_packages(exclude=("testing",))
    install_packages = [
        package
        for package
        in packages
        if not package.endswith(".tests")
    ]
    test_packages = [package for package in packages if package.endswith(".tests")]

    # Get Requirements and Requirments Installation Details
    install_requirements = get_requirements_from_packages(install_packages)
    test_requirements = get_requirements_from_packages(test_packages)
    setup_requirements = ["pytest-runner", "pytest", "pytest-cov", "pytest-html"]

    # Get Dependency Links For Each Requirement (As Necessary)
    dependency_links = []

    if not install_packages:
        raise Exception("No Packages Found To Install, Empty Project")

    setup(
        author="Two Six Labs",
        author_email="magicwand@twosixlabs.com",
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Natural Language :: English",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
        ],
        description=(
            "The Magicwand Data Tool is a platform generate TCP traffic data for identifying differences between normal TCP traffic and malicious 'low volume' denial of service traffic."
        ),
        include_package_data=True,
        install_requires=install_requirements,
        keywords=["python", "MAGICWAND", "TCP", "DDOS", "locust"],
        long_description=readme,
        long_description_content_type='text/markdown',
        name="magicwand",
        packages=packages,
        project_urls={},
        python_requires=">3.6",
        scripts=["magicwand/bin/magicwand"],
        setup_requires=setup_requirements,
        tests_require=test_requirements,
        url="https://github.com/twosixlabs/magicwand-datatool",
        version=version,
    )


if __name__ == "__main__":
    main()
