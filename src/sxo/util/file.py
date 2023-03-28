# -*- coding: utf-8 -*-
def save(fnm: str, text: str):
    file = open(fnm, "w")
    file.write(text)
    file.close()
