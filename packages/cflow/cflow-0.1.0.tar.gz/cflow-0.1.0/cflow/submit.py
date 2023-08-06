import io
import os.path
import requests

from .error import CommunicationError

from .subcommand import Subcommand

class submit(Subcommand):
    '''
    Submits a .DATA file to a flow cloud server for processing.
    '''

    def add_arguments(self, command_parser):
        command_parser.add_argument("-r", "--recursive", help = "allow recursive uploads", dest = 'allow_recursive_submit', action = 'store_const', const = True, default = False)
        command_parser.add_argument("filename", help="the path to the file or directory to upload")

    def take_single_file(self, filename):
        '''
        Processes a single file for upload to the server, choosing a name to use and opening a file handle for reading.

        Args:
            filename (str): The path to the file to upload.

        Returns:
            filename (str): The filename to upload the file by.
            to_upload (file): A file handle (or file-like object) suitable for reading the contents of the file from.
        '''
        _, upload_fname = os.path.split(filename)

        return upload_fname, open(filename, "rb")

    def take_directory(self, filename):
        '''
        Processes a directory for upload to the server, choosing a name to use and producing an archive that can be uploaded as a single file.

        Args:
            filename (str): The path to the directory to upload.

        Returns:
            filename (str): The filename to upload the file by.
            to_upload (file): A file handle (or file-like object) suitable for reading the archive produced from the directory from.
        '''
        _, upload_fname = os.path.split(filename)

        archive = _zipdir(filename)

        return "{}.zip".format(upload_fname), archive.getvalue()

    def assess_file(self, filename, allow_recursive_submit):
        '''
        Assesses a path for suitability for upload, and opens a file for reading from the path.

        Args:
            filename (str): The path to the file to assess.
            allow_recursive_submit (bool): Whether a recursive, archiving submit should be allowed.

        Raises:
            RuntimeError: If the supplied path is not that of a file or directory.

        Returns:
            filename (str): The name of the file that has been assessed.
            handle (file): A file handle (or file-like object) representing the assessed file.
        '''
        if os.path.isdir(filename):
            if allow_recursive_submit:
                return self.take_directory(filename)
            else:
                raise RuntimeError("Submitted object at {} is a directory, and cflow is not in recursive mode. Invoke with --recursive to upload this directory.".format(filename))
        elif os.path.isfile(filename):
            return self.take_single_file(filename)
        else:
            raise RuntimeError("Submitted object at {} is neither a file nor a directory.".format(filename))

    def upload_file(self, server, auth_token, filename, to_upload):
        '''
        Uploads the file found at a given path to the remote server.

        Args:
            server (str): A string containing the address of the server to perform the command against.
            auth_token (UUID): The authentication token to use for authenticating the request.
            filename (str): The name to give for the upload.
            to_upload (file): A file handle (or file-like object) containing the data to upload.

        Raises:
            RuntimeError: If the supplied pail is not that of a suitable file or directory to upload.
            cflow.CommunicationError: If the response is not a valid HTTP 201 with a process identifier attached.

        Returns:
            upload_file (UUID): A process identifier for the uploaded data.
        '''
        response = requests.post(self.url(server), data = {
            "auth_token": auth_token
        }, files = {
            filename: to_upload
        })

        if response.status_code != 201:
            raise CommunicationError(response.status_code, response.text)

        return response.text

    def run(self, server, auth_token, options):
        filename, to_upload = self.assess_file(options.filename, options.allow_recursive_submit)

        process_id = self.upload_file(server, auth_token, filename, to_upload)

        self.quiet_print(
            quiet_message = process_id,
            loud_message = "Process initiated with id {}.\nUse `cflow status {}' to follow up on this process.".format(process_id, process_id)
        )

from zipfile import ZipFile, ZIP_DEFLATED

def _zipdir(path, destination_file = io.BytesIO()):
    '''
    Uses zipfile to recursively archive the contents of a directory to an archive file.

    Args:
        path (str): The path of the directory to archive.
        destination_file (file): A file handle (or file-like object) to write the contents to.

    Returns:
        destination_file (file): The supplied file handle (or file-like object).
    '''
    with ZipFile(destination_file, "a", compression = ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(path):
            for file in files:
                zip_file.write(os.path.join(root, file), compress_type = ZIP_DEFLATED)

    return destination_file
