
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f --foo', help='f test start')
parser.add_argument('-b --boo', help='b test start')
args = parser.parse_args()
