#!/usr/python3
import argparse
import requests
import os
import time
import sys
time_start = time.time()

def log(obj, newline=True):
    global args
    if args.v:
        if newline:
            print(obj, flush=True)
        else:
            print(obj, end="", flush=True)

parser = argparse.ArgumentParser(
    description="download a list of objects from ruscorpora's parallel corpus")
parser.add_argument(
    'list', default=sys.stdin, type=argparse.FileType('r'),
    help='file to read objects from')
parser.add_argument(
    'output', metavar='out', type=str,
    help='the output folder')
parser.add_argument(
    '-v', "--verbose", action='store_true',
    help='print status information')

args = parser.parse_args()
log("Arguments parsed.")
log("Loading input file... ", newline=False)
list = [i.split(" ") for i in args.output.read().split("\n")]
log("done.")

log("Making directory `" + args.output + "`...", newline=False)
try:
    os.makedir(args.output)
    log("done.")
except FileExistsError:
    log("FAILED - USING EXISTING.")
os.chdir(args.output)
log("Switched directory to `" + args.output + "`.")
log("Starting list evaluation... ", newline=False)
for i in list:
    log("done.")
    log("Opening file `" + i[0] + ".html` for writing... ")
    with open(i[0]+".html", "w") as file:
        log("Composing URL... ", newline=False)
        url = "http://search2.ruscorpora.ru/search.xml?dpp=&spp=&spd=&text=lexgramm&mode=para&sort=gr_tagging&env=alpha&"
        for j,k in zip(i[1:], range(1, len(i))):
            url += "&parent{n}=0&level{n}=0&lex{n}={text}&gramm{n}=&flags{n}=&sem{n}=".format(text=j, n=k)
        log("Composed URL is: `"+url+"`.")
        log("Sending request... ", newline=False)
        with requests.get(url) as request:
            log("done.")
            log("Writing file... ", newline=False)
            file.write(request.content)
            log("done.")
            log("Closing file... ", newline=False)
log("done.")
time_spent = time.time() - time_start
log("---DONE---")
time_spent = int(time_spent)
m, s = divmod(time_spent, 60)
h, m = divmod(m, 60)
log("Time used: " + "%d:%02d:%02d" % (h, m, s) + "(" + str(time_spent) + ")")
