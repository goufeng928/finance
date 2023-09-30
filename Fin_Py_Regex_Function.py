import re
import pyperclip

def LongTextToShortText(LongText):

    Regex_Line = ".*\s\s"

    Regex_Line = Regex_Line * 6

    ShortText = re.findall("聚丙烯.*" + Regex_Line, LongText)

    return ShortText

def PerXLineVerify(LongText, X):

    LongText = LongText.replace('\r', '')
    
    LineList = LongText.split('\n')

    NewList = []

    for i in range(0, len(LineList) - 1):

        NewList.append(LineList[i])

        if len(NewList) == X:

            NewString = '\n'.join(NewList)


if __name__ == "__main__":

    LongText = pyperclip.paste()

    print(LongText)

    PerXLineVerify(LongText, 8)
