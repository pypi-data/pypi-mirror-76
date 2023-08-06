from abc import ABC, abstractmethod
import requests
from tqdm import tqdm
from mod_updater.util.utils import TermColors
import os

class DownloadSource(ABC):

    def download_file(self, response, file_path):
        total_size_in_bytes= int(response.headers.get('content-length', 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print(f"{TermColors.FAIL}ERROR, something went wrong{TermColors.ENDC}")

    @abstractmethod
    def download(self):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def parse(cls, json):
        raise NotImplementedError()
