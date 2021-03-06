"""This is a simple utility to convert a TSV file to TSVx format. We
really would prefer a complex utility, which can do everything
automagically, but for now, simple will do.

Usage:
  tsv2tsvx [<input>] [<output>] [--delimiter=<delimeter>]
  tsv2tsvx -h | --help

Options:
  -h --help        Show this screen.

TODO:
  [--title=<title>] [--types=<types>]  [--vars=<vars>]
  --title=<title>  Add a title to the file
  --types=<types>  A comma-seperated list of types for the columns
  --vars=<vars>    A comma-seperated list of variable names
"""

import docopt
import os
import os.path
import sys

import tsvx

import tsvx.helpers
import tsvx.parser

arguments = docopt.docopt(__doc__)

inputfile = arguments["<input>"]
outputfile = arguments["<output>"]
delimiter = arguments["--delimiter"]

ofp = sys.stdout
if outputfile:
    if os.path.exists(outputfile):
        print "Error: Output file already exists. Please erase it first."
        sys.exit(-1)
    ofp = open(outputfile, "w")

ifp = sys.stdin
if inputfile:
    if not os.path.exists(inputfile):
        print "Error: Input file doesn't exist."
        sys.exit(-1)

    ifp = open(inputfile, "r")


headers = ifp.next()

if not delimiter:
    if '\t' in headers:
        delimiter = "\t"
    elif ',' in headers:
        delimiter = ","
    elif ";" in headers:
        delimiter = ";"
    elif "|" in headers:
        delimiter = "|"
    else:
        print "Headers did not contain tab, comma, semicolon, or pipe."
        print "Could not guess delimiter. Please explicitly specify delimiter"
        print "with --delimiter option"
        sys.exit(-1)

ofp.write(headers)
split_headers = headers[:-1].split(delimiter)
vars = [tsvx.helpers.variable_from_string(x) for x in split_headers]
ofp.write("\t".join(vars)+"\t(variables)\n")
(sample_line, ifp) = tsvx.helpers.peek(ifp)
type_headers = zip(*map(tsvx.parser.guess_type,
                        sample_line[:-1].split(delimiter)))
ofp.write("\t".join(type_headers[0])+"\t(types)\n")
ofp.write("\t".join(type_headers[1])+"\t(json)\n")
ofp.write("-----\n")

for line in ifp:
    # Escape quotes
    line = line.replace('"', '\\"')
    if delimiter == "\t":
        ofp.write(line)
    else:
        ofp.write("\t".join(line.split(delimiter)))

ofp.close()
