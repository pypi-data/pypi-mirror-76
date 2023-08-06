from __future__ import print_function

from .display import translate_status_code

from .subcommand import Subcommand

class metadata(Subcommand):
    '''
    Fetches metadata for a simulation from the cflow cloud server, by process ID. The metadata class also contains class methods for use by other subcommands where necessary.
    '''

    def add_arguments(self, command_parser):
        command_parser.add_argument("token", help = "the process ID for the task to download results from")

    def run(self, server, auth_token, options):
        sim_id = options.token

        data = self.fetch_json(server, auth_token, {
            "simulation": sim_id,
        })

        self.print("Simulation ID: {}".format(sim_id))
        self.print("Base name: {}".format(data["base"]))
        self.print("Status: {}".format(translate_status_code(data["state"])))

        self.quiet_print(quiet_message = "{} {} {}".format(sim_id, data["base"], data["state"]))

        files = data["files"]
        self.print("{} files:".format(len(files)))
        for file in files:
            self.quiet_print(quiet_message = file, loud_message = "  {}".format(file))

#region Class methods

    @classmethod
    def fetch(Self, server, auth_token, sim_id):
        '''
        Fetches a JSON object.

        Args:
            server (str): The remote cflow server.
            auth_token (UUID): The token used to authorise the connection.
            sim_id (UUID): The ID of the simulation to fetch.

        Returns:
            fetch (dict): A dictionary containing the metadata for the simulation.
        '''
        return Self().fetch_json(server, auth_token, {
            "simulation": sim_id,
        })

    @classmethod
    def file_names(Self, server, auth_token, sim_id):
        '''
        Fetches the file names associated with the results of a simulation.

        Args:
            as cflow.metadata.fetch

        Returns:
            file_names (list(str)): A list of file names associated with the simulation.
        '''
        return Self.fetch(server, auth_token, sim_id)["files"]

#endregion
