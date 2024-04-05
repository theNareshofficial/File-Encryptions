#! /bin/python

import os

def os_name():
          name = os.name

          if name == "nt":
                    os.system("cls")
          else:
                    os.system("clear")

os_name()
