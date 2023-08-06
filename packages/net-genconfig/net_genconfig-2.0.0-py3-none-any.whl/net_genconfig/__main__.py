# net_genconfig.__main__


import net_genconfig

import argparse
from copy import copy, deepcopy
import datetime
import jinja2
import os
import re
import sys
import yaml

from deepops import deepmerge, deepremoveitems

from net_genconfig import netaddr_filter

from net_inventorylib import NetInventory



# --- functions ---



def generate_config(devicename):
    """Generate the configuration for the specified device and write it
    to either standard output or a file, depending on the command line
    options specified.

    Returns True if the configuration is generated successfully.  If
    there is a problem of some sort which is not serious enough to
    abort the script (such as one device cannot be found), the function
    will return False.  More serious problems will stop the entire
    script.
    """


    # configuration


    if devicename not in inventory["devices"]:
        print("warning: device not found in inventory: %s - skipping"
                  % devicename,

              file=sys.stderr)

        return False


    # get the definition dictionary for this device from the inventory
    #
    # we use this variable for some checks here, and to pass it to the
    # starting role template, so it avoids repeatedly fetching it

    device = inventory["devices"][devicename]

    if device is None:
        print("warning: device definition empty: %s - skipping" % devicename,
              file=sys.stderr)

        return False


    # if the dump device option is enabled, print a YAML version of the
    # device definition (now we've done merges, etc.) to stdout and
    # return

    if dump_device:
        print(yaml.dump(device, default_flow_style=False))
        return True


    # we need a role and platform to read in the template file

    if "role" not in device:
        print("error: missing role for device: %s" % devicename,
              file=sys.stderr)

        exit(1)

    if "platform" not in device:
        print("error: missing platform for device: %s" % devicename,
              file=sys.stderr)

        exit(1)

    role = device["role"]
    platform = device["platform"]


    # generate


    if debug:
        print("debug: generating configuration for: %s role: %s "
                  "platform: %s" % (devicename, role, platform),
              file=sys.stderr)


    if not os.path.isdir(roles_dirname):
        print("error: role directory does not exist: %s" % roles_dirname,
              file=sys.stderr)

        exit(1)

    if not os.path.isdir(include_dirname):
        print("error: include directory does not exist: %s" % include_dirname,
              file=sys.stderr)

        exit(1)


    if not os.path.isdir(os.path.join(roles_dirname, platform)):
        print("error: platform not found: %s used for device: %s"
                  % (platform, devicename), file=sys.stderr)

        exit(1)


    # read the template file

    role_filename = os.path.join(platform, role) + ".j2"

    if debug:
        print("debug: using role file (relative to filesystem loader "
                  "directory): %s" % role_filename,
               file=sys.stderr)

    try:
        template = env.get_template(role_filename)

    except jinja2.exceptions.TemplateNotFound:
        print("error: role not found: %s for platform: %s" % (role, platform),
              file=sys.stderr)

        exit(1)


    # render the template

    config = template.render(devicename=devicename, device=device,
                             inventory=inventory, **vars)


    # return, if output is disabled

    if no_output:
        if debug:
            print("debug: output disabled", file=sys.stderr)

        return True


    # if not disabled, squash blank lines

    if not no_squash_blanklines:
        # remove any blank lines at the top
        config = re.sub(r"^\n+", "", config)

        # squash three or more blank lines into two (a single blank
        # line)
        config = re.sub(r"\n\n\n+", r"\n\n", config)

        # the last line should end with a single newline
        config = re.sub(r"\n\n+$", r"\n", config)


    # write output to either standard output or a file, depending on
    # the options specified

    if output_filename:
        output_filename_expanded = output_filename.replace("%", devicename)

        if debug:
            print("debug: writing to output file: %s"
                      % output_filename_expanded,
                  file=sys.stderr)

        with open(output_filename_expanded, "w") as output_file:
            print(config, file=output_file)

    else:
        if debug:
            print("debug: writing to standard output", file=sys.stderr)

        print(config)


    # generation succeeded

    return True



# --- global helper functions ---



