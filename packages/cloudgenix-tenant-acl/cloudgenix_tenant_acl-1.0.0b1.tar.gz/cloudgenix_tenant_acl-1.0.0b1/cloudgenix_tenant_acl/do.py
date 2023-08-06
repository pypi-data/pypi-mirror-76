#!/usr/bin/env python
import sys
import os
import argparse

####
#
# Enter other desired optional system modules here.
#
####

import json
from .pull import pull_acl
from . import GLOBAL_MY_SCRIPT_VERSION

####
#
# End other desired system modules.
#
####

# Import CloudGenix Python SDK
try:
    import cloudgenix
    jdout = cloudgenix.jdout
    jd = cloudgenix.jd
except ImportError as e:
    cloudgenix = None
    sys.stderr.write("ERROR: 'cloudgenix' python module required. (try 'pip install cloudgenix').\n {0}\n".format(e))
    sys.exit(1)

# Get AUTH_TOKEN/X_AUTH_TOKEN from env variable, if it exists. X_AUTH_TOKEN takes priority.
if "X_AUTH_TOKEN" in os.environ:
    CLOUDGENIX_AUTH_TOKEN = os.environ.get('X_AUTH_TOKEN')
elif "AUTH_TOKEN" in os.environ:
    CLOUDGENIX_AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
else:
    # not set
    CLOUDGENIX_AUTH_TOKEN = None

try:
    # Also, separately try and import USERNAME/PASSWORD from the config file.
    from cloudgenix_settings import CLOUDGENIX_USER, CLOUDGENIX_PASSWORD

except ImportError:
    # will get caught below
    CLOUDGENIX_USER = None
    CLOUDGENIX_PASSWORD = None


# Handle differences between python 2 and 3. Code can use text_type and binary_type instead of str/bytes/unicode etc.
if sys.version_info < (3,):
    text_type = unicode
    binary_type = str
else:
    text_type = str
    binary_type = bytes


####
#
# Start custom modifiable code
#
####

GLOBAL_MY_SCRIPT_NAME = "Do ACL"


def do_acl(sdk, new_ipv4_list):
    """
    Download, update ACL.
    :param sdk: Authenticated CloudGenix SDK
    :param new_ipv4_list: new ipv4 list to use.
    :return: Boolean status, old_ipv4_list
    """

    tenant_template = pull_acl(sdk, whole_resp=True)

    old_ipv4_list = tenant_template.get('ipv4_list', [])

    # update template
    tenant_template['ipv4_list'] = new_ipv4_list

    # send the update
    resp = sdk.patch.tenants(tenant_template)
    cloudgenix.jd(tenant_template)

    if not resp.cgx_status:
        sdk.throw_error("Failed to PATCH tenant ACL", resp)

    return old_ipv4_list

####
#
# End custom modifiable code
#
####
# Start the script.


