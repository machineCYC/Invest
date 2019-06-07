

def deleteComma(strNumber):
    try:
        return strNumber.replace(",", "")
    except:
        return str(strNumber).replace(",", "")