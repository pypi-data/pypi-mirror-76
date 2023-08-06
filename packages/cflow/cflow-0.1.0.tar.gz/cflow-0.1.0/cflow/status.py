import os.path
import requests

from .display import translate_status_code
from .error import CommunicationError

from .subcommand import Subcommand

class status(Subcommand):
    '''
    Fetches the current status of a flow cloud process from the flow cloud server.
    '''

    def add_arguments(self, command_parser):
        command_parser.add_argument("token", help = "the process ID for the task to get the status of")

    def run(self, server, auth_token, options):
        sim_id = options.token

        status_code = self.fetch_json(server, auth_token, {
            'simulation': sim_id,
        })["status"]

        self.quiet_print(
            loud_message = "The process {} is {}.".format(sim_id, translate_status_code(status_code)),
            quiet_message = status_code
        )

        if self.very_quiet and response_object.get("error", False):
            return 1
