#!/usr/bin/python
import sys, glob, os, subprocess

def usage():
    print """Usage:
    python topdf.py /input/dir/ <input format> /output/dir/
    e.g. python topdf.py /Users/steve/Downloads/ ppt /Users/steve/Desktop/
"""

def validate_args(args):
    if len(args) == 1 or args[1] in ["?", "-h", "--help"]:
        usage()
        return False
    print "Checking arguments."
    if len(args) != 4:
        print "Error: Invalid number of arguments; see usage."
        return False
    ret_val = True
    if not os.path.exists(args[1]):
        print "Error: %s doesn't exist." % args[1]
        ret_val = False
    elif not glob.glob("%s*.%s" % (args[1], args[2])):
        print "Error: No %s files exist in %s." % (args[2], args[1])
        ret_val = False
    if not os.path.exists(args[3]):
        print "Error: %s doesn't exist." % args[3]
        ret_val = False
    return ret_val


def main(args):
    if not validate_args(args):
        sys.exit(1)
    files = glob.glob("%s*.%s" % (args[1], args[2]))
    print "Running conversion for %s file(s)." % len(files)
    subprocess.Popen("rm -rf /tmp/topdf ; mkdir /tmp/topdf/", shell=True, stdout=subprocess.PIPE).stdout.read()
    for f in files:
        subprocess.Popen("qlmanage -p -o /tmp/topdf/ %s" % f, shell=True, stdout=subprocess.PIPE).stdout.read()
    html_files = glob.glob("/tmp/topdf/*/Preview.html")
    for h in html_files:
        output_path = args[3] + h.split("/")[3].split(".")[0] + ".pdf"
        subprocess.Popen("wkhtmltopdf %s %s" % (h, output_path), shell=True, stdout=subprocess.PIPE).stdout.read()
    print "Conversion finished."


main(sys.argv)