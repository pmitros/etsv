# TSVx: Enhanced TSV Format

TSV is a nice format. It's human-readable, very fast to parse, and
concise. It's possible to process as a streaming format.

It's also painfully hard to work with due to lack of
standardization. Each file requires a different set of heuristics to
load. In addition, the columns must be parsed in a different way for
every file.

If this proposal is successful, ideally, e.g. a spreadsheet would be
able to open a MySQL export without prompting the user for help, and
pandas would be able to work with both.

This is a prototype for working with an enhanced TSV format. tsvx
files are a tab-seprated format, with several extensions:

* We standardize escaping. We use JSON-style escaping.
* We standardize column types to be JSON variables. We support
  more types encoded as such
* We standardize on headers which can provide column names and type
  metadata. Columns may have types, units, and similar

This is repository includes (at the time of this writing, the start
of) a parser for such tab-separated files. 

Example file:

    title: Food inventory
    description: A sample TSVx file
    created-date: '2016-10-29T15:25:29.449640'
    generator: test.py
    ---------------------
    Food Name	Weight	Price	Expiration Date
    var:	foodname	weight	price	expiration
    types:	str	int	float	ISO8601-date
    units:	None	kg	dollars/kg	ISO8601-date
    json-types:	String	Number	Number	String
    mysql-types:	VARCHAR(80)	SMALLINT	DOUBLE	VARCHAR(20)
    ---------------------
    Tuna	300	5.13	2017-10-12
    Salmon	150	7.13	2018-10-12


The file has three sections:

* Metadata (optional)
* Headers (required)
* Data (required)

Sections are seperated by a line of all dashes, containing at least
three dashes.

The metadata is a YAML dictionary. The first line must contain a
colon. Fields defined are:

* title -- A single line title/description
* description -- A multiline description
* authors  -- JSON list of authors
* created-date -- ISO8601 date and time of when the file was created
* modified-date -- ISO8601 date and time of last modification
* generator -- Some identifier of the program or source the data came
  from

First line of the headers are human-readable column headers. Following
lines define additional information about each column. Required are
types and json-types, which say how the data ought to be
interpreted. Currently defined types are:

* int -- Integer
* float -- Floating point number, either containing a space or otherwise
* bool -- Boolean
* ISO8601-datetime -- Date and time as 2014-12-30T11:59:00.01
* ISO8601-date -- Date as 2014-12-30
* str -- JSON-encoded string (quotes omitted)

JSON types are String, Number, or Boolean.