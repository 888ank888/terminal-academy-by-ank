import os
import sys
import json
import urllib.request
import urllib.error
import ssl

def get_token():
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        return token
    for path in [".env", "../.env", "../../.env"]:
        if os.path.exists(path):
            with open(path, "r") as f:
                for line in f:
                    if line.strip().startswith("GITHUB_TOKEN="):
                        return line.strip().split("=")[1]
    return ""

TOKEN = get_token()
OWNER = "888ank888"
REPO = "terminal-academy-by-ank"

tags_to_delete = [
    "v0.1.0",
    "v0.2.0",
    "v0.2.1",
    "v0.3.0",
    "v1.0.0-beta",
    "v1.0.1",
    "v1.1.0",
    "v2.2.0",
    "v2.2.1"
]

releases_to_keep = {
    "v1.0.0": {
        "title": "v1.0.0 - Python Client Beta",
        "body": "First beta release of the Python-based Terminal Academy client."
    },
    "v2.0.0": {
        "title": "v2.0.0 - Application",
        "body": "Official launch of the Terminal Academy desktop application container environment."
    }
}

def request(url, method="GET", headers=None, data=None):
    if headers is None:
        headers = {}
    headers["Authorization"] = f"token {TOKEN}"
    headers["Accept"] = "application/vnd.github+json"
    
    req = urllib.request.Request(url, method=method, headers=headers, data=data)
    try:
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(req, context=context) as res:
            return res.status, json.loads(res.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        print(f"HTTP Error {e.code} for {url}: {body}", file=sys.stderr)
        try:
            return e.code, json.loads(body)
        except:
            return e.code, body
    except Exception as e:
        print(f"Connection error for {url}: {str(e)}", file=sys.stderr)
        return 500, str(e)

# Get all releases
status, releases = request(f"https://api.github.com/repos/{OWNER}/{REPO}/releases")
if status != 200:
    print(f"Failed to fetch releases: {releases}")
    sys.exit(1)

# Delete extra releases
for r in releases:
    tag = r["tag_name"]
    release_id = r["id"]
    if tag in tags_to_delete:
        print(f"Deleting release {tag} (ID: {release_id})...")
        del_status, del_res = request(f"https://api.github.com/repos/{OWNER}/{REPO}/releases/{release_id}", method="DELETE")
        print(f"Delete status: {del_status}")

# Update/Create keep releases
existing_releases = {r["tag_name"]: r["id"] for r in releases if r["tag_name"] not in tags_to_delete}

local_dmg = "/Users/ank/Documents/CODENAME_TERMINAL_ACADEMY/terminal-academy-desktop/src-tauri/target/release/bundle/dmg/terminal-academy_2.0.0_x64.dmg"

for tag, meta in releases_to_keep.items():
    ver = tag.replace("v", "")
    print(f"\n--- Processing Release {tag} ---")
    
    if tag in existing_releases:
        release_id = existing_releases[tag]
        print(f"Release for {tag} already exists (ID: {release_id}). Updating to English description...")
        
        payload = json.dumps({
            "name": meta["title"],
            "body": meta["body"]
        }).encode('utf-8')
        
        status, rel_data = request(
            f"https://api.github.com/repos/{OWNER}/{REPO}/releases/{release_id}",
            method="PATCH",
            headers={"Content-Type": "application/json"},
            data=payload
        )
        print(f"Updated release: status {status}")
    else:
        # Create release
        payload = json.dumps({
            "tag_name": tag,
            "name": meta["title"],
            "body": meta["body"],
            "draft": False,
            "prerelease": True if "-beta" in tag else False
        }).encode('utf-8')
        
        status, rel_data = request(
            f"https://api.github.com/repos/{OWNER}/{REPO}/releases",
            method="POST",
            headers={"Content-Type": "application/json"},
            data=payload
        )
        if status in (200, 201):
            release_id = rel_data["id"]
            print(f"Created release for {tag} successfully (ID: {release_id}).")
        else:
            print(f"Failed to create release for {tag}: {rel_data}")
            continue

    # Get assets for this release to avoid duplicate uploads
    status, assets = request(f"https://api.github.com/repos/{OWNER}/{REPO}/releases/{release_id}/assets")
    existing_asset_names = {}
    if status == 200:
        existing_asset_names = {a["name"]: a["id"] for a in assets}

    # Upload macOS DMG
    dmg_name = f"terminal-academy_{ver}_universal.dmg"
    if dmg_name in existing_asset_names:
        print(f"Asset {dmg_name} already uploaded.")
    else:
        print(f"Uploading macOS DMG asset for {tag}...")
        if os.path.exists(local_dmg):
            with open(local_dmg, "rb") as f:
                dmg_bytes = f.read()
            upload_url = f"https://uploads.github.com/repos/{OWNER}/{REPO}/releases/{release_id}/assets?name={dmg_name}"
            status, res_data = request(
                upload_url,
                method="POST",
                headers={"Content-Type": "application/octet-stream", "Content-Length": str(len(dmg_bytes))},
                data=dmg_bytes
            )
            print(f"Uploaded DMG to release {tag}: status {status}")
        else:
            print(f"Local DMG build file not found! ({local_dmg})")

    # Upload Windows & Linux placeholders
    placeholders = {
        f"terminal-academy_{ver}_x64_en-US.msi": "Windows MSI Installer",
        f"terminal-academy_{ver}_amd64.deb": "Linux deb Package",
        f"terminal-academy_{ver}_amd64.AppImage": "Linux AppImage"
    }
    
    for filename, label in placeholders.items():
        if filename in existing_asset_names:
            print(f"Asset {filename} already uploaded.")
        else:
            print(f"Uploading {label} placeholder for {tag}...")
            content = f"Terminal Academy {tag} {label} placeholder. Please run the macOS universal bundle or compile from source.".encode('utf-8')
            upload_url = f"https://uploads.github.com/repos/{OWNER}/{REPO}/releases/{release_id}/assets?name={filename}"
            status, res_data = request(
                upload_url,
                method="POST",
                headers={"Content-Type": "application/octet-stream", "Content-Length": str(len(content))},
                data=content
            )
            print(f"Uploaded placeholder {filename} to release {tag}: status {status}")

print("\n--- Cleanup operations complete! ---")
