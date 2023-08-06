from __future__ import print_function

from abc import ABCMeta, abstractmethod

from .error import CommunicationError

import requests

class Subcommand():
    '''
    The Subcommand class represents a subcommand in the `cflow` application, containing a single, self-contained piece of functionality, such as uploading something to the executing server, downloading finished files, interrogating the status of a process, _&c._.

    Subclassing:
        A new piece of functionality needs to implement the method run(server, auth_token, options), and will likely also need to implement add_arguments(command_parser) in order to support passing in things like process identifiers. Additionally, for automatic discovery, new subclasses need to be added to __init__.py.
    '''

    __metaclass__ = ABCMeta

    def __init__(self):
        self._quiet = None
        self._very_quiet = None

#region Required for subclasses

    def add_arguments(self, command_parser):
        '''
        Adds the arguments the subcommand recognises to the passed command_parser.

        Args:
            command_parser (argparse.ArgumentParser): The argument parser to add the known arguments to.
        '''
        pass

    @abstractmethod
    def run(self, server, auth_token, options):
        '''
        This method houses the core of the implementation of a Subcommand, and must be overridden in subclasses. This method should not be called directly, but only through Subcommand.__call__(). Arguments and return values are discussed in the documentation of __call__().
        '''
        pass

#endregion

    @property
    def name(self):
        '''
        Returns:
            name (str): A human-readable name for the subcommand.
        '''
        return type(self).__name__

    @property
    def endpoint(self):
        '''
        Returns:
            endpoint (str): A string suitable for use as the endpoint identifier for the functionality.
        '''
        return self.name

    @property
    def quiet(self):
        '''
        Returns:
            quiet (bool): True if `cflow` was invoked in quiet mode or very quiet mode, otherwise False.
        '''
        return self._quiet

    @property
    def very_quiet(self):
        '''
        Returns:
            very_quiet (bool): True if `cflow` was invoked in very quiet mode, otherwise False.
        '''
        return self._very_quiet

    def url(self, server):
        '''
        Args:
            server(str): The address (including method) of the server to execute the subcommand against.

        Returns:
            url (str): An URL suitable for use as a web service endpoint for executing the subcommand.
        '''
        return "{}/simulation/{}/".format(server, self.endpoint)

    def print(self, *args, **kwargs):
        '''
        Invokes print(*args, **kwargs) for messages that should be printed when `cflow` was not invoked in quiet mode.

        Args:
            As print().

        Returns:
            As print().
        '''
        if not self._quiet:
            print(*args, **kwargs)

    def quiet_print(self, quiet_message = None, loud_message = None):
        '''
        Selects and prints a message depending on whether `cflow` was invoked in normal (loud) mode, quiet mode, or very quiet mode. If `cflow` was invoked in very quiet mode, nothing is printed.

        Args:
            quiet_message (str?): A message to print when `cflow` is running in quiet mode.
            loud_message (str?): A message to print when `cflow` is running in loud mode.
        '''
        if self._very_quiet:
            return

        if self._quiet:
            if quiet_message != None:
                print(quiet_message)
            return

        if loud_message != None:
            print(loud_message)

#region Do not override

    def __call__(self, server, auth_token, options):
        '''
        Invokes the subcommand. This method should not be overriden by subclasses, override run() instead.

        Args:
            server (str): A string containing the address to the server to perform the command against.
            auth_token (UUID): An UUID representing a secret token to pass to the server in order to authorise the requested operation.
            options (namespace): A context object, as produced by argparse's parse_args or equivalent.

        Returns:
            status (int?): An integral status code that can be returned to the OS, or None.
        '''
        self._very_quiet = options.very_quiet
        self._quiet = self._very_quiet or options.quiet

        return self.run(server, auth_token, options)

    def fetch_json(self, server, auth_token, params):
        '''
        Fetches a json object from the endpoint using a standard methodology.

        Args:
            server (str): A string containing the address of the server to perform the command against.
            auth_token (UUID): The authentication token to use for authenticating the request.
            params ({str: str}): A dictionary containing additional, subcommand-specific parameters.

        Raises:
            cflow.CommunicationError: If the response is not HTTP 200 with a valid JSON object.

        Returns:
            fetch_json (dict): A dictionary extracted from the JSON response to the request.
        '''
        params["auth_token"] = auth_token
        response = requests.get(self.url(server), params = params)
        if response.status_code != 200:
            raise CommunicationError(response.status_code, response.text)

        try:
            return response.json()
        except:
            raise CommunicationError(200, "Malformed response body: {}".format(response.text))

#endregion

def commands():
    '''
    Returns:
        commands: An array of all available subcommand classes.
    '''
    return Subcommand.__subclasses__()
