#!/usr/bin/env python

# Importing modules
import copy
import argparse
from netaddr import IPNetwork, IPSet, AddrFormatError
import json
import sys

version = "1.0.0b1"
__version__ = version
GLOBAL_MY_SCRIPT_VERSION = version

# Handle differences between python 2 and 3. Code can use text_type and binary_type instead of str/bytes/unicode etc.
if sys.version_info < (3,):
    text_type = unicode
    binary_type = str
else:
    text_type = str
    binary_type = bytes


def lossy_supernet(ip_list, match_quality=30, ip_mismatch_limit=20):
    """
    Take a list of IP / subnets and return an optimized list.
    :param ip_list: list of IPv4 strings or IPv4/prefix strings
    :param match_quality: minimum % to be a good match
    :param ip_mismatch_limit: Do not match if IPs mismatched are > this amount (even if good match.)
    :return: dict with results.
    """

    # Default storage objects
    working_dict = {}
    output_list = []
    output_dict = {}

    input_ip_list_len = len(ip_list)

    # sanity data
    if not isinstance(ip_list, list):
        print("ERROR: ip_list is not a list (is '{0}').".format(type(ip_list)))
        return {
            'parsing_details': None,
            'output_list': [],
            'input_list': ip_list,
            'original_network_entries': input_ip_list_len,
            'final_network_entries': None,
            'total_mismatch_ip': None,
            'total_ip': None,
            'input_loss': ip_mismatch_limit,
            'input_quality': match_quality
        }
    if isinstance(match_quality, (float, int)):
        # match_quality is correct type. Is percent, convert int to float (%)
        if isinstance(match_quality, int):
            if match_quality >= 100:
                match_quality = 1.00
            elif match_quality <= 0:
                match_quality = 0.00
            else:
                # convert
                match_quality = float(match_quality * 0.01)
        else:
            # float
            if match_quality >= 1.00:
                match_quality = 1.00
            elif match_quality <= 0.00:
                match_quality = 0.00

    else:
        # invalid match quality, set to default
        match_quality = 0.50
    if not isinstance(ip_mismatch_limit, int):
        # invalid ip match limit, set to default.
        ip_mismatch_limit = 20

    # expanded_ip_list = []
    # for ip_entry in ip_list:
    #     # expand all /32s in IP ranges
    #     ip_net = IPNetwork(ip_entry)
    #     for ip_addr in ip_net:
    #         expanded_ip_list.append(text_type(ip_addr) + "/32")
    #         print(expanded_ip_list[-1])

    # Enumerate Expanded IP list
    for ip_addr in ip_list:
        original_ip_network = IPNetwork(ip_addr)
        # For every IP, determine supernet chain to root (0.0.0.0/0)
        try:
            ip_nets = original_ip_network.supernet()
        except AddrFormatError:
            # misformatted error. Continue.
            print("ERROR: '{0}' is not a correctly formatted ipv4 address or address/prefix. Skipping."
                  "".format(ip_addr))
            continue
        # /32 or last is important, add it to the list.
        ip_nets.append(original_ip_network)
        # Iterate through each supernet chain, building giant relational dictionary
        for ip_net in ip_nets:
            # Create a string for key value
            ip_net_key = text_type(ip_net.ip) + '/' + text_type(ip_net.prefixlen)
            # If key does not exist, add key and template values
            if not working_dict.get(ip_net_key):
                working_dict[ip_net_key] = {'matches': 0.00, 'iplist': [], 'dead': False}
            # Add IP to match list
            working_dict[ip_net_key]['iplist'].append(str(ip_addr))
            # Get matching addresses, update with new subnet.
            working_dict[ip_net_key]['matches'] = IPSet(working_dict[ip_net_key]['iplist']).size
            # Calculate match quality %
            working_dict[ip_net_key]['quality'] = float(working_dict[ip_net_key]['matches']) / float(ip_net.size)
            # Save size of supernet for later use.
            working_dict[ip_net_key]['size'] = ip_net.size

            # Add bitmask to value for parsing
            working_dict[ip_net_key]['bitmask'] = int(ip_net.prefixlen)

    # print json.dumps(working_dict, sort_keys=True,indent=4, separators=(',', ': '))
    parsing_dict = copy.deepcopy(working_dict)

    from cloudgenix import jd
    # jd(parsing_dict)
    # iterate supernets from largest (/0) to smallest (/32)
    for root_iter in range(0, 33):
        for key, value in parsing_dict.items():
            # If dict entry's bitmask is at the level we are parsing and not dead, act.
            if value['bitmask'] == root_iter and value['dead'] is not True:
                # Determine # of IPs that are not supposed to match
                mismatched_ips = value['size'] - value['matches']
                # If this supernet meets criteria, pop it to result and remove matching from parsing_dict
                if value['quality'] > match_quality and mismatched_ips <= ip_mismatch_limit:
                    # Add supernet to output
                    output_list.append(key)
                    output_dict[key] = {'quality': value['quality'], 'mismatch': mismatched_ips}
                    # put ip match list in remove queue
                    removal_queue_list = list(value['iplist'])
                    # delete (mark dead) this key
                    value['dead'] = True
                    # Reiterate parsing_dict, removing and recalculating IPs
                    for key2, value2 in parsing_dict.items():
                        # If an IP in removeList exists in supernet match list
                        for match in removal_queue_list:
                            if match in reversed(value2['iplist']):
                                # Remove the IP from the match list
                                value2['iplist'].remove(match)
                                # Decrement the match value
                                value2['matches'] = IPSet(value2['iplist']).size
                        # Recalculate quality after removing IPs
                        value2['quality'] = float(value2['matches']) / float(value2['size'])
                        # If all match IPs have been removed, mark key deleted (dead)
                        if value2['matches'] == 0 and working_dict[key2]['matches'] != 0:
                            # print '**'+key2+"** now has 0 IPs, originally "+str(working_dict[key2]['matches'])
                            value2['dead'] = True

    # print key + ' matches with a '+str(value['quality'] * 100) +
    #             '% match ('+str(value['matches'])+'/'+str(value['size'])+')'
    # print json.dumps(parsing_dict, sort_keys=True,indent=4, separators=(',', ': '))
    # print output_list
    mismatch_total = 0
    for key, value in output_dict.items():
        mismatch_total = mismatch_total + value['mismatch']

    return {
        'parsing_details': output_dict,
        'output_list': output_list,
        'input_list': ip_list,
        'original_network_entries': input_ip_list_len,
        'final_network_entries': len(output_dict.keys()),
        'total_mismatch_ip': mismatch_total,
        'total_ip': len(ip_list),
        'input_loss': ip_mismatch_limit,
        'input_quality': match_quality
    }


