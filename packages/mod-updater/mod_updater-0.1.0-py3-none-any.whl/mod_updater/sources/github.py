from .base import DownloadSource
import requests

class GithubSource(DownloadSource):
    REQUIRED_ARGS = ["owner", "repo"]
    
    def __init__(self, owner, repo, path):
        self._releases_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
        self._path = path

    def download(self):
        r = requests.get(self._releases_url)
        download_url = r.json()["assets"][0]["browser_download_url"]
        name = r.json()["assets"][0]["name"]
        download_response = requests.get(download_url, stream=True)
        self.download_file(download_response, f"{self._path}/{name}")

    @classmethod
    def parse(cls, json, path):
        for arg in cls.REQUIRED_ARGS:
            if arg not in json:
                raise Exception("Missing required arg ", arg, "in ", json)
        owner = json["owner"]
        repo = json["repo"]
        return cls(owner, repo, path)