# dictionary of global helper functions to be added to the Jinja2
# environment; as each function is defined, they are added to this and
# then it iterated through, to extend the environment later
#
# the list is initialised to include some functions which are imported

global_helpers = {
    "deepcopy": deepcopy,
    "deepmerge": deepmerge,
    "deepremoveitems": deepremoveitems
}



def warn_helper(msg):
    """Helper function to print a warning inside a Jinja2 template.
    The supplied message is printed to stderr but execution is not
    stopped.

    Keyword arguments:

    msg -- warning message to display
    """

    print("warning: " + msg, file=sys.stderr)


    # helper functions return a string to be included in the template;
    # we don't particularly have anything to include but have to return
    # something, so we return an empty string

    return ""


global_helpers["warn"] = warn_helper



def raise_helper(msg):
    """Helper function to raise an exception inside a Jinja2 template.
    The generic 'Exception' class is raised in Python.

    Keyword arguments:

    msg -- exception message to display when aborting
    """

    raise Exception(msg)


global_helpers["raise"] = raise_helper



def assert_helper(condition, msg):
    """Helper function for assertions inside a Jinja2 template.  If the
    supplied condition is False, an exception is raised with the given
    error message.  The 'AssertionError' class is raised by Python.

    If the condition is True, an empty string is returned to avoid
    printing anything.

    Keyword arguments:

    condition -- the condition which must be satisfied to not raise the
    exception

    msg -- message to display in the event of the condition not being
    true
    """

    if not condition:
        raise AssertionError(msg)

    return ""


global_helpers["assert"] = assert_helper



def re_match_helper(pattern, string):
    """Helper function for matching strings against regular expressions
    in a Jinja2 template: a boolean is returned, indicating whether the
    match succeeded or not.

    This is a wrapper around re.match().

    Keyword arguments:

    pattern -- the regular expression to match against

    string -- the string to match against
    """

    return bool(re.match(pattern, string))


global_helpers["re_match"] = re_match_helper



def re_match_group_helper(pattern, string, *groups):
    """Helper function for matching strings against regular expressions
    and extract selected groups (marked by parentheses) of text in a
    Jinja2 template, returning them in the form of a tuple, one for
    each group, in order.

    The desired groups are identified either by number (0 for the first
    one, by opening bracket, 1 for the second, etc.) or by name (using
    the syntax '(?P<name>...)'.  These styles can be mixed.

    This is a wrapper around re.match().group() (re.match() returns a
    Match object and group() is called on that).

    Keyword arguments:

    pattern -- the regular expression to match against; the required
    groups to return should be specified using parentheses

    string -- the string to match and return the groups of

    *groups -- a list of arguments giving the numbers or names of the
    desired match groups
    """

    r = re.match(pattern, string)

    if r is None:
        raise ValueError("re_match_group() string: %s does not "
                         "match pattern: %s"
                             % (repr(string), repr(pattern)))

    return r.group(*groups)


global_helpers["re_match_group"] = re_match_group_helper



def re_match_groups_helper(pattern, string):
    """Helper function for matching strings against regular expressions
    and extract groups (marked by parentheses) of text in a Jinja2
    template, returning them in the form of a tuple, one for each pair.

    The caller can extract the desired one by indexing the tuple.  To
    select an arbitrary list of groups (by name),
    re_match_group_helper() is more useful.

    This is a wrapper around re.match().groups() (re.match() returns a
    Match object and groups() is called on that).

    Keyword arguments:

    pattern -- the regular expression to match against; the required
    groups to return should be specified using parentheses

    string -- the string to match and return the groups of
    """

    r = re.match(pattern, string)

    if r is None:
        raise ValueError("re_match_groups() string: %s does not "
                         "match pattern: %s"
                             % (repr(string), repr(pattern)))

    return r.groups()


global_helpers["re_match_groups"] = re_match_groups_helper



def to_list_helper(s):
    """Helper function to make a list from the lines in a multiline
    string: each line is added as an item to the list.

    Blank lines (including ones consiting entirely of spaces) are
    skipped, as well as leading and trailing spaces on the remaining
    lines.

    The function is useful to get more complex data structures back
    from Jinja2 macros (which can only return text).
    """

    l = []

    for i in s.split("\n"):
        i = i.strip()
        
        # only add to the list, if the line is not blank
        if i:
            l.append(i)

    return l


global_helpers["to_list"] = to_list_helper



def to_set_helper(s):
    """Helper function to make a set from the lines in a multiline
    string: each line is added as an item to the list.

    Blank lines (including ones consiting entirely of spaces) are
    skipped, as well as leading and trailing spaces on the remaining
    lines.

    The function is useful to get more complex data structures back
    from Jinja2 macros (which can only return text).
    """

    t = set()

    for i in s.split("\n"):
        i = i.strip()
        
        # only add to the list, if the line is not blank
        if i:
            t.add(i)

    return t


global_helpers["to_set"] = to_set_helper



def to_dict_helper(s):
    """Helper function to make a dictionary from a string: the lines of
    the string are parsed in the form 'key:value' and used to populate
    a dictionary that is returned.

    Blank lines (including ones consisting entirely of spaces) are
    skipped, as well as leading and trailing spaces in the key and
    value.

    The function is useful to get more complex data structures back
    from Jinja2 macros (which can only return text).
    """

    d = {}
    
    for i in s.split("\n"):
        # skip blank lines (including ones just composed of spaces)
        if not i.strip():
            continue

        try:
            k, v = i.split(":", 1)
        except ValueError:
            raise(ValueError(
                "failed parsing 'key:value' from line: %s" % repr(i)))

        # store the key:value in the dictionary, trimming spaces
        d[k.strip()] = v.strip()

    return d


global_helpers["to_dict"] = to_dict_helper



# --- command line arguments ---



# create the parser and add in the available command line options

parser = argparse.ArgumentParser(
    # override the program name as running this as a __main__ inside a
    # module directory will use '__main__' by default - this name isn't
    # necessarily correct, but it looks better than that
    prog="net-genconfig",

    # we want the epilog help output to be printed as it and not
    # reformatted or line wrapped
    formatter_class=argparse.RawDescriptionHelpFormatter)


parser.add_argument(
    "-C", "--config",
    dest="config_dirname",
    default=(os.environ.get("NET_CONFIG_DIR")
                 if "NET_CONFIG_DIR" in os.environ else "."),
    help="base directory for roles, include and inventory")

parser.add_argument(
    "-r", "--roles",
    dest="roles_dirname",
    default="roles",
    help="directory containing role configuration templates")

parser.add_argument(
    "-n", "--include",
    dest="include_dirname",
    default="include",
    help="directory containing included templates / macro libraries")

parser.add_argument(
    "-i", "--inventory",
    dest="inventory_dirname",
    default="inventory",
    help="directory containing inventory of devices, networks, etc.")

parser.add_argument(
    "-o", "--output",
    dest="output_filename",
    help="write configuration to named file instead of stdout; '%%' "
         "can be used to substitute in the name of the device into "
         "the filename")

parser.add_argument(
    "-O", "--no-output",
    action="store_true",
    help="generate the configuration but do not output it - useful to "
         "test generation succeeds")

parser.add_argument(
    "-S", "--no-squash-blanklines",
    action="store_true",
    help="disable the squashing of leading and trailing, as well as "
         "multiple, consecutive blank lines (prevent equivalent of "
         "'| cat -s') in output")

parser.add_argument(
    "-E", "--list-env",
    action="store_true",
    help="list filter and global helper functions and stop (this will "
          "include the standard Jinja2, as well as the netaddr module "
          " and custom ones)")

parser.add_argument(
    "-I", "--dump-inventory",
    action="store_true",
    help="dump complete read inventory in YAML to stdout and stop, "
         "without generating any configurations")

parser.add_argument(
    "-U", "--dump-device",
    action="store_true",
    help="dump resulting device definition in YAML to stdout, after "
         "merging profiles and stop, without generating any "
         "configurations")

parser.add_argument(
    "-d", "--define",
    action="append",
    nargs=2,
    default=[],
    help="define variable for use in the template",
    metavar=("VAR", "VALUE"))

parser.add_argument(
    "-q", "--quiet",
    action="store_true",
    help="when generating configuration for multiple devices, don't "
         "print the name of each device, as it's generated")

parser.add_argument(
    "-D", "--debug",
    action="store_true",
    help="enable debug mode")

parser.add_argument(
    "devicename",
    nargs="*",
    help="name(s) of the device(s) to generate the configuration for")

parser.add_argument(
    "--version",
    action="version",
    version=("%(prog)s " + net_genconfig.__version__))


# parse the supplied command line against these options, storing the
# results

args = parser.parse_args()

roles_dirname = os.path.join(args.config_dirname, args.roles_dirname)
include_dirname = os.path.join(args.config_dirname, args.include_dirname)
inventory_dirname = os.path.join(args.config_dirname, args.inventory_dirname)
output_filename = args.output_filename
no_output = args.no_output
no_squash_blanklines = args.no_squash_blanklines
list_env = args.list_env
dump_inventory = args.dump_inventory
dump_device = args.dump_device
quiet = args.quiet
devicenames = args.devicename
debug = args.debug

vars = {}
for var, value in args.define:
    vars[var] = value


if debug:
    print("""\
debug: roles directory: %s
debug: include directory: %s
debug: inventory directory: %s
debug: output filename: %s
debug: device names: %s"""
              % (roles_dirname, include_dirname, inventory_dirname,
                 output_filename, devicenames),
          file=sys.stderr)


# check a couple of nonsensical configurations aren't being use related
# to multiple devices

if (len(devicenames) > 1) and (not (no_output or dump_device)):
    if not output_filename:
        print("error: multiple device names specified but outputting "
                  "to standard output - all configurations would be "
                  "concatenated",
              file=sys.stderr)

        exit(1)


    elif output_filename.find("%") == -1:
        print("error: multiple device names specified but output "
                  "filename does not contain a '%' to substitute the "
                  "device name - output file would be overwritten",
              file=sys.stderr)

        exit(1)



# --- inventory ---



if debug:
    print("debug: starting to read inventory directory", file=sys.stderr)



# read in the inventory

inventory_obj = NetInventory(inventory_dirname, debug=debug)

inventory = inventory_obj.get()


if dump_inventory:
    print(yaml.dump(inventory, default_flow_style=False))
    exit(0)


if "devices" not in inventory:
    print("error: no devices found in inventory", file=sys.stderr)
    exit(1)



# --- jinja2 ---



# build the Jinja2 environment

jinja_fsloader_dirs = [roles_dirname, include_dirname]

if debug:
    print("debug: creating environment with filesystem loader directories: "
          "%s" % jinja_fsloader_dirs)

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(jinja_fsloader_dirs),
    extensions=[
        "jinja2.ext.do", "jinja2.ext.loopcontrols", "jinja2.ext.with_"],
    trim_blocks=True)


# add in the special warn(), raise() and assert() functions, as well as
# some other functions we need, into the Jinja2 environment

for global_helper in global_helpers:
    env.globals[global_helper] = global_helpers[global_helper]


# add in the netaddr library functions as additional filters

for filter_name, filter_func in (
    netaddr_filter.FilterModule().filters().items()):

    env.filters[filter_name] = filter_func


# if the 'list environment' option is specified, print out the filter
# and global helper functions and stop

if list_env:
    print("Filters:")
    for filter in sorted(env.filters):
        print("  " + filter)

    print()

    print("Global helpers:")
    for global_helper in sorted(env.globals):
        print("  " + global_helper)

    exit(0)



# --- generate ---



# go through all the devices specified, generate and write out their
# configurations

if not devicenames:
    print("warning: no device names specified", file=sys.stderr)


# this flag will change to False if any configuration fails to generate
# and is used to affect the return code from the script

complete_success = True


for devicename in devicenames:
    if (not quiet) and (len(devicenames) > 1):
        print(devicename)

    complete_success &= generate_config(devicename)


exit(0 if complete_success else 1)
