from __future__ import print_function

import os.path
import requests

from .error import CommunicationError

from .subcommand import Subcommand

class cancel(Subcommand):
    '''
    Cancels an ongoing simuation, denoted by the process ID.
    '''

    def add_arguments(self, command_parser):
        command_parser.add_argument("token", help = "the process ID for the task to cancel")

    def run(self, server, auth_token, options):
        sim_id = options.token

        params = {"auth_token" : auth_token, "simulation" : sim_id}
        response = requests.post(self.url(server), data=params)
        if response.status_code == 204:
            self.print("Process {} cancelled.".format(sim_id))
        elif response.status_code == 404:
            self.print("No such simulation: {}".format(sim_id))
        else:
            raise CommunicationError(response.status_code, response.text)

