# Function to print software title and it's version
import os
from urllib.parse import urlparse
from data.data import SC,DC


def printSoftwareTitle():
    print(f"FortiAnalyser - User CSV Formater {SC.VERSION}")
    print("")


# Function to extract the FQDN from the URL
def extractFqdn(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc


# Function to convert bytes to MB or GB
def convertToMbOrGb(bytes):
    gb = 1073741824
    mb = 1048576

    if bytes > gb:
        return str(round(bytes / gb, 2)) + " GB"
    elif bytes > 104857:
        return str(round(bytes / mb, 2)) + " MB"
    else:
        return str(bytes) + " Bytes"


# Function to clear the screen
def clearScreen():
    os.system("cls")


def printSuccessText():
    print(f"{DC.lang_text["finished"]}")
    print(f"All CSVs successfully generated!")
    input("Press ENTER to exit...")
