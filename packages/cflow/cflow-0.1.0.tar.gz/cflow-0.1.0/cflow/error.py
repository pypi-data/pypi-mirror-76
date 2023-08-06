class CommunicationError(RuntimeError):
    '''
    A specialized Exception for errors encountered in communication with the cflow server.
    '''

    format_string = "Received reply: {}: {} from server"

    def __init__(self, status_code, text):
        '''
        Args:
            status_code (int): An HTTP status code.
            text (str): A human-readable error message.
        '''
        self.status_code = status_code
        self.text = text

        super(CommunicationError, self).__init__(self.text)

    @property
    def error_text(self):
        '''
        Returns:
            error_text (str): An error message containing an HTTP status and its associated error message.
        '''
        return self.format_string.format(self.status_code, self.text)

class ConfigurationError(RuntimeError):
    '''
    A specialized Exception for errors encountered when trying to configure the cflow client from the environment.
    '''

    format_string = "Could not determine a value for configuration key(s) {}."

    def __init__(self, config_keys):
        '''
        Args:
            config_key ([str]): A list of configuration keys that could not be determined.
        '''
        self._config_keys = config_keys

        super(ConfigurationError, self).__init__(self.error_text)

    @property
    def config_keys(self):
        '''
        Returns:
            config_keys (str): A human-readable list of configuration key names.
        '''
        return ", ".join(map(lambda x: "`{}'".format(x), self._config_keys))

    @property
    def error_text(self):
        '''
        Returns:
            error_text (str): An error message incorporation the missing keys.
        '''
        return self.format_string.format(self.config_keys)
