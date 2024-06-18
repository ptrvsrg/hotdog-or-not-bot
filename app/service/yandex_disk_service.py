import hashlib
import logging
from io import BytesIO

import yadisk


class YandexDiskService:

    def __init__(self, token, base_dir):
        self.logger = logging.getLogger("yandex_disk_service")

        # Client creation
        self.logger.info(f"Creating Yandex Disk client")
        self.client = yadisk.AsyncClient(token=token)
        self.base_dir = base_dir

    async def upload_file(self, file_bytes, folder_name):
        """
        Asynchronously uploads a file to Yandex Disk.
        Parameters:
            file_bytes (bytes): The content of the file in bytes.
            folder_name (str): The name of the folder where the file will be uploaded.
        Returns:
            None
        """
        # Create a hash for the filename
        file_hash = hashlib.md5(file_bytes).hexdigest()
        file_path = f"{self.base_dir}/{folder_name}/{file_hash}.jpg"

        # Create folder
        await self._make_dir(f"{self.base_dir}/{folder_name}")

        # Upload file
        io = BytesIO(file_bytes)
        await self.client.upload(io, file_path, overwrite=True)
        self.logger.info(f"File uploaded: {file_path}")

    async def _make_dir(self, folder):
        """
        Asynchronously creates a folder in Yandex Disk.
        Parameters:
            folder (str): The name of the folder to be created.
        Returns:
            None
        """
        path = ""
        for folder_name in folder.split("/"):
            path = f"{path}/{folder_name}"
            try:
                await self.client.mkdir(path)
            except yadisk.exceptions.PathExistsError:
                self.logger.debug(f"Directory already exists: {path}")

        self.logger.info(f"Created directory: {folder}")
