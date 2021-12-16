from asaapi import ASAAPI
from os import environ


def main():
    # instantiate the interface
    asa_api = ASAAPI(user=user, passwd=passwd, verify=False)

    # Execute "show version"
    asa_api.set_api_endpoint(ip, api_port=port)
    print(asa_api.asa_api_get(command=["show version"]))

    # Configure the outside interface name-if as "outside-test"
    asa_api.asa_api_get(command=["interface gigabitEthernet0/0", "nameif outside-test"])
    print(asa_api.asa_api_get(command=["show running-config interface gigabitEthernet 0/0"]))

    # Execute a packet-tracer and print the results
    ptrace = "packet-tracer input outside tcp 8.8.8.8 1099 192.168.12.12 80"
    print(asa_api.asa_api_get(command=[ptrace]))


if __name__ == "__main__":
    ip = environ.get("ASAIP")
    user = environ.get("ASAUSER")
    passwd = environ.get("ASAPASS")
    port = int(environ.get("ASAPORT"))
    main()
