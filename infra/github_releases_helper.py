import os
import sys
import json
import urllib.request
import urllib.error

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

tags = [
    "v2.0.0-desktop",
    "v2.1.0",
    "v2.2.0",
    "v2.2.1"
]

import ssl

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

existing_releases = {r["tag_name"]: r["id"] for r in releases}

local_dmg = "/Users/ank/Documents/CODENAME_TERMINAL_ACADEMY/terminal-academy-desktop/src-tauri/target/release/bundle/dmg/terminal-academy_2.0.0_x64.dmg"

# Check if we have 2.2.1 built file
local_dmg_221 = "/Users/ank/Documents/CODENAME_TERMINAL_ACADEMY/terminal-academy-desktop/src-tauri/target/release/bundle/dmg/terminal-academy_2.2.1_x64.dmg"
if os.path.exists(local_dmg_221):
    local_dmg = local_dmg_221
elif not os.path.exists(local_dmg):
    # Fallback to check any DMG in the folder
    dmg_dir = "/Users/ank/Documents/CODENAME_TERMINAL_ACADEMY/terminal-academy-desktop/src-tauri/target/release/bundle/dmg"
    if os.path.exists(dmg_dir):
        files = [f for f in os.listdir(dmg_dir) if f.endswith(".dmg")]
        if files:
            local_dmg = os.path.join(dmg_dir, files[0])

print(f"Using local DMG source file: {local_dmg}")

for tag in tags:
    ver = tag.replace("v", "")
    print(f"\n--- Processing {tag} ---")
    
    if tag in existing_releases:
        release_id = existing_releases[tag]
        print(f"Release for {tag} already exists (ID: {release_id}).")
    else:
        # Create release
        payload = json.dumps({
            "tag_name": tag,
            "name": tag,
            "body": f"Terminal Academy Desktop release {tag}",
            "draft": False,
            "prerelease": False
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
            
    # Get existing assets for this release to avoid duplicate uploads
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

print("\n--- All operations complete! ---")
