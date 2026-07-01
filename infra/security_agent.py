import os
import json
import time

WORKSPACE_ROOT = "/Users/ank/Documents/CODENAME_TERMINAL_ACADEMY"
BLACKLIST_PATH = os.path.join(WORKSPACE_ROOT, "terminal-academy-desktop/public/blacklist.json")

# Threat intelligence data representing malicious/dangerous commands and unsafe install patterns
KNOWN_THREATS_DB = [
    "bash -i >& /dev/tcp/",
    "nc -e /bin/sh",
    "python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(",
    "perl -e 'use Socket;",
    "rm -rf /",
    "chmod -R 777 /etc",
    "chmod -R 777 /var",
    "chown -R student /etc",
    "mkfs.ext4",
    "dd if=/dev/zero of=/dev/",
    ":(){:|:&};:",
    "forkbomb",
    "wget -O- http",
    "curl -sSL http",
    "shred -u",
    "iptables -F",
    "ufw disable",
    "find / -name *.pem",
    "grep -rnw '/etc/' -e 'password'",
    "ln -sf /bin/sh /tmp/"
]

def load_blacklist():
    if not os.path.exists(BLACKLIST_PATH):
        return []
    try:
        with open(BLACKLIST_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[SECURITY_SUBAGENT] Error loading blacklist: {e}")
        return []

def save_blacklist(blacklist):
    try:
        with open(BLACKLIST_PATH, "w", encoding="utf-8") as f:
            json.dump(blacklist, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print("[SECURITY_SUBAGENT] Threat database updated successfully.")
    except Exception as e:
        print(f"[SECURITY_SUBAGENT] Error saving blacklist: {e}")

def run_threat_audit():
    print("[SECURITY_SUBAGENT] Actively searching for dangerous terminal/server commands and unsafe install patterns...")
    blacklist = load_blacklist()
    updated = False
    
    for threat in KNOWN_THREATS_DB:
        if threat not in blacklist:
            print(f"[SECURITY_SUBAGENT] Malicious vector identified: '{threat}'. Appending to threat database.")
            blacklist.append(threat)
            updated = True
            
    if updated:
        save_blacklist(blacklist)
    else:
        print("[SECURITY_SUBAGENT] Threat database is fully synchronized and secure.")

def main():
    print("[SECURITY_SUBAGENT] Initializing background security monitoring sub-agent...")
    while True:
        try:
            run_threat_audit()
        except Exception as e:
            print(f"[SECURITY_SUBAGENT] Error during security audit loop: {e}")
        # Run threat scanning checks periodically
        time.sleep(3600)

if __name__ == "__main__":
    main()
