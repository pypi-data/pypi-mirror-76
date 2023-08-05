# __main__.py

from configparser import ConfigParser
##from importlib import resources # Python 3.7+
import sys
import requests
import os

from nam import upload
from nam import download

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


proxies = {
  "http": None,
  "https": None,
}

nexus_format = sys.argv[1]
auth = (sys.argv[2], sys.argv[3])
url = sys.argv[4]
path = sys.argv[5]
artifact_name = sys.argv[6]
repository = sys.argv[7]
directory = sys.argv[8]

def assign_parameters():
    if nexus_format == '' or nexus_format != 'npm' or  nexus_format != 'nuget' or  nexus_format != 'maven':
        print("Please specify repository format e.g npm, maven, npm, nuget")
        return 1

    return 0


def main():
    ##cfg = ConfigParser()
    ##cfg.read_string(resources.read_text("reader", "config.txt"))
    ##url = cfg.get("feed", "url")
    print("Copyright \N{COPYRIGHT SIGN} 2020 Stewartium\n")

    if assign_parameters():
        print("Nexus Format entered: ", nexus_format)
        if nexus_format == 'raw' and len(sys.argv) == 9:
            upload.upload_raw()
        elif nexus_format == 'npm' and len(sys.argv)  == 8:
            upload.upload_npm()
        elif nexus_format == 'maven' and len(sys.argv) == 9:
            upload.upload_maven()
        else:
            print("Nexus Repository format choosen does not have correct amount of parameters")
            print("Number of arguments entered: ", len(sys.argv))
    else:
        print("Incorrect parameters added")


if __name__ == "__main__":
    main()
