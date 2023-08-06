"""
    CUSTOM WRITER CLASSES
        - Class which manages writer tasks like
        auth, write metadata, write file, create dir structure
"""
import json
import os
from datetime import timezone, datetime
from pathlib import Path

import boto3


# pylint: disable=no-init
class CustomLocalJsonWriter:
    """
        Custom JSON Writer class which writes data to local filesystem.

        Writes data into a file.json per query. The files are written to a directory tree
        set out as .
    """

    def __init__(
            self,
            file_name: str,
            folder_path: str,
            **kwargs
    ):
        # creates full path
        self.folder_path = folder_path
        # create file paths
        self.file_name = file_name
        # currently overwrites metadata.json each time
        self.metadata_file = kwargs.get("metadata_file", "metadata.json")
        # init data
        self.data = []
        # init path
        self.full_path = 'test'

    @staticmethod
    def mkdir_if_not_exists(full_path: str):
        """
            Make a new directory if one doesn't exist
        """
        Path(full_path).mkdir(parents=True, exist_ok=True)

    def check_files_in_dir(self):
        """
            Return the length of files in a directory
        """
        return len(os.listdir(self.full_path))

    @staticmethod
    def timestamp_suffix():
        """builds a filename suffix from the current timestamp"""
        curr_time = datetime.now().replace(tzinfo=timezone.utc).timestamp()
        suff = str(round(curr_time, 2)).replace(".", "_")
        return suff


class CustomS3JsonWriter(CustomLocalJsonWriter):
    """Class Extends Basic LocalGAJsonWriter"""

    def __init__(
            self,
            file_name: str,
            folder_path: str,
            bucket: str,
            profile_name: str = None,
            **kwargs
    ):
        self.os_path_sep = "/"

        if profile_name is None:
            self.boto3_session = boto3.Session()
        else:
            self.boto3_session = boto3.Session(profile_name=profile_name)

        self.bucket = bucket
        """Writes a general object to s3"""
        self.s3_resource = self.boto3_session.resource('s3')
        super().__init__(file_name=file_name, folder_path=folder_path, **kwargs)
        self.metadata_file = kwargs.get("metadata_file", "metadata.json.gz")

    def set_full_path(self):
        """Set full path to write to"""
        # creates full path
        today_date = datetime.today()
        date_prefix = today_date.strftime('%Y/%m/%d')

        full_path = [date_prefix, self.folder_path]

        return os.path.join(*full_path).replace('\\', '/')

    # pylint: disable=no-member,too-many-arguments
    def write_to_s3(
            self,
            json_data,
            data_path
    ):
        """
            Write report to s3 bucket
        """
        json_data = json.dumps(json_data)
        self.s3_resource.Bucket(self.bucket).put_object(
            Key=os.path.join(self.full_path, data_path).replace('\\', '/'),
            Body=json_data)

    def write_file(self, data: dict):
        """
            upload python dict into s3 bucket with gzip archive
        """
        # create directory structure if not exists
        self.full_path = self.set_full_path()

        # generate a unix timestamp suffix for file
        self.data = data
        suff = self.timestamp_suffix()
        data_path = "{}_{}.json".format(self.file_name, suff)
        self.write_to_s3(self.data, data_path)
        self.data = []
