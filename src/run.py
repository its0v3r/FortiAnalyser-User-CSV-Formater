# Run
if __name__ == "__main__":
    from data.data import SC, DC
    from app.general_def import (
        loadLanguage,
        getClientData,
        getCsvData,
        getImportantColumns,
        changeColumnNames,
        cleanCsv,
        generateFullCsv,
        generateShortCsv,
    )
    from app.utils_def import clearScreen, printSuccessText

    loadLanguage()
    clearScreen()
    getClientData()
    getCsvData()
    getImportantColumns()
    changeColumnNames()
    cleanCsv()
    generateFullCsv()
    generateShortCsv()
    printSuccessText()
