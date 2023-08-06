import os.path
from unittest import TestCase

from cflow import Config

class ClientTest(TestCase):

    def setUp(self):
        pass


    def test_config(self):
        Config.config_file = None
        conf = Config([Config.subcommand_download])
        with self.assertRaises(ValueError):
            token = conf.auth_token


        with open("config_file", "w") as fp:
            fp.write("""[server]
auth_token = xyz
server = www.xyz.com
            """)


        Config.config_file = os.path.abspath("config_file")
        conf = Config([Config.subcommand_download])
        self.assertEqual(conf.auth_token, "xyz")
        self.assertEqual(conf.server, "www.xyz.com")


        os.environ[Config.server_envkey] = "cflow.server"
        conf = Config([Config.subcommand_download])
        self.assertEqual(conf.auth_token, "xyz")
        self.assertEqual(conf.server, "cflow.server")

        conf = Config([Config.subcommand_download, "--{}=cflow.arg.server".format(Config.server_optkey)])
        self.assertEqual(conf.auth_token, "xyz")
        self.assertEqual(conf.server, "cflow.arg.server")

        conf = Config([Config.subcommand_download, "--{}=cflow.arg.server".format(Config.server_optkey), "arg1", "arg2"])
        self.assertEqual(conf.auth_token, "xyz")
        self.assertEqual(conf.server, "cflow.arg.server")
        self.assertEqual(conf.argv, ["arg1", "arg2"])

        with self.assertRaises(ValueError):
            conf = Config(["invalid_subcomman"])


