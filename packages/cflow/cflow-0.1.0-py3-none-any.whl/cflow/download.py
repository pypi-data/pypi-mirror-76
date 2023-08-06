from __future__ import print_function

import os.path
import requests
import re
import tempfile
import random
import shutil

from .error import CommunicationError

from .metadata import metadata

def _fname(response):
    '''
    Gets the file name from an HTTP response.

    Args:
        response (requests.Response): The response object to extract a filename from.

    Returns:
        _fname (str): The filename.
    '''
    cd = response.headers.get("content-disposition")
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]

def _get_ext_list(server, auth_token, sim_id):
    '''
    Retrieves a list of the extensions of all the generated files from a simulation.

    Args:
        server (str): The URI of the server to connect to.
        auth_token (UUID): An auth token to authorise the connection.
        sim_id (UUID): The ID of the simulation to get file extensions for files for.

    Returns:
        _get_ext_list ([str]): A list of file extensions.
    '''
    ext_list = []
    for file in metadata.file_names(server, auth_token, sim_id):
        _, ext = os.path.splitext(file)
        ext_list.append(ext[1:])
    return ext_list

from .subcommand import Subcommand

class download(Subcommand):
    '''
    Downloads artefacts produced by the flow cloud server, by the process ID and (optionally) the desired file extensions. If no file extensions are provided, every file is downloaded.
    '''

    def add_arguments(self, command_parser):
        command_parser.add_argument("token", help = "the process ID for the task to download results from")
        command_parser.add_argument("extension", nargs = "*", help = "the extensions for the files to download")

    def run(self, server, auth_token, options):
        sim_id = options.token
        ext_list = options.extension
        if len(ext_list) == 0:
            ext_list = _get_ext_list(server, auth_token, sim_id)

        self.print("Downloading {} files:".format(len(ext_list)))
        for ext in ext_list:
            params = {"auth_token" : auth_token, "simulation" : sim_id, "file" : ext}
            response = requests.get(self.url(server), params=params)
            if response.status_code != 200:
                raise CommunicationError(response.status_code, response.text)

            target_file = _fname(response)
            self.quiet_print(quiet_message = target_file, loud_message = "  {}...".format(target_file))

            download_fname = os.path.join(tempfile.gettempdir(), "{}-{}".format(random.randint(0,100000), target_file))
            with open(download_fname, "wb") as fh:
                fh.write(response.content)

            shutil.move(download_fname, target_file)

        self.print("Download complete")
