# Terminal Academy 🚀

An international, systems-first educational platform teaching real Linux administration, network architecture, and DevOps to adolescents through an interactive command-line interface.

---

## 🛠️ Quick Start Guide

### Option 1: Lightweight Local Demo (No Docker Required)
The core client is built using Python's standard `curses` library and runs natively in your terminal. It is extremely lightweight (~70KB) and doesn't require any complex setup.

**Requirements:** macOS or Linux (Windows users must run inside WSL2), Python 3.10+.

1. Clone the repository:
   ```bash
   git clone https://github.com/888ank888/terminal-academy-by-ank.git
   cd terminal-academy-by-ank/cli-client
   ```
2. Launch the terminal client:
   ```bash
   python3 main.py
   ```
3. Use `Tab` to switch focus between the **Work Terminal** shell prompt and the **ANK Monitor** system utilities menu.

---

### Option 2: Full Sandboxed Infrastructure (Docker & gVisor)
For the full multi-tenant, secure learning sandbox environment, run the stack using Docker Compose. This routes execution inside secure, userspace-virtualized gVisor containers.

**Requirements:** Docker & Docker Compose with `runsc` (gVisor runtime) enabled.

1. Provision the sandbox and start the services:
   ```bash
   docker compose up -d --build
   ```
2. Attach to the secure sandbox container:
   ```bash
   docker exec -it academy-sandbox /bin/bash
   ```

---

## 📂 Repository Structure
* `/cli-client`: Python-based terminal HUD client, authentication gates, and telemetry simulators.
* `/web-landing`: High-fidelity SaaS console landing page and Firebase registration sync.
* `Dockerfile.sandbox`: Alpine-based lightweight container blueprint for isolated labs.
