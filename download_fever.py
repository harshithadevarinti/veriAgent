import urllib.request
import os

os.makedirs("data", exist_ok=True)

def show_progress(block_num, block_size, total_size):
    downloaded = block_num * block_size
    percent = min(downloaded / total_size * 100, 100) if total_size > 0 else 0
    mb_downloaded = downloaded / (1024 * 1024)
    mb_total = total_size / (1024 * 1024)
    print(f"\r{percent:.1f}% ({mb_downloaded:.1f} MB / {mb_total:.1f} MB)", end="")

url = "https://fever.ai/download/fever/wiki-pages.zip"
path = os.path.join("data", "wiki-pages.zip")

print("Downloading wiki-pages.zip...")
urllib.request.urlretrieve(url, path, reporthook=show_progress)
print("\nDone!")