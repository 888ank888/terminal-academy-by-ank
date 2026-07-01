# Terminal Academy 🚀

An international, systems-first educational platform teaching real Linux administration, network architecture, and DevOps to adolescents through an interactive command-line interface.

---

# Terminal Academy 🚀

An international, systems-first educational platform teaching real Linux administration, network architecture, and DevOps to adolescents through an interactive glassmorphic desktop environment.

---

## 🛠️ Quick Start Guide

### Option 1: Tauri Desktop Application (Recommended)
The primary client is a cross-platform desktop application built using Tauri (Rust), React (TypeScript), and Vite. It features a rich glassmorphic HUD dashboard, an active system monitor, diagnostic libraries, and an interactive AI Mentor Ank (powered by Gemini).

To run the desktop application locally:
1. Navigate to the desktop client folder:
   ```bash
   cd terminal-academy-desktop
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development stack:
   ```bash
   npm run desktop
   ```
   *(Note: You can also use the `./start.sh` launcher script in the root directory, which automatically clears any socket conflicts and launches the Tauri development environment in one command.)*

**Requirements:**
* Node.js (v18+)
* Rust & Cargo (to compile the Tauri backend)
* An SSH key at `~/.ssh/id_ed25519` authorized to connect to the remote sandbox allocator server.
* A Gemini API Key (configured in the app settings, or populated in `public/config.json`).

---

### Option 2: Legacy CLI Curses Client (Alternative Demo)
A lightweight command-line interface HUD client built using Python's standard `curses` library.

1. Navigate to the CLI client folder:
   ```bash
   cd cli-client
   ```
2. *(Windows Only)* Install the curses library port:
   ```cmd
   pip install windows-curses
   ```
3. Launch the terminal client:
   ```bash
   python3 main.py
   ```

---

### Option 3: Local Sandboxed Infrastructure (Docker & gVisor)
If you wish to host the sandbox environments locally rather than using the remote server, you can spawn the secure multi-tenant stack via Docker Compose.

**Requirements:** Docker with the `runsc` (gVisor) runtime configured.
1. Spawns the sandbox and sidecar services:
   ```bash
   docker compose up -d --build
   ```
2. Attach to the secure sandbox container:
   ```bash
   docker exec -it academy-sandbox /bin/bash
   ```

---

## 📂 Repository Structure
* `/terminal-academy-desktop`: Tauri desktop client (React frontend & Rust native PTY/SSH core).
* `/cli-client`: Legacy Python curses terminal HUD client and sandboxed Dockerfile configuration.
* `/web-landing`: High-fidelity B2B SaaS console landing page.
* `/infra`: Server provisioning and telemetry sockets.

