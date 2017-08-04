# About

AWS CLI Speedtest is a tool for testing upload speeds, download speeds and latencies for the Amazon Simple Storage Service (S3).

# Details

The tool supports a Command Line Interface and tests can be run directly from a UNIX-Based Terminal on the command line. The results of the same are exported into separate CSV files. Multiple carousels and regions are also supported, so tests may also be run repeatedly on multiple S3 regions.

# Prerequisites

Requires requests and boto3 module.

To install use: pip install requests boto3

AWS must already be configured on the system with respect to an Amazon account before the tool may be used for testing.

# Usage

Once AWS has been successfully configured on the system with aws configure, the Speedtest can be run from the Terminal as

		speedtest.py carousels --locations locationList

Where carousels is the number of trials for the test, defaults to 1
		--locations grants support for S3 Region selection
		locationList is the set of S3 regions to be tested

# Configuring Regions
By default, the tool reads from the file locations.txt which contains the list of locations. Any locations can be included or excluded from the test by commenting in or out with a Hash mask(# ).

# Output
The test results are exported as the files ul-[locationName], dl-[locationName] and lat-[locationName] for the Upload SpeedTest, the Download SpeedTest and the Latency Test respectively, for the S3 region corresponding to locationName.

# Example

For benchmarking servers over 3 trials for the regions us-east-1 and ap-southeast-1, the command would be:

		speedtest.py 3 --locations us-east-1 ap-southeast-1
