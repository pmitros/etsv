'''Dump a MySQL database to a directory of TSVx files

Usage:
  mysql_tsvx.py --host=host --user=user --port=port
                --password=password --database=database
                [--output=directory] [--overwrite]
                [--max-step=maximum-step] [--row-limit=row-limit]
'''

import MySQLdb
import docopt
import subprocess
import sys
import os
import os.path

import helpers

arguments = docopt.docopt(__doc__)
cursor = helpers.mysql_connect(arguments)
database = arguments["--database"]

if not arguments["--output"]:
    directory = database+"-tsvx-dump"
else:
    directory = arguments["--output"]

print "Saving to " + directory

if os.path.exists(directory) and not arguments["--overwrite"]:
    print "Directory %s exists" % (filename)
    sys.exit(-1)
elif not os.path.exists(directory):
    os.mkdir(directory)

cursor.execute("show tables;")
for table in cursor:
    table = table[0]
    filename = os.path.join(directory, table + ".tsvx")
    print filename
    helpers.scrape_mysql_table_to_tsvx(
        filename, cursor, arguments["--database"], table,
        arguments["--row-limit"], arguments["--max-step"]
    )
