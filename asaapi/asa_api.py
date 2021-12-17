import urllib
import urllib.parse
import requests
from requests.auth import HTTPBasicAuth
import logging

log = logging.getLogger(__name__)


class ASAAPI(object):
    def __init__(self, user: str = "", passwd: str = "", user_agent: str = "REST API Agent", verify: bool = True):
        """
        Create an ASA API object to interact with the ASA API.
        :param  user: username with which to authenticate against the ASA
        :param  passwd: password with which to authenticate against the ASA
        :param  user_agent: By default the ASA will accept "REST API Agent"
        :param  verify: Verify certificate validity. Should always be "True" in production; "False" allows self-signed
        """
        self.api_endpoint = None
        self.user_agent = user_agent
        self.response = None
        self.username = user
        self.passwd = passwd
        self.verify = verify
        return

    def set_api_endpoint(self, asa_ip: str, api_port: int = 443, context_name: str = "admin") -> None:
        """
        Given an ASA IP address, port, type of command and context name (if applicable) create the URL endpoint needed
        :param asa_ip: The IP address of the interface where the HTTP server has been enabled
        :param api_port: The port on which the HTTP server is listening (default = 443)
        :param context_name: In a ,ulti-context firewall, the context on which to execute this operation -
                             "admin" for single context by default

        """
        self.api_endpoint = "https://" + asa_ip + ":" + str(api_port) + f"/{context_name}/exec"
        log.debug(f"API Endpoint: {self.api_endpoint}")

    def sanitize_command(self, command: list) -> str:
        """
        When passing commands to the API, spaces need to be converted to '+' charactrers.
        Also, when nested configuration items like setting the nameif of an interface are required,
        concatonate the endpoint with the commands in the list
        Other sanitzation can happen here as well.
        :param command: list of the command(s) to be issued like "show version" or "write mem"
        """
        # TODO: more sanitization of input
        sanitized_cmd = ""
        for item in command:
            log.debug(f"Original Command: {item}")
            sanitized_cmd += "/" + urllib.parse.quote_plus(item)
        log.debug(f"Sanitized Command: {sanitized_cmd}")
        return sanitized_cmd

    def call_asa_api(self, command=None, operation="get", data=""):
        """
        Make the ASDM/API call to the ASA
        :param command: list that represents the command to be issued on the ASA
        :param data: for future use
        """
        sanitized_commands = ""
        sanitized_commands += self.sanitize_command(command)
        api_endpoint = self.api_endpoint + sanitized_commands if sanitized_commands else self.api_endpoint

        if operation == "get":
            r = requests.get(
                api_endpoint,
                auth=HTTPBasicAuth(self.username, self.passwd),
                headers={"Content-Type": "text/xml", "User-Agent": self.user_agent},
                verify=self.verify,
            )
        if r.status_code == 200:
            return r.text
        else:
            log.error(f"API call failed with status code:{r.status_code}")

    def get_curl_cmd(self, cmd):
        """
        Given a command, sanitize, format, and return the equivelant curl command
        :param cmd: command to execute on the ASA
        """
        curl = f"curl -u '{self.username}:{self.passwd}' -H 'User-Agent: {self.user_agent}' "
        if not self.verify:
            curl += "-k "
        return f"{curl}{self.api_endpoint}{self.sanitize_command(cmd)}"