def optimize_acl():
    """
    optimize an acl list.
    :return:
    """
    script_name = "Optimize ACL"
    # Parse arguments
    parser = argparse.ArgumentParser(description="{0} ({1})".format(script_name, GLOBAL_MY_SCRIPT_VERSION))

    ####
    #
    # Add custom cmdline argparse arguments here
    #
    ####

    custom_group = parser.add_argument_group('custom_args', 'Optimize ACL arguments')
    custom_group.add_argument("--input", help="ACL file to optimize",
                              required=True)
    custom_group.add_argument("--output", help="File name to save output to",
                              required=True)
    custom_group.add_argument("--match-quality", help="Minimum match quality (percent.) Default: 30",
                              type=int, default=30)
    custom_group.add_argument("--ip-mismatch-limit", help="Maximum IPs that get mis-matched in an entry. Default: 60",
                              type=int, default=60)

    args = vars(parser.parse_args())

    input_filename = args['input']
    output_filename = args['output']
    match_quality = args['match_quality']
    ip_mismatch_limit = args['ip_mismatch_limit']

    with open(input_filename, "r") as old_config_json:
        input_json = json.load(old_config_json)

    if not isinstance(input_json, list):
        print("ERROR: ACL json is not in correct format (expected list, got '{0}'.)".format(type(input_json)))
        exit(1)

    ipv4_addr_list = []
    for entry in input_json:
        if isinstance(entry, dict):
            ipv4 = entry.get('ipv4')
            if ipv4 and isinstance(ipv4, text_type):
                # got ipv4 candidate. add
                ipv4_addr_list.append(ipv4)
            else:
                print("WARNING: read ipv4 invalid format: type: {0} value: '{1}'. Skipping.."
                      "".format(type(ipv4), ipv4))
        else:
            print("WARNING: read list entry invalid format: type: {0} value: '{1}'. Skipping.."
                  "".format(type(entry), entry))

    # optimize the addr list.
    optimized_output = lossy_supernet(ipv4_addr_list, match_quality, ip_mismatch_limit)

    optimized_ipv4_list = []
    for entry in optimized_output['output_list']:
        optimized_ipv4_list.append({
            "ipv4": entry
        })

    optimized_output['optimized_ipv4_list'] = optimized_ipv4_list

    with open(output_filename, "w") as new_config_json:
        json.dump(optimized_output, new_config_json, indent=4)

    return




