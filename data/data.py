import os


# StaticConfig
class SC:
    VERSION = "2.0"
    LANG_PATH = os.path.join(os.getcwd() + "\\lang\\")
    LANG_OPTIONS = os.listdir(LANG_PATH)
    CSV_RAW_PATH = os.path.join(os.getcwd() + "\\csv\\raw\\")
    CSV_RESULT_PATH = os.path.join(os.getcwd() + "\\csv\\result\\")
    NEW_COLUMN_NAMES = {
        "date": "Date",
        "time": "Hour",
        "catdesc": "Category",
        "direction": "Direction",
        "dstcountry": "Destination country",
        "dstip": "Destination IP",
        "dstport": "Destination port",
        "eventtype": "Event Type",
        "rcvdbyte": "Received Bytes",
        "sentbyte": "Sent Bytes",
        "srcip": "Source IP",
        "srcport": "Source port",
        "url": "URL",
        "user": "User",
    }
    COLUMNS_TO_EXTRACT = [
        "date",
        "time",
        "catdesc",
        "direction",
        "dstcountry",
        "dstip",
        "dstport",
        "eventtype",
        "rcvdbyte",
        "sentbyte",
        "srcip",
        "srcport",
        "url",
        "user",
    ]


# DynamicConfig
class DC:
    lang_text = None
    client_name = ""
    user_name = ""
    df = None
