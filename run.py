import os
import pandas as pd
from urllib.parse import urlparse
import json

# Function to print software title and it's version
def printSoftwareTitle():
    print(f"FortiAnalyser - User CSV Formater {SC.VERSION}")
    print("")

# Function to get the languague title from the .json lang file
def getLanguageFromFile(file_name):
    file_path = os.path.join(SC.LANG_PATH, file_name)
    with open(file_path, "r", encoding="utf-8") as infile:
        data = json.load(infile)
        return data.get("language")

# Function to load the software language
def loadLanguage():
    printSoftwareTitle()
    for index, option in enumerate(SC.LANG_OPTIONS):
        file_name = getLanguageFromFile(option)
        print(f"[{index + 1}] - {file_name}")

    lang_code = int(input("Choose you language: ")) or 1

    language = ""
    for index, option in enumerate(SC.LANG_OPTIONS):
        if lang_code == index + 1:
            language = option 

    language_path = os.path.join(SC.LANG_PATH + language)

    with open(language_path, "r", encoding="utf-8") as infile:
        DC.lang_text = json.load(infile)


# Function to get client data do generate the CSV file names later on
def getClientData():
    printSoftwareTitle()
    print(DC.lang_text["raw_file_path_warning"])
    print(DC.lang_text["result_file_path_warning"])
    print("")
    DC.client_name = str(input(DC.lang_text["insert_client_name"]))
    DC.user_name = str(input(DC.lang_text["insert_user_name"]))
    print("")
    print(DC.lang_text["generating_text"])
    print("")


# Function to get the most recent raw file in the raw directory
def getCsvData():
    highest_timestamp = 0
    most_recent_file = ""
    files = os.listdir(SC.CSV_RAW_PATH)

    for file in files:
        current_file_path = os.path.join(SC.CSV_RAW_PATH + file)
        file_timestamp = os.path.getctime(current_file_path)
        if file_timestamp > highest_timestamp:
            highest_timestamp = file_timestamp
            most_recent_file = current_file_path

    DC.df = pd.read_csv(most_recent_file, header=None)


# Function to add the columns names to the final CSV
def addColumnNamesToCsv():
    DC.df.columns = SC.COLUMN_NAMES


# Function to remove columns that will not be used in the final CSV
def removeUnnecessaryColumns():
    DC.df = DC.df.drop(columns=SC.COLUMNS_TO_REMOVE)


# Function to change the column names in the final CSV. Column names are changed for better readability
def changeColumnNames():
    DC.df.rename(columns=SC.NEW_COLUMN_NAMES, inplace=True)


# Function to clear CSV rows as FAZ raw files comes very dirty and very hard to read
def cleanCsv():
    DC.df = DC.df.apply(cleanRow, axis=1)


# Function to actually clear the rows
def cleanRow(raw_row):
    clean_row_dict = {}

    for row_entry in raw_row.index:
        clean_value = raw_row[row_entry]
        if "=" in str(clean_value):
            key, clean_value = clean_value.split("=", 1)
            if '"' in clean_value:
                clean_value = clean_value.split('"')[1]
        clean_row_dict[row_entry] = clean_value

    return pd.Series(clean_row_dict)


# Function to generate the CSV with all details
def generateFullCsv():
    file_name = f"\\{DC.client_name} - {DC.lang_text["most_accessed_websites_for_the_user"]} {DC.user_name} - {DC.lang_text['full_list']}.csv"
    full_file_path = os.path.join(SC.CSV_RESULT_PATH + file_name)
    DC.df.to_csv(full_file_path, index=False)


# Function to generate the CSV with only information about what FQDNs the user accessed, it's hit count and web usage
def generateShortCsv():
    df = DC.df.copy()
    df["FQDN"] = DC.df["URL"].apply(extractFqdn)
    df["Received Bytes"] = df["Received Bytes"].astype(int)
    df["Sent Bytes"] = df["Sent Bytes"].astype(int)
    df["Total Usage"] = df["Received Bytes"] + df["Sent Bytes"]

    website_data = (
        df.groupby("FQDN")
        .agg(hit_count=("FQDN", "size"), total_usage=("Total Usage", "sum"))
        .reset_index()
        .sort_values(by="hit_count", ascending=False)
    )

    website_data["total_usage"] = website_data["total_usage"].apply(convertToMbOrGb)
    website_data = website_data[["FQDN", "hit_count", "total_usage"]]
    website_data.columns = ["FQDN", "Hit Count", "Total Usage"]

    file_name = f"\\{DC.client_name} - {DC.lang_text['most_accessed_websites_for_the_user']} {DC.user_name} - {DC.lang_text['short_list']}.csv"
    full_file_path = os.path.join(SC.CSV_RESULT_PATH + file_name)
    website_data.to_csv(full_file_path, index=False)


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


# Run
if __name__ == "__main__":
    from data.data import SC, DC

    loadLanguage()
    clearScreen()
    getClientData()
    getCsvData()
    addColumnNamesToCsv()
    removeUnnecessaryColumns()
    changeColumnNames()
    cleanCsv()
    generateFullCsv()
    generateShortCsv()
