######################################################################
# 
# File: __init__.py
# 
# Copyright 2011 Brian Beach, All Rights Reserved.
# 
# This software is licensed under the MIT license.
# 
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
######################################################################

"""
Command to run jslint on all of the files listed on the command line.

The JSLint code from github just contains the JSLINT function; it
doesn't do any reporting, so we have to add our own reporting script.

The other annoying thing is that the Javascript intepreter from
Spidermonkey doesn't have any file i/o.  To get around this we package
up the source files to examine as string constants in generated
Javascript code.
"""

import fileinput
import os.path
import StringIO
import subprocess
import sys

JSLINT_SOURCE_FILE = os.path.join(os.path.dirname(__file__), 'fulljslint.js')

REPORT_FUNCTION = """
//
// JSLINT_OPTIONS
//
// The options we set for jslint.
//

var JSLINT_OPTIONS = %s;

//
// jslintOneFile
//
// Runs JSLint on a string that is the contents of a source code file,
// and prints out any errors that were found.
//

var jslintOneFile = function (fileName, fileContents) {
    var i, error, global, implied;
    JSLINT(fileContents, JSLINT_OPTIONS);
    data = JSLINT.data();
    if (data.errors) {
        for (i = 0; i < data.errors.length; i++) {
            var error = data.errors[i];
            if (error) {
                print(fileName + " " + error.line + ": " + error.reason);
                print(error.evidence);
                print("");
            }
        }
    }
    if (data.implieds) {
	for (i = 0; i < data.implieds.length; i++) {
	    var implied = data.implieds[i];
            if (implied) {
                print(fileName + " " + implied.line + ": implied global '" + implied.name + "'");
                print("");
            }
	}
    }
    if (data.unused) {
	for (i = 0; i < data.unused.length; i++) {
	    var unused = data.unused[i];
            if (unused) {
                print(fileName + " " + unused.line + ": unused variable '" + unused.name + "'");
                print("");
            }
	}
    }
};
"""

def read_file(file_name):
    with open(file_name, 'r') as f:
        return f.read()

def file_contents_as_string_constant(file_name):
    """
    Returns the contents of the given file as a string constant that
    can be included in a Javascript program.  Backslashes, quotes, and
    newlines all need to be escaped.
    """
    file_contents = read_file(file_name)
    file_contents = file_contents.replace('\\', '\\\\')
    file_contents = file_contents.replace('"', '\\"')
    file_contents = file_contents.replace('\n', '\\n')
    return '"' + file_contents + '"'

def generate_javascript(options):
    """
    Writes a complete Javascript program to run jslint on all of the
    files listed on the command line.
    """
    out = StringIO.StringIO()
    # First, the JSLINT function
    out.write(read_file(JSLINT_SOURCE_FILE));
    # Next, our reporting function
    out.write(REPORT_FUNCTION % options)
    # Finally, run the reporting function on each of the input files.
    for file_name in sys.argv[1:]:
        out.write('jslintOneFile("%s", ' % file_name)
        out.write(file_contents_as_string_constant(file_name))
        out.write(');\n')
    # Return the whole thing
    return out.getvalue()

def main():
    options = "undefined";
    if len(sys.argv) > 1 and sys.argv[1] == '--options':
        options = sys.argv[2]
        del sys.argv[1:3]
    p = subprocess.Popen(
        'js',
        stdin = subprocess.PIPE,
        stdout = subprocess.PIPE,
        stderr = subprocess.STDOUT
        )
    (out, err) = p.communicate(generate_javascript(options))
    assert err == None
    sys.stdout.write(out)
    if out == '':
        sys.exit(0)
    else:
        sys.exit(1)

