# Terminal Academy 🚀 (v2.0.0)

An international, systems-first educational platform teaching real Linux administration, network architecture, and DevOps to teens through an interactive, glassmorphic desktop environment.

---

## 🚀 Key Features in v2.0.0
* **Interactive Branching Skill Tree:** Visualize and select courses across an interconnected 20-Node syllabus roadmap (from Linux Core to Docker containers, reverse proxies, databases, and Minecraft servers).
* **Tauri Desktop Application:** High-performance desktop application built using Tauri (Rust), React (TypeScript), and Tailwind-inspired custom CSS themes.
* **AI Mentor Ank:** Powered by Gemini, Ank acts as your personal mission controller, dynamically guiding you through practical terminal incidents.
* **Secure Sandbox Virtualization:** Sandboxed systems environment runs inside Alpine Linux containers, isolated by gVisor (`runsc`) user space kernel shims.

---

## 🛠️ Quick Start Guide

### Spawning the Desktop client
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
   npm run dev
   ```
   *(Note: You can also execute `./start.sh` in the repository root to automatically resolve socket conflicts and boot the Tauri environment in one step.)*

### Requirements:
* Node.js (v18+)
* Rust & Cargo (to compile Tauri backend bindings)
* A Gemini API Key (configured inside the application dashboard)

---

## 📂 Repository Structure
* `/terminal-academy-desktop`: Tauri desktop client (React frontend & Rust native PTY/SSH core).
* `/academy_showcase/web-landing`: High-fidelity, glassmorphic desktop download website.
* `/infra`: Server provisioning and telemetry sockets.
