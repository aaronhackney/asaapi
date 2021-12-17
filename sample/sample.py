import warnings
from asaapi import ASAAPI
from os import environ


import asaapi

cmds_to_execute = [
    ["show version"],
    ["interface gigabitEthernet0/0", "nameif outside-test"],
    ["show running-config interface gigabitEthernet 0/0"],
    ["packet-tracer input outside tcp 8.8.8.8 1099 192.168.12.12 80"],
]


def main():

    # Only print the first TLS InsecureRequestWarning (Self signed certificates) or other warning instances
    if not verify:
        warnings.simplefilter("once")

    # instantiate the interface an define the endpoint (ASA) IP and Port
    asa_api = ASAAPI(user=user, passwd=passwd, verify=verify)
    asa_api.set_api_endpoint(ip, api_port=port)

    # loop through the list of commands to execute
    for cmd in cmds_to_execute:
        print(asa_api.get_curl_cmd(cmd))
        print("-------------------------------------------------------------------")
        print(asa_api.call_asa_api(command=cmd))


if __name__ == "__main__":
    ip = environ.get("ASAIP")
    user = environ.get("ASAUSER")
    passwd = environ.get("ASAPASS")
    port = int(environ.get("ASAPORT"))
    verify = True if environ.get("VERIFY") else False
    main()
