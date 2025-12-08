import os
import re
import subprocess
import sys
from pathlib import Path
import urllib.request
import urllib.error

# Where to save downloaded wheels
wheel_download_dir = Path("./wheels")
wheel_download_dir.mkdir(exist_ok=True)

def install_package_with_web_fallback(package_name: str):
    """
    Try to install a package using pip. If PyPI index access fails,
    extract wheel URLs from stderr and download them manually, then retry
    installing from the local wheels folder.
    """
    retries=0
    wheels_downloaded = 0

    while retries < 50:

        print(f"\n📦 Attempting to install {package_name}... (attempt {retries})")
        retries += 1
        
        # First attempt — normal pip install (uses local wheels if present)
        result = subprocess.run(
            [
                sys.executable, "-m", "pip", "install",
                "--no-cache-dir",
                f"--find-links={wheel_download_dir}",
                package_name
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        output = result.stdout + result.stderr
        if result.returncode != 0 or "error" in output.lower() or "failed" in output.lower():
            print("❌ Initial installation failed. Analyzing output...")
            print(".......................................................\n")
        else:
            print("✅ Package installed successfully.")
            return True

        # Extract wheel URLs
        wheel_urls = re.findall(r"https://files\.pythonhosted\.org/[^\s]+\.whl", output)
        if not wheel_urls:
            print("❌ No .whl URLs found in pip output. Cannot continue.\n")
            print(output)
            return False

        print(f"🔗 Found {len(wheel_urls)} wheel(s) to download...")
        # Download all found wheels
        for whl_url in wheel_urls:
            print(f"🌐 Processing URL: {whl_url}")
            filename = whl_url.split("/")[-1]
            local_path = wheel_download_dir / filename
            if local_path.exists():
                print(f"✅ Already downloaded: {filename}")
                continue
            try:
                print(f"⬇️  Downloading {filename} ...")
                with urllib.request.urlopen(whl_url) as response:
                    with open(local_path, "wb") as f:
                        f.write(response.read())
                print(f"💾 Saved: {local_path}")
                wheels_downloaded += 1
            except urllib.error.URLError as e:
                print(f"❌ Failed to download {filename}: {e}")
        print("wheels downloaded./n")
        

        # Retry once using only local wheels
        print("\n🔁 Retrying installation using downloaded wheels...")
        print("........................................................")
        retry_result = subprocess.run(
            [
                sys.executable, "-m", "pip", "install",
                "--no-index",  # use only local wheels
                f"--find-links={wheel_download_dir}",
                package_name
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if retry_result.returncode == 0:
            print("✅ Successfully installed from local wheels!")
            print(f"downloaded {wheels_downloaded} wheels in total.\n")
            break

        else:
            print("❌ Installation still failed. Looking for more wheels to download...\n")
            print(retry_result.stderr)
            continue


if __name__ == "__main__":
    print("Running install_package_with_web_fallback...\n")
    # if len(sys.argv) < 2:
    #     print("Usage: python install_from_web_wheels.py <package-name>")
    #     sys.exit(1)

    # pkg = sys.argv[1]
    pkg = "pip-audit"
    install_package_with_web_fallback(pkg)
        