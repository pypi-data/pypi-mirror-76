from __future__ import print_function

import os.path

from .display import translate_status_code

from .subcommand import Subcommand

class queue(Subcommand):
    '''
    Lists your currently queued simulations.
    '''

    def add_arguments(self, command_parser):
        command_parser.add_argument("-a", "--all", help = "fetch all simulations rather than just pending and running ones", dest = 'all', action = 'store_const', const = True, default = False)

    def run(self, server, auth_token, options):
        params = {}

        if options.all:
            params['all'] = True

        simulations = self.fetch_json(server, auth_token, params)['simulations']

        if len(simulations) == 0:
            self.print("No processes" if options.all else "No pending processes")
            return

        self.print("Processes:")

        for sim in simulations:
            is_error = sim.get("error", False)
            line_color = '\033[31m' if is_error else '\033[32m'

            if self.very_quiet and is_error:
                return 1

            self.quiet_print(
                quiet_message = "{} {}".format(sim["id"], sim["status"]),
                loud_message = "  {}: {}{}\033[0m".format(sim["id"], line_color, translate_status_code(sim["status"]))
            )
