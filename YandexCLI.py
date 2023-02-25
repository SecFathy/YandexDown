import argparse
import requests
import urllib.parse
import os


class YandexDiskDownloader:
    def __init__(self, link, download_location):
        self.link = link
        self.download_location = download_location

    def download(self):
        url = f"https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={self.link}"
        response = requests.get(url)
        download_url = response.json()["href"]
        file_name = urllib.parse.unquote(download_url.split("filename=")[1].split("&")[0])
        save_path = os.path.join(self.download_location, file_name)

        with open(save_path, "wb") as file:
            download_response = requests.get(download_url, stream=True)
            for chunk in download_response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    file.flush()

        print("Download complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Yandex Disk Downloader')
    parser.add_argument('-l', '--link', type=str, help='Link for Yandex Disk URL', required=True)
    parser.add_argument('-d', '--download_location', type=str, help='Download location in PC', required=True)
    args = parser.parse_args()

    downloader = YandexDiskDownloader(args.link, args.download_location)
    downloader.download()
