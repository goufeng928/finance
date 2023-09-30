#!/usr/bin/python
# -*- coding: UTF-8 -*-

# pip install pyperclip

import pyperclip

#获得剪贴板的内容，返回一个字符串。
text = pyperclip.paste()

print(text)

#将text写入剪贴板。
#pyperclip.copy(newtext)
