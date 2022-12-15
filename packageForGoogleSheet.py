import gspread


def getStarsList(path):
    f = open(path, 'r')
    stars = f.read()
    stars = stars.replace("*\n", '*').replace("\n", " ")
    starsArray = []
    for i in stars:
        newArray = []
        newArray.append(i)
        starsArray.append(newArray)
    return starsArray


def createBackUp(worksheet, diapason):
    backUpData = worksheet.get(diapason)
    backUpfile = open("backup.txt", "w")
    text = ""
    lastElement = False
    lastElementIndex = len(backUpData)
    for i in range(lastElementIndex):
        if (i == lastElementIndex - 1):
            lastElement = True
        if (backUpData[i] != []):
            if (backUpData[i] == ' '):
                if (lastElement == False):
                    text += '\n'
                else:
                    text += ''
            else:
                if (lastElement == False):
                    text += backUpData[i][0] + '\n'
                else:
                    text += backUpData[i][0]
        else:
            text += '\n'
    backUpfile.write(text)


def getAdressRange(adress, length):
    column = ""
    row = ""
    array = list(adress)
    for i in array:
        if str(i).isalpha():
            column += i
        else:
            row += i
    firstRow = str(int(row) + 1)
    lastRow = str(int(firstRow) + length)
    result = column + firstRow + ":" + column + lastRow
    return result


def updateTableDate(columnName, tableName, passwordFileName, nameStarsFile):
    starsList = getStarsList(nameStarsFile)
    gc = gspread.service_account(filename=passwordFileName)
    worksheet = gc.open(tableName).get_worksheet(0)
    columnCellAdress = worksheet.find(columnName).address
    diapason = getAdressRange(columnCellAdress, len(starsList) - 1)
    createBackUp(worksheet, diapason)
    worksheet.update(diapason, starsList)


def restoreBackUp(columnName, tableName, passwordFileName, nameBackUpFile):
    backedUpList = getStarsList(nameBackUpFile)
    gc = gspread.service_account(filename=passwordFileName)
    worksheet = gc.open(tableName).get_worksheet(0)
    columnCellAdress = worksheet.find(columnName).address
    diapason = getAdressRange(columnCellAdress, len(backedUpList) - 1)
    worksheet.update(diapason, backedUpList)

#restoreBackUp("Л12", "Тестовый ввод", "awesome-delight-371517-2deba832a677.json", "backup.txt")