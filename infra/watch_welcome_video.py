import os
import sys
import subprocess
import re
import json

PUBLIC_DIR = "/Users/ank/Documents/CODENAME_TERMINAL_ACADEMY/terminal-academy-desktop/public"
APP_DIR = "/Users/ank/Documents/CODENAME_TERMINAL_ACADEMY/terminal-academy-desktop"
ROOT_DIR = "/Users/ank/Documents/CODENAME_TERMINAL_ACADEMY"

def get_token():
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        return token
    for path in [".env", "../.env", "../../.env"]:
        if os.path.exists(path):
            with open(path, "r") as f:
                for line in f:
                    if line.strip().startswith("GITHUB_TOKEN="):
                        return line.strip().split("=")[1].strip().strip('"').strip("'")
    return ""

def check_and_integrate():
    # Look for welcome.mp4 or welcome.webm
    video_file = None
    for name in ["welcome.mp4", "welcome.webm"]:
        p = os.path.join(PUBLIC_DIR, name)
        if os.path.exists(p):
            video_file = name
            break
            
    if not video_file:
        print("No welcome video found yet.")
        return False
        
    print(f"Found welcome video: {video_file}!")
    
    # 1. Update App.tsx to use video element
    app_tsx_path = os.path.join(APP_DIR, "src/App.tsx")
    with open(app_tsx_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Replace the text-based brand-logo / "//" placeholder with video element
    target_logo = """              <div 
                id="welcome-logo-container"
                style={{
                  width: '80px',
                  height: '80px',
                  borderRadius: '20px',
                  background: 'rgba(255, 85, 0, 0.05)',
                  border: '2px solid var(--accent-primary)',
                  boxShadow: '0 0 20px rgba(255, 85, 0, 0.3)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '2.5rem',
                  fontWeight: 'bold',
                  color: 'var(--accent-primary)',
                  marginBottom: '15px',
                  textShadow: '0 0 10px rgba(255, 85, 0, 0.5)',
                  transition: 'all 0.5s ease'
                }}
              >
                //
              </div>"""

    replacement_logo = f"""              <div 
                id="welcome-logo-container"
                style={{{{
                  width: '300px',
                  height: '225px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  marginBottom: '15px',
                  transition: 'all 0.5s ease'
                }}}}
              >
                <video 
                  src="/{video_file}" 
                  autoPlay 
                  loop 
                  muted 
                  playsInline 
                  style={{{{ 
                    width: '100%', 
                    height: '100%', 
                    objectFit: 'contain' 
                  }}}} 
                />
              </div>"""

    if target_logo in content:
        content = content.replace(target_logo, replacement_logo)
    else:
        # Fallback if already modified or slightly different
        print("Warning: target logo markup not found or already replaced.")
        
    # Bump version from 2.0.2 to 2.0.3
    content = content.replace("2.0.2", "2.0.3")
    with open(app_tsx_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    # Update package.json version
    pkg_path = os.path.join(APP_DIR, "package.json")
    with open(pkg_path, "r", encoding="utf-8") as f:
        pkg = json.load(f)
    pkg["version"] = "2.0.3"
    with open(pkg_path, "w", encoding="utf-8") as f:
        json.dump(pkg, f, indent=2)
        
    # Update tauri.conf.json version
    tauri_path = os.path.join(APP_DIR, "src-tauri/tauri.conf.json")
    with open(tauri_path, "r", encoding="utf-8") as f:
        tauri_cfg = json.load(f)
    tauri_cfg["version"] = "2.0.3"
    with open(tauri_path, "w", encoding="utf-8") as f:
        json.dump(tauri_cfg, f, indent=2)
        
    # Update cleanup_releases.py
    cleanup_path = os.path.join(ROOT_DIR, "infra/cleanup_releases.py")
    with open(cleanup_path, "r", encoding="utf-8") as f:
        cleanup_cfg = f.read()
    
    # Add v2.0.3 entry to releases_to_keep
    old_keep = '"v2.0.2": {\n        "title": "v2.0.2 - Transitions & UI Improvements",\n        "body": "Introduces smooth multi-stage startup transitions and exit animation overlay."\n    }'
    new_keep = '"v2.0.2": {\n        "title": "v2.0.2 - Transitions & UI Improvements",\n        "body": "Introduces smooth multi-stage startup transitions and exit animation overlay."\n    },\n    "v2.0.3": {\n        "title": "v2.0.3 - Welcome Animation Update",\n        "body": "Official release integrating the custom transparent welcome animation video asset."\n    }'
    cleanup_cfg = cleanup_cfg.replace(old_keep, new_keep)
    with open(cleanup_path, "w", encoding="utf-8") as f:
        f.write(cleanup_cfg)
        
    # 2. Build Tauri App
    print("Building Tauri app...")
    subprocess.run(["npm", "run", "tauri", "build"], cwd=APP_DIR, check=True)
    
    # 3. Git commit, tag, push
    token = get_token()
    if not token:
        print("Error: GITHUB_TOKEN not found in environment or .env file.")
        return False
        
    remote_url = f"https://x-token-auth:{token}@github.com/888ank888/terminal-academy-by-ank.git"
    
    print("Committing and pushing tag v2.0.3...")
    subprocess.run(["git", "add", "."], cwd=ROOT_DIR, check=True)
    subprocess.run(["git", "commit", "-m", "feat: integrate welcome video animation and bump version to v2.0.3"], cwd=ROOT_DIR, check=True)
    subprocess.run(["git", "push", remote_url, "main"], cwd=ROOT_DIR, check=True)
    subprocess.run(["git", "tag", "v2.0.3"], cwd=ROOT_DIR, check=True)
    subprocess.run(["git", "push", remote_url, "v2.0.3"], cwd=ROOT_DIR, check=True)
    
    # 4. Run cleanup releases script to publish
    print("Publishing release on GitHub...")
    subprocess.run(["python3", "infra/cleanup_releases.py"], cwd=ROOT_DIR, check=True)
    
    print("Welcome animation integrated and published successfully as v2.0.3!")
    return True

if __name__ == "__main__":
    try:
        success = check_and_integrate()
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    except Exception as e:
        print(f"Error during welcome video integration: {str(e)}", file=sys.stderr)
        sys.exit(1)
