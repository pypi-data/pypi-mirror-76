import os.path
from configparser import ConfigParser
import argparse

import cflow

from .error import ConfigurationError

class Runner(object):
    '''
    The central object in the cflow client. The Runner is responsible for reading configuration files and the OS environment, parsing command line arguments, and outputting results. The public interface to Runner consists of a single (class) method: `cflow.Runner.invoke()`. See the documentation for `cflow.Runner.invoke()` for details on calling the method and using the results.

    Synopsis:
        `sys.exit(cflow.Runner.invoke(sys.argv) or 0)`
    '''

    config_file = "cflowrc"

    config_keys = [
        "allow_recursive_submit",
        "auth_token",
        "disable_https",
        "server",
    ]

    default_config_values = {
        "disable_https": False,
        "allow_recursive_submit": False,
    }

    environment_keys = {
        "CFLOW_SERVER": "server",
        "CFLOW_AUTH_TOKEN": "auth_token",
    }

#region Public interface

    @classmethod
    def invoke(Self, argv):
        '''
        Invokes the cflow client, parsing out the configuration, evaluating the environment and command line arguments, and runs the selected subcommand (or, if not possible, prints an error).

        Usage:
            `sys.exit(cflow.Runner.invoke(sys.argv) or 0)`

        Args:
            argv (list): sys.argv or equivalent.

        Raises:
            cflow.CommunicationError: On problems communicating with the remote server.
            cflow.ConfigurationError: On failure to configure the runner from the environment.

        Returns:
            invoke (int?): An integral status code to be returned to the OS (0 on success), or None.
        '''
        return Self(argv[1:])._run()

#endregion

    def __init__(self, argv):
        '''
        Initialises the runner, parsing arguments and preparing it for running the subcommand. Do not invoke directly, call `cflow.Runner.invoke()` instead.

        Args:
            argv (list): A list of arguments as returned by sys.argv or equivalent, with the program name removed (_i.e._ _e.g._ `sys.argv[1:]`).
        '''
        self._config_section = "server"

        self._allow_recursive_submit = None
        self._auth_token = None
        self._server = None
        self._disable_https = None

        self._subcommand = None

        self._init_argparse(argv)
        self._init_env()
        self._init_config_file()

        self._validate_config()

    def _run(self):
        '''
        Runs the selected subcommand. Do not invoke directly, call `cflow.runner.invoke()` instead.

        Returns:
            _run (int?): An integral status code to be returned to the OS (0 on success) or None.
        '''
        return self._subcommand(self._server_uri, self._auth_token, self._opts)

#region Environment initialisers

    def _init_argparse(self, argv):
        '''
        Initialises values in self from the argument parser, in particular which subcommand to use.
        '''
        opts = self._argparser.parse_args(argv)

        if opts.cflow_server:
            if opts.cflow_server.startswith("http://"):
                self._server = opts.cflow_server[7:]
                self._disable_https = True
            elif opts.cflow_server.startswith("https://"):
                self._server = opts.cflow_server[8:]
            else:
                self._server = opts.cflow_server

        if opts.auth_token:
            self._auth_token = opts.auth_token

        self._config_section = opts.config_section
        self._subcommand = opts.subcommand

        self._opts = opts

    def _init_env(self):
        '''
        Initialises values in self from the OS environment where missing.
        '''
        for envkey, config_key in self.environment_keys.items():
            attr_key = "_{}".format(config_key)
            if not getattr(self, attr_key):
                setattr(self, attr_key, os.environ.get(envkey, None))

    def _init_config_file(self):
        '''
        Initialises values in self from config files where mising.
        '''
        config_parser = ConfigParser()
        config_parser.read([
            "/etc/cflow/{}".format(self.config_file),
            os.path.expanduser("~/.{}".format(self.config_file)),
        ])

        if self._config_section in config_parser:
            config_section = config_parser[self._config_section]

            for config_key in self.config_keys:
                attr_key = "_{}".format(config_key)
                if not getattr(self, attr_key):
                    setattr(self, attr_key, config_section.get(config_key, None) or self.default_config_values.get(config_key, None))

        try:
            self._allow_rescursive_submit = self._opts.allow_recursive_submit = self._opts.allow_recursive_submit or self._allow_recursive_submit
        except:
            pass

#endregion

    def _validate_config(self):
        '''
        Validates the execution environment to ensure the cflow client has the configuration data it needs to communicate with the cflow server.

        Raises:
            cflow.ConfigurationError: On missing configuration values.
        '''
        missing_keys = list()
        for config_key in self.config_keys:
            attr_key = "_{}".format(config_key)
            if getattr(self, attr_key) == None:
                missing_keys.append(config_key)

        if len(missing_keys):
            raise ConfigurationError(missing_keys)

    @property
    def _server_uri(self):
        '''
        Returns:
            server (str): The base URI for the remote server, with method and name (_e.g._ `http://example.info`).
        '''
        method = "http" if self._disable_https else "https"

        return "{}://{}".format(method, self._server)

    @property
    def _argparser(self):
        '''
        Returns:
            _argparser (argparse.ArgumentParser): An initialised argument parser that can process arguments to cflow and its subcommands.
        '''
        parser = argparse.ArgumentParser(prog = "cflow")

        parser.add_argument("--debug", help = "run cflow in debug mode", dest = 'config_section', action = 'store_const', const = 'test_server', default = 'server')

        parser.add_argument("--cflow-server", help = "the server to connect to")
        parser.add_argument("--auth-token", help = "the authorisation token to use against the server")

        parser.add_argument("-q", "--quiet", help = "reduce the ouput printed on success", dest = 'quiet', action = 'store_const', const = True, default = False)
        parser.add_argument("-Q", "--very-quiet", help = "further reduce the ouput printed on success, implies -q", dest = 'very_quiet', action = 'store_const', const = True, default = False)

        subparsers = parser.add_subparsers()

        for command in cflow.commands():
            command_runner = command()

            subparser = subparsers.add_parser(command_runner.name, help = command_runner.__doc__)
            subparser.set_defaults(subcommand = command_runner)

            command_runner.add_arguments(subparser)

        return parser
