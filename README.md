# t//a — Terminal Academy 🚀

An international, systems-first educational platform teaching real-world Linux administration, network architecture, and DevOps through an interactive, high-density desktop environment.

---

### **v2.1.1 (Patch Release)**

`t//a` features an ultra-lightweight cross-platform client compile using **Tauri v2** and Rust, resulting in an exceptionally small installer footprint compared to resource-heavy Electron alternatives:
* **macOS DMG Installer:** ~6 MB
* **Windows MSI Setup:** ~3 MB
* **Linux DEB Package:** ~4 MB

---

## 🚀 Key Architectural Pillars

* **Figma-Style Draggable Skill-Tree Canvas:** An interactive, bounded panning roadmap board workspace that lets students navigate nodes smoothly with hardware-accelerated transforms.
* **Zero-Risk Sandbox Virtualization:** A local container execution loop running on top of Docker. Incidents are completed in safe, isolated workspaces with no threat to the host OS.
* **AI Mentor Ank:** A witty, sarcastic Socratic guide powered by Gemini API, designed to provide conceptual hints and architecture critiques without giving away direct answers.

---

## 🛠️ Curriculum Syllabus Map (2026 Expansion)

The skill tree is divided into modules spanning Linux essentials through advanced hosting and bare-metal operations:

### **1. Linux & Systems Basics**
* CLI navigation, shell configuration, standard stream redirections, and environmental variables.
* Multi-user setups, group permissions, and strict `sudoers` administration.

### **2. Networking & Docker Orchestration**
* Port-forwarding configurations, secure local/remote SSH tunnels, and iptables-based firewalls.
* Docker volume namespaces, custom multi-tier Docker Compose stacks, and internal virtual networks.

### **3. Bare-Metal Survival Skills (Phase 3 Ingestion)**
* **Automated Log Analysis:** Parse and extract telemetry patterns from high-volume stream logs using `grep`, `awk`, `sed`, and `journalctl`.
* **Advanced Git Infrastructure:** Setup bare git repositories, manage remote upstreams, resolve merge conflicts via interactive rebase, and write automated server deployment hooks (`post-receive`).
* **Linux OS Hardening & Auditing:** Tweak kernel configs via `sysctl`, profile system resources, configure file system boundaries, and enforce cgroups compliance.

---

## 📂 Repository Layout

* `/terminal-academy-desktop`: Core Tauri application (React + TypeScript frontend, Rust native system state/PTY bridge).
* `/web-landing`: Clean static promotional site and waitlist registrar.

---

## 💻 Quick Start Guide

### Running the Desktop Environment Locally
1. Navigate to the desktop client workspace:
   ```bash
   cd terminal-academy-desktop
   ```
2. Install standard dependencies:
   ```bash
   npm install
   ```
3. Boot the local development environment:
   ```bash
   npm run dev
   ```
   *(Note: You can also use the helper script `./start.sh` in the root workspace to auto-resolve active process locks and bootstrap Tauri.)*

### Prerequisites
* **Node.js** (v18+)
* **Rust & Cargo compiler toolchain** (to build Tauri native bindings)
* **Docker Engine** (running locally for sandbox containers)