def go():
    """
    Stub script entry point. Authenticates CloudGenix SDK, and gathers options from command line to run do_site()
    :return: No return
    """

    # Parse arguments
    parser = argparse.ArgumentParser(description="{0} ({1})".format(GLOBAL_MY_SCRIPT_NAME, GLOBAL_MY_SCRIPT_VERSION))

    ####
    #
    # Add custom cmdline argparse arguments here
    #
    ####

    custom_group = parser.add_argument_group('custom_args', 'Do ACL Options')
    custom_group.add_argument("--input", help="ACL file to Apply to controller",
                              required=True)
    custom_group.add_argument("--archive", help="File name to save previous ACL to",
                              default=None)
    custom_group.add_argument("--no-client-login", help="Don't prompt for client login if ESP/MSP. "
                                                        "Act on ACL on the ESP/MSP.",
                              default=False, action='store_true')

    ####
    #
    # End custom cmdline arguments
    #
    ####

    # Standard CloudGenix script switches.
    controller_group = parser.add_argument_group('API', 'These options change how this program connects to the API.')
    controller_group.add_argument("--controller", "-C",
                                  help="Controller URI, ex. https://api.elcapitan.cloudgenix.com",
                                  default=None)

    login_group = parser.add_argument_group('Login', 'These options allow skipping of interactive login')
    login_group.add_argument("--email", "-E", help="Use this email as User Name instead of cloudgenix_settings.py "
                                                   "or prompting",
                             default=None)
    login_group.add_argument("--password", "-PW", help="Use this Password instead of cloudgenix_settings.py "
                                                       "or prompting",
                             default=None)
    login_group.add_argument("--insecure", "-I", help="Do not verify SSL certificate",
                             action='store_true',
                             default=False)
    login_group.add_argument("--noregion", "-NR", help="Ignore Region-based redirection.",
                             dest='ignore_region', action='store_true', default=False)

    debug_group = parser.add_argument_group('Debug', 'These options enable debugging output')
    debug_group.add_argument("--sdkdebug", "-D", help="Enable SDK Debug output, levels 0-2", type=int,
                             default=0)

    args = vars(parser.parse_args())

    sdk_debuglevel = args["sdkdebug"]

    # Build SDK Constructor
    if args['controller'] and args['insecure']:
        sdk = cloudgenix.API(controller=args['controller'], ssl_verify=False)
    elif args['controller']:
        sdk = cloudgenix.API(controller=args['controller'])
    elif args['insecure']:
        sdk = cloudgenix.API(ssl_verify=False)
    else:
        sdk = cloudgenix.API()

    # check for region ignore
    if args['ignore_region']:
        sdk.ignore_region = True

    # SDK debug, default = 0
    # 0 = logger handlers removed, critical only
    # 1 = logger info messages
    # 2 = logger debug messages.

    if sdk_debuglevel == 1:
        # CG SDK info
        sdk.set_debug(1)
    elif sdk_debuglevel >= 2:
        # CG SDK debug
        sdk.set_debug(2)

    # login logic. Use cmdline if set, use AUTH_TOKEN next, finally user/pass from config file, then prompt.
    # figure out user
    if args["email"]:
        user_email = args["email"]
    elif CLOUDGENIX_USER:
        user_email = CLOUDGENIX_USER
    else:
        user_email = None

    # figure out password
    if args["password"]:
        user_password = args["password"]
    elif CLOUDGENIX_PASSWORD:
        user_password = CLOUDGENIX_PASSWORD
    else:
        user_password = None

    # client login
    no_client_login = args['no_client_login']

    # check for token
    if CLOUDGENIX_AUTH_TOKEN and not args["email"] and not args["password"]:
        sdk.interactive.use_token(CLOUDGENIX_AUTH_TOKEN)
        if sdk.tenant_id is None:
            print("AUTH_TOKEN login failure, please check token.")
            sys.exit(1)

    else:
        while sdk.tenant_id is None:
            sdk.interactive.login(user_email, user_password,
                                  client_login=False if no_client_login else True)
            # clear after one failed login, force relogin.
            if not sdk.tenant_id:
                user_email = None
                user_password = None

    ####
    #
    # Do your custom work here, or call custom functions.
    #
    ####

    output_filename = args['archive']
    input_filename = args['input']

    # open output to "fail fast" if file doesn't work.
    if output_filename is not None:
        with open(output_filename, "w") as new_config_json:
            pass

    # open input file.
    with open(input_filename, "r") as config_json:
        input_json = json.load(config_json)

    if not isinstance(input_json, list):
        if isinstance(input_json, dict):
            # check for optimized ACL
            optimized_ipv4_list = input_json.get("optimized_ipv4_list")
            if optimized_ipv4_list is None or not isinstance(optimized_ipv4_list, list):
                print("ERROR: ACL json is not in correct format (expected list, got '{0}'.)".format(type(input_json)))
                exit(1)
            else:
                # got optimized list, set.
                input_json = optimized_ipv4_list
        else:
            print("ERROR: ACL json is not in correct format (expected list, got '{0}'.)".format(type(input_json)))
            exit(1)

    sanitized_ipv4_list = []
    for entry in input_json:
        if isinstance(entry, dict):
            ipv4 = entry.get('ipv4')
            if ipv4 and isinstance(ipv4, text_type):
                # got ipv4 candidate. add
                sanitized_ipv4_list.append(ipv4)
            else:
                print("WARNING: read ipv4 invalid format: type: {0} value: '{1}'. Skipping.."
                      "".format(type(ipv4), ipv4))
        else:
            print("WARNING: read list entry invalid format: type: {0} value: '{1}'. Skipping.."
                  "".format(type(entry), entry))

    # do the ACL change.
    old_ipv4_list = do_acl(sdk, sanitized_ipv4_list)

    if output_filename is not None:
        with open(output_filename, "w") as old_config_json:
            json.dump(old_ipv4_list, old_config_json, indent=4)

    return

    ####
    #
    # End custom work.
    #
    ####


if __name__ == "__main__":
    go()
