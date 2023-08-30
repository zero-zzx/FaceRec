import os

from escpos import printer


def Print_paper(str):
    p = printer.File("/dev/ttyUSB0")
    print(p)
    p.codepage = 'gbk'
    p.image("/home/pi/Desktop/FaceRec/logo.jpg")
    p.text('\n')
    p.set(width=1, height=1)
    p.text(str)
    p.cut()
    p.close()


if __name__ == "__main__":
    Print_paper('this is the test.\n')