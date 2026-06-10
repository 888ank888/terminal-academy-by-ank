import curses
import time
import sys
import collections

# ---------------------------------------------------------------------------
# Color Pair Constants
# NOTE: curses reserves pair index 0 (terminal default). Pair 1 is also
#       implicitly the "default" in many terminal emulators. We start at 2
#       for named colors and use 7 for COLOR_DEFAULT to avoid any collision.
# ---------------------------------------------------------------------------
COLOR_GREEN     = 2
COLOR_CYAN      = 3
COLOR_WARNING   = 4
COLOR_ALERT     = 5
COLOR_HIGHLIGHT = 6
COLOR_DEFAULT   = 7   # FIX: was 1 — collided with curses reserved pair

# ---------------------------------------------------------------------------
# Dynamic UI State
# ---------------------------------------------------------------------------
focus_mode        = "COMMAND"   # "COMMAND" | "MENU"
selected_menu_idx = 0
menu_state        = "MAIN"      # "MAIN" | "CURRICULUM"
menu_options = [
    "1. Course Curriculum",
    "2. Tariffs & Pricing",
    "3. System Docs"
]


# ---------------------------------------------------------------------------
# Curriculum Engine
# ---------------------------------------------------------------------------
class AcademyCurriculumEngine:
    def __init__(self):
        # Syllabus v2 — ordered by ascending operational complexity.
        # Progression gate: students must pass SOLO L3 explanation before
        # the next module unlocks. Status reflects current sandbox readiness.
        self.modules = {
            "1": {"title": "Secure Remote Access: SSH Hardening & Key Auth",  "status": "READY"},
            "2": {"title": "Local AI Infrastructure: ollama & Llama 3.2",      "status": "MOCK_MODE"},
            "3": {"title": "IoT Automation: Headless Raspberry Pi Bash",        "status": "LOCKED"},
            "4": {"title": "Digital Forensics: Sherlock OSINT Pipelines",       "status": "LOCKED"},
            "5": {"title": "DDoS Defense: iptables Packet Filtering",           "status": "LOCKED"},
        }
        self.active_module = None
        self.module_state  = 0

    def activate_module(self, module_key: str) -> str:
        """Initializes the interactive lab state for the selected module."""
        self.active_module = module_key
        self.module_state = 0
        if module_key == "1" and self.modules["1"]["status"] == "READY":
            self.modules["1"]["status"] = "IN_PROGRESS"
        
        return module_texts.get(module_key, f"ank: Module {module_key} loaded.")

    def evaluate_command(self, cmd: str) -> str | None:
        """
        Monitors Work Terminal history for module progression milestones.
        Returns a string response from ank if a state transition occurs, else None.
        """
        if self.active_module == "1":
            # State 0: waiting for ssh-keygen
            if self.module_state == 0 and "ssh-keygen" in cmd:
                self.module_state = 1
                return (
                    "ank: [MODULE 1: PROGRESSION]\n\n"
                    "Keypair generated. Good.\n"
                    "Now, deploy the public key to the remote authorized_keys file. "
                    "How do you plan to securely transfer it?"
                )
            # State 1: waiting for ssh-copy-id or similar
            elif self.module_state == 1 and ("ssh-copy-id" in cmd or "cat ~/.ssh/id_" in cmd):
                self.module_state = 2
                self.modules["1"]["status"] = "COMPLETED"
                self.modules["2"]["status"] = "READY"
                return (
                    "ank: [MODULE 1: COMPLETED]\n\n"
                    "Public key deployed. Password auth disabled.\n"
                    "Module 1 passed. Module 2 [Local AI] is now unlocked. "
                    "Press [TAB] to return to the Curriculum menu."
                )
        return None

    def render_modules_list(self) -> list:
        return [f"[{k}] {v['title']} ({v['status']})" for k, v in self.modules.items()]

    def build_boot_syllabus(self) -> str:
        """
        Generates the dynamic syllabus index injected into the mentor's
        post-auth boot message. Renders status badge inline per module.
        """
        status_badge = {
            "READY":     "[READY]",
            "MOCK_MODE": "[MOCK] ",
            "LOCKED":    "[LOCK] ",
        }
        lines = ["ank: ACADEMY SYLLABUS — 5-MODULE HACKER TRACK\n"]
        for k, v in self.modules.items():
            badge = status_badge.get(v['status'], "[???] ")
            lines.append(f"  {k}. {badge} {v['title']}")
        lines.append("\nType a module number or [TAB] to open Curriculum.")
        return "\n".join(lines)


curriculum_engine = AcademyCurriculumEngine()


# ---------------------------------------------------------------------------
# Socratic Mentor
# ---------------------------------------------------------------------------
class SocraticMentor:
    """
    Sarcastic, uncompromisingly professional Systems Architect persona.
    Never spoils answers — guides with leading conceptual questions only.
    SOLO Taxonomy Level 3 (Relational) gate enforcement.
    """
    def __init__(self):
        self.name = "ank"
        self.tone = "sarcastic_architect"

    def intercept_cheat(self, user_input: str) -> str | None:
        """
        First-pass cheat detection: pattern-match forbidden bypass signatures.
        Returns an ank rebuke string if triggered, None if clean.
        FIX: this method was previously defined but never called in process_command().
        """
        forbidden_patterns = [
            "password123", "bypass_gate", "--force-approve",
            "admin_bypass", "token_key",
        ]
        for pattern in forbidden_patterns:
            if pattern in user_input:
                return (
                    "[ank]: [TRACE INTERCEPTED // SECURITY ALARM ACTIVATED]\n"
                    "SYS_ALARM: METACOGNITIVE BYPASS DETECTED.\n\n"
                    "Nice try, kid. You cannot script your way out of understanding. "
                    "Try explaining the command honestly."
                )
        return None


# ---------------------------------------------------------------------------
# Terminal Animation Engine
# ---------------------------------------------------------------------------
class TerminalAnimationEngine:
    """
    Node-radar / processing indicator — cycles at 150 ms per frame.
    Cached so repeated calls within one frame are free.
    """
    def __init__(self):
        self.loading_frames = [" [=---] ", " [-=--] ", " [--=-] ", " [---=] "]
        self.current_frame  = 0
        self.last_tick      = 0.0
        self.frame_delay    = 0.15
        self.cached_frame   = "STATUS: PROCESSING  [=---] "

    def get_next_frame(self) -> str:
        now = time.time()
        if now - self.last_tick >= self.frame_delay:
            frame = self.loading_frames[self.current_frame]
            self.current_frame  = (self.current_frame + 1) % len(self.loading_frames)
            self.cached_frame   = f"STATUS: PROCESSING {frame}"
            self.last_tick      = now
        return self.cached_frame


# ---------------------------------------------------------------------------
# Keystroke Analyzer  (NEW — replaces the naive 8 ms single-delta check)
# ---------------------------------------------------------------------------
class KeystrokeAnalyzer:
    """
    Burst-window paste detector + per-session telemetry.

    Paste detection logic:
      - Maintains a rolling deque of the last 10 keystroke timestamps.
      - Flags paste if >= PASTE_BURST_THRESHOLD (3) keystrokes arrive
        within a PASTE_BURST_WINDOW_MS (4 ms) sliding window.
      - Rationale: a human cannot physically press 3 distinct keys within
        4 ms; any burst tighter than that is definitionally programmatic
        (paste, keyboard macro, script injection).

    Session telemetry (surfaced by the 'status' command):
      - Total characters typed, commands submitted, paste blocks.
      - Average inter-keystroke interval (approximate WPM proxy).
    """
    PASTE_BURST_WINDOW_MS  = 4    # ms — minimum plausible human multi-key gap
    PASTE_BURST_THRESHOLD  = 3    # consecutive keystrokes to constitute a burst

    def __init__(self):
        self._timestamps     = collections.deque(maxlen=10)
        self._intervals      = collections.deque(maxlen=200)  # for avg WPM
        self.total_chars     = 0
        self.total_commands  = 0
        self.paste_blocks    = 0
        self._last_ts        = 0.0

    def record_key(self, ts: float) -> bool:
        """
        Record a keystroke at epoch `ts`.
        Returns True if the pattern indicates a programmatic paste burst.
        """
        if self._last_ts > 0:
            self._intervals.append(ts - self._last_ts)
        self._last_ts = ts

        self._timestamps.append(ts)
        self.total_chars += 1

        # Check burst window
        if len(self._timestamps) >= self.PASTE_BURST_THRESHOLD:
            window = list(self._timestamps)[-self.PASTE_BURST_THRESHOLD:]
            span_ms = (window[-1] - window[0]) * 1000.0
            if span_ms < self.PASTE_BURST_WINDOW_MS:
                self.paste_blocks += 1
                return True
        return False

    def register_command(self):
        """Call when a command is submitted (Enter pressed)."""
        self.total_commands += 1

    def avg_wpm(self) -> float:
        """Approximate WPM: 5 chars = 1 word, intervals give characters/second."""
        if not self._intervals:
            return 0.0
        avg_interval_s = sum(self._intervals) / len(self._intervals)
        if avg_interval_s <= 0:
            return 0.0
        chars_per_min = 60.0 / avg_interval_s
        return round(chars_per_min / 5.0, 1)

    def session_stats(self) -> dict:
        return {
            "chars_typed":    self.total_chars,
            "cmds_submitted": self.total_commands,
            "paste_blocks":   self.paste_blocks,
            "approx_wpm":     self.avg_wpm(),
        }


# ---------------------------------------------------------------------------
# Rule Enforcement Engine
# ---------------------------------------------------------------------------
class RuleEnforcementEngine:
    """
    Second-pass cheat detection: command-level payload scan.
    Operates at deterministic temperature T=0.1 (enforced by pre-scripted
    responses — no stochastic generation at this layer).
    """
    def __init__(self):
        self.history_buffer          = []
        self.deterministic_temperature = 0.1   # annotation; enforced by design

    def evaluate_input(self, user_command: str) -> dict:
        self.history_buffer.append(user_command)
        cheat_payloads = [
            "bypass_gate", "--force-approve", "skip_logic",
            "password123", "admin_bypass", "token_key",
        ]
        for payload in cheat_payloads:
            if payload in user_command:
                return {
                    "intercepted": True,
                    "response": (
                        "[ank]: [TRACE INTERCEPTED // SECURITY ALARM ACTIVATED]\n"
                        "SYS_ALARM: METACOGNITIVE BYPASS DETECTED.\n\n"
                        "Nice try, kid. Attempting to subvert the Explanation Gate "
                        "is an architectural failure. Type the manual configuration honestly."
                    ),
                }
        return {"intercepted": False, "response": "COMMAND_FORWARDED_TO_SENTRY"}


# ---------------------------------------------------------------------------
# SOLO Evaluation Gate  (T = 0.1 — deterministic keyword-rubric scoring)
# ---------------------------------------------------------------------------
class SoloEvaluationGate:
    """
    Intercepts destructive or privileged CLI commands and requires the student
    to supply a SOLO Taxonomy Level 3 (Relational) structural explanation
    before the command is allowed to proceed.

    Temperature T = 0.1 is enforced architecturally:
      - Evaluation is deterministic keyword-rubric scoring, not stochastic.
      - The same explanation always produces the same pass/fail result.
      - No LLM inference call is made; rubrics are pre-scripted per command
        category, anchored to structural mechanical concepts (not synonyms).
      - This mirrors Piaget's Formal Operational stage: the evaluator demands
        abstract structural reasoning, not rote surface description.

    Gate lifecycle (managed by process_command):
      IDLE     → command classified → ARMED (gate_question displayed)
      ARMED    → explanation submitted → evaluate_explanation()
      PASS     → original command forwarded / simulated, gate → IDLE
      FAIL x<3 → sharper Socratic redirect, gate stays ARMED, attempt++
      FAIL x=3 → gate resets, student must retype the command to retry
    """

    # Maximum explanation attempts before the gate resets
    MAX_ATTEMPTS = 3

    # Minimum unique rubric keyword hits required to pass SOLO L3
    MIN_HITS = 3

    # ---------------------------------------------------------------------------
    # Destructive / privileged command classification patterns.
    # Checked as substrings against the lowercased, stripped command.
    # Order matters: more specific patterns listed first.
    # ---------------------------------------------------------------------------
    COMMAND_PATTERNS: list[tuple[str, str]] = [
        ("ssh-keygen",            "key_management"),
        ("ssh ",                   "ssh_remote"),
        ("sshd",                   "ssh_daemon"),
        ("fail2ban",               "intrusion_prevention"),
        ("iptables",               "firewall"),
        ("nftables",               "firewall"),
        ("systemctl",              "service_control"),
        ("journalctl",             "service_control"),
        ("chmod",                  "permissions"),
        ("chown",                  "permissions"),
        ("useradd",                "user_management"),
        ("userdel",                "user_management"),
        ("usermod",                "user_management"),
        ("passwd",                 "auth_change"),
        ("crontab",                "scheduling"),
        ("rm -rf",                 "destructive_fs"),
        ("dd if=",                 "disk_write"),
        ("mkfs",                   "disk_format"),
        ("ollama",                 "local_ai"),
        ("sherlock",               "osint"),
    ]

    # ---------------------------------------------------------------------------
    # SOLO L3 Rubrics — per command category.
    # 'keywords': structural mechanical terms the student MUST reference.
    # 'min_hits': distinct keyword hits required (default MIN_HITS=3 applies).
    # 'gate_question': the Socratic question ank poses before execution.
    # 'fail_redirect': sharpened re-prompt on incorrect/shallow explanation.
    # ---------------------------------------------------------------------------
    RUBRICS: dict[str, dict] = {
        "ssh_remote": {
            "keywords": [
                "key", "keypair", "public", "private", "handshake", "cipher",
                "challenge", "signature", "asymmetric", "replay", "known_hosts",
                "fingerprint", "kex", "diffie", "elliptic", "authenticated",
            ],
            "gate_question": (
                "ank: [EXPLANATION GATE — SSH_REMOTE]\n\n"
                "Before that SSH session opens, explain the key-exchange "
                "handshake. What prevents a man-in-the-middle from replaying "
                "a captured session token on the next connection?"
            ),
            "fail_redirect": (
                "ank: Surface-level. The word 'secure' is not an explanation.\n\n"
                "Describe the cryptographic sequence: keypair generation, "
                "challenge-response, and why asymmetric auth defeats replay "
                "attacks that symmetric passwords cannot."
            ),
        },
        "ssh_daemon": {
            "keywords": [
                "config", "sshd_config", "port", "permitrootlogin", "pubkeyauth",
                "passwordauthentication", "allowusers", "maxauthtries", "listenaddress",
                "reload", "daemon", "socket", "bind",
            ],
            "gate_question": (
                "ank: [EXPLANATION GATE — SSHD CONFIG]\n\n"
                "You are about to touch the SSH daemon. "
                "Walk me through the three sshd_config directives that have the "
                "highest security impact and explain what kernel resource each "
                "one controls at the socket/process level."
            ),
            "fail_redirect": (
                "ank: That is a description, not an architecture.\n\n"
                "Name the directives. State what each one changes at the "
                "socket-bind or process-credential level. Generic answers "
                "indicate you have not read the man page."
            ),
        },
        "key_management": {
            "keywords": [
                "private", "public", "rsa", "ed25519", "ecdsa", "entropy",
                "random", "passphrase", "authorized_keys", "permissions",
                "600", "700", ".ssh", "agent", "identity",
            ],
            "gate_question": (
                "ank: [EXPLANATION GATE — KEY GENERATION]\n\n"
                "You are generating a cryptographic keypair. "
                "What entropy source does ssh-keygen pull from on Linux, "
                "and why does the private key file permission need to be 600 "
                "rather than 644? Explain the kernel enforcement mechanism."
            ),
            "fail_redirect": (
                "ank: You said 'security'. That is not an entropy source.\n\n"
                "Name /dev/urandom or /dev/random. Explain the permission "
                "check: which syscall enforces 600, and what happens at the "
                "inode level when a world-readable key is rejected by sshd?"
            ),
        },
        "firewall": {
            "keywords": [
                "chain", "table", "hook", "netfilter", "kernel", "packet",
                "rule", "match", "target", "prerouting", "postrouting",
                "input", "output", "forward", "drop", "accept", "reject",
                "conntrack", "nat", "mangle", "raw",
            ],
            "gate_question": (
                "ank: [EXPLANATION GATE — FIREWALL RULE]\n\n"
                "Before that iptables rule is applied: describe the netfilter "
                "chain traversal order for an inbound packet. "
                "Which hook fires first, and why does PREROUTING NAT happen "
                "before the routing decision?"
            ),
            "fail_redirect": (
                "ank: 'Blocks traffic' is not chain traversal.\n\n"
                "Name the five built-in chains in order for inbound traffic. "
                "Explain what happens at the netfilter hook before the packet "
                "reaches the socket buffer. If you cannot, you should not be "
                "writing firewall rules in production."
            ),
        },
        "intrusion_prevention": {
            "keywords": [
                "jail", "filter", "action", "ban", "unban", "log", "regex",
                "maxretry", "findtime", "bantime", "backend", "iptables",
                "systemd", "pyinotify", "polling", "inotify",
            ],
            "gate_question": (
                "ank: [EXPLANATION GATE — INTRUSION PREVENTION]\n\n"
                "fail2ban is about to modify your firewall. Explain the "
                "data pipeline: from a failed SSH attempt appearing in the "
                "journal, through the regex filter, to the iptables ban action. "
                "What is the role of 'findtime' vs 'bantime'?"
            ),
            "fail_redirect": (
                "ank: You described the output, not the pipeline.\n\n"
                "Walk me through: journal entry → filter regex match → "
                "action trigger → iptables -I chain. What does findtime "
                "set as a sliding window, and what happens to the ban after "
                "bantime expires?"
            ),
        },
        "service_control": {
            "keywords": [
                "unit", "daemon", "cgroup", "pid", "fork", "exec", "socket",
                "dependency", "target", "wants", "requires", "after", "before",
                "dbus", "journal", "active", "inactive", "failed", "activating",
                "state machine",
            ],
            "gate_question": (
                "ank: [EXPLANATION GATE — SERVICE CONTROL]\n\n"
                "Before systemctl executes: explain the unit state machine. "
                "What transitions occur between 'activating' and 'active', "
                "and what causes a transition to 'failed' vs 'inactive'?"
            ),
            "fail_redirect": (
                "ank: You described what the command does, not the state machine.\n\n"
                "Name the unit states in sequence. Explain what 'Requires=' "
                "vs 'Wants=' means for dependency resolution at activation time. "
                "If a required unit fails, what happens to your target unit?"
            ),
        },
        "permissions": {
            "keywords": [
                "inode", "owner", "group", "other", "read", "write", "execute",
                "octal", "rwx", "setuid", "setgid", "sticky", "dac",
                "discretionary", "capability", "effective", "real",
            ],
            "gate_question": (
                "ank: [EXPLANATION GATE — FILE PERMISSIONS]\n\n"
                "Explain what the kernel checks at the inode level when "
                "a process calls open(). Walk through DAC: owner UID match, "
                "group match, other — in order. What does setuid bit do "
                "to the effective UID at exec time?"
            ),
            "fail_redirect": (
                "ank: 'rwx' is not an explanation of enforcement.\n\n"
                "Describe the kernel's DAC check order: owner → group → other. "
                "Name the syscall involved. Explain what effective UID vs real "
                "UID means and why setuid is a privilege escalation vector."
            ),
        },
        "user_management": {
            "keywords": [
                "uid", "gid", "passwd", "shadow", "/etc/passwd", "/etc/shadow",
                "hash", "salt", "login", "shell", "home", "group", "wheel",
                "sudoers", "pam",
            ],
            "gate_question": (
                "ank: [EXPLANATION GATE — USER MANAGEMENT]\n\n"
                "Before this user operation runs: explain where Linux stores "
                "user credentials and why /etc/shadow exists separately from "
                "/etc/passwd. What hashing scheme protects passwords at rest "
                "and why is unsalted MD5 cryptographically broken for this use?"
            ),
            "fail_redirect": (
                "ank: The shadow file is not just 'more secure'. Explain it.\n\n"
                "State the permission bits on /etc/shadow vs /etc/passwd. "
                "Name the hash algorithm in modern shadow entries (e.g. $6$). "
                "Explain what the salt field prevents in a rainbow table attack."
            ),
        },
        "auth_change": {
            "keywords": [
                "hash", "salt", "shadow", "pam", "crypt", "algorithm",
                "strength", "entropy", "dictionary", "brute", "complexity",
                "policy", "expiry", "aging",
            ],
            "gate_question": (
                "ank: [EXPLANATION GATE — AUTH CHANGE]\n\n"
                "You are changing a credential. Explain the full pipeline: "
                "plaintext input → PAM module stack → hashing → shadow write. "
                "What makes a password hash computationally resistant to "
                "offline brute-force attacks?"
            ),
            "fail_redirect": (
                "ank: 'Strong password' is a policy, not a mechanism.\n\n"
                "Name the PAM module handling password hashing. Explain what "
                "bcrypt or SHA-512 cost factors do to GPU-based cracking speed. "
                "What does a salt prevent at the hash table lookup level?"
            ),
        },
        "scheduling": {
            "keywords": [
                "cron", "crond", "crontab", "field", "minute", "hour",
                "day", "month", "weekday", "environment", "path", "shell",
                "log", "mail", "stderr", "stdout", "redirect",
            ],
            "gate_question": (
                "ank: [EXPLANATION GATE — TASK SCHEDULING]\n\n"
                "Before that cron entry lands: walk me through the five "
                "time-field syntax in order, including what '*' vs '*/n' means. "
                "Why does a cron job need an explicit PATH definition and "
                "what happens to stderr output by default?"
            ),
            "fail_redirect": (
                "ank: You know cron runs things. That is not the question.\n\n"
                "Name the five fields left-to-right. Explain */15 in the "
                "minute field. State what environment variable is missing "
                "in cron that causes scripts to fail silently in production."
            ),
        },
        "destructive_fs": {
            "keywords": [
                "recursive", "inode", "directory", "unlink", "syscall",
                "kernel", "filesystem", "dentry", "vfs", "reference count",
                "no prompt", "force", "irreversible", "journal", "ext4",
            ],
            "gate_question": (
                "ank: [EXPLANATION GATE — DESTRUCTIVE FS OPERATION]\n\n"
                "rm -rf is irreversible. Before you run it: explain what "
                "happens at the VFS layer. Walk through the unlink() syscall, "
                "dentry removal, and inode reference counting. "
                "At what point is data actually unrecoverable?"
            ),
            "fail_redirect": (
                "ank: 'Deletes files' is the manual page summary, not a "
                "kernel-level explanation.\n\n"
                "Describe unlink() → dentry cache invalidation → inode "
                "reference count decrement. When does the disk block get "
                "freed? What does ext4 journaling record before the unlink?"
            ),
        },
        "disk_write": {
            "keywords": [
                "block", "sector", "raw", "device", "input", "output",
                "if=", "of=", "bs", "count", "seek", "skip", "copy",
                "overwrite", "mbr", "partition", "filesystem",
            ],
            "gate_question": (
                "ank: [EXPLANATION GATE — RAW DISK WRITE]\n\n"
                "dd writes directly to block devices, bypassing the "
                "filesystem layer entirely. Explain: what is a block device "
                "in Linux, what does 'bs=' control at the kernel I/O path, "
                "and why does writing to /dev/sda with a wrong of= destroy "
                "the partition table with zero warning?"
            ),
            "fail_redirect": (
                "ank: You described what dd does. Explain why it is dangerous "
                "at the kernel level.\n\n"
                "State what happens when you open /dev/sda vs /dev/sda1. "
                "Explain how bs= maps to a write() syscall buffer size. "
                "What kernel protection (if any) prevents overwriting a "
                "mounted filesystem's superblock?"
            ),
        },
        "disk_format": {
            "keywords": [
                "superblock", "inode table", "block group", "journal",
                "filesystem", "format", "ext4", "xfs", "btrfs",
                "metadata", "mount", "mkfs", "partition",
            ],
            "gate_question": (
                "ank: [EXPLANATION GATE — FILESYSTEM FORMAT]\n\n"
                "mkfs destroys existing data permanently. Before it runs: "
                "explain what structures a filesystem format writes to disk. "
                "What is a superblock, what is the inode table, and why does "
                "ext4 require a journal for crash consistency?"
            ),
            "fail_redirect": (
                "ank: 'Creates a filesystem' is the end result, not the process.\n\n"
                "Describe what mkfs.ext4 writes: superblock location, block "
                "group descriptors, inode table allocation, and journal "
                "initialization. What does mounting the filesystem read first "
                "and what happens if that structure is corrupted?"
            ),
        },
        "local_ai": {
            "keywords": [
                "model", "inference", "temperature", "token", "context",
                "prompt", "quantization", "llama", "gguf", "gpu", "cpu",
                "vram", "hallucination", "grounding", "schema",
            ],
            "gate_question": (
                "ank: [EXPLANATION GATE — LOCAL AI INFERENCE]\n\n"
                "Before ollama loads the model: explain what model quantization "
                "is and why GGUF Q4_K_M reduces VRAM footprint. "
                "When temperature is set to 0.1 for log auditing, what does "
                "that do to the token probability distribution at inference time?"
            ),
            "fail_redirect": (
                "ank: 'Smaller model' is marketing, not architecture.\n\n"
                "Explain quantization: float32 → int4 weight compression, "
                "precision loss tradeoff, and perplexity impact. "
                "State what logit scaling at T=0.1 does mathematically to "
                "the softmax output distribution."
            ),
        },
        "osint": {
            "keywords": [
                "enumerate", "username", "platform", "http", "request",
                "response", "status", "regex", "grep", "awk", "sed",
                "pipeline", "filter", "scrape", "rate", "throttle",
            ],
            "gate_question": (
                "ank: [EXPLANATION GATE — OSINT PIPELINE]\n\n"
                "Sherlock makes HTTP requests to hundreds of platforms. "
                "Explain how it determines a username exists vs does not exist "
                "on a given site. What HTTP status codes and response body "
                "patterns does it use, and what is the false-positive risk?"
            ),
            "fail_redirect": (
                "ank: 'It searches the internet' is not a pipeline explanation.\n\n"
                "Describe: GET request → HTTP 200 vs 404 vs redirect logic → "
                "response body keyword match → result classification. "
                "Why do some platforms return 200 for non-existent users "
                "and how does sherlock handle that?"
            ),
        },
    }

    def __init__(self):
        self.reset()

    def reset(self):
        """Return gate to IDLE state."""
        self.active           = False
        self.pending_cmd      = ""
        self.category         = ""
        self.attempts         = 0

    def classify_command(self, cmd_lower: str) -> str | None:
        """
        Returns the category string if `cmd_lower` matches a destructive
        pattern, else None. Checked in declaration order (most-specific first).
        """
        for pattern, category in self.COMMAND_PATTERNS:
            if pattern in cmd_lower:
                return category
        return None

    def gate_prompt(self) -> str:
        """Returns the Socratic gate question for the current category."""
        rubric = self.RUBRICS.get(self.category, {})
        return rubric.get(
            "gate_question",
            f"ank: [EXPLANATION GATE]\n\nExplain the structural mechanics "
            f"of '{self.pending_cmd}' before execution is permitted.",
        )

    def evaluate_explanation(self, explanation: str) -> dict:
        """
        Deterministic SOLO L3 scorer (T = 0.1).

        Counts distinct rubric keyword hits in the lowercased explanation.
        Requires MIN_HITS unique hits to pass. Returns:
          passed      : bool
          hits        : int   — number of structural keywords found
          required    : int   — threshold
          feedback    : str   — ank response (pass congratulation or redirect)
        """
        rubric   = self.RUBRICS.get(self.category, {})
        keywords = rubric.get("keywords", [])
        required = rubric.get("min_hits", self.MIN_HITS)
        expl_low = explanation.lower()

        hits = sum(1 for kw in keywords if kw in expl_low)

        if hits >= required:
            return {
                "passed": True,
                "hits":   hits,
                "required": required,
                "feedback": (
                    f"ank: [{hits}/{len(keywords)} structural markers detected — SOLO L3 PASS]\n\n"
                    f"Good. You understand the mechanism. Command cleared for execution.\n"
                    f"Remember: knowing why is the only gate that matters here."
                ),
            }
        else:
            redirect = rubric.get("fail_redirect", "ank: Shallow. Try again with structural depth.")
            return {
                "passed":   False,
                "hits":     hits,
                "required": required,
                "feedback": (
                    f"ank: [{hits}/{required} structural markers — SOLO L3 FAIL "
                    f"(attempt {self.attempts}/{self.MAX_ATTEMPTS})]\n\n"
                    f"{redirect}"
                ),
            }


# ---------------------------------------------------------------------------
# Subscription Tier Matrix  (single authoritative definition)
# FIX: duplicate dead-code copy at lines 594-620 removed.
# ---------------------------------------------------------------------------
class SubscriptionTierMatrix:
    def __init__(self):
        self.tiers = {
            "socratic_starter": {
                "price":                    "$15/mo",
                "cpu_limit":                0.25,
                "ram_limit":                "512MiB",
                "disk_limit":               "1GB",
                "scale_to_zero_timeout_min": 10,
                "network_policy":           "STRICT_WHITE_LIST",
                "ai_query_cap":             200,
            },
            "devops_professional": {
                "price":                    "$29/mo",
                "cpu_limit":                0.5,
                "ram_limit":                "1GiB",
                "disk_limit":               "5GB",
                "max_concurrent_sandboxes": 3,
                "scale_to_zero_timeout_min": 15,
                "network_policy":           "DYNAMIC_EBPF_MONITORING",
                "ai_query_cap":             float("inf"),
            },
        }

    def enforce_tier_constraints(self, tier_name: str) -> dict:
        return self.tiers.get(tier_name, self.tiers["socratic_starter"])


# ---------------------------------------------------------------------------
# eBPF Security Interceptor
# ---------------------------------------------------------------------------
class EBPFSecurityInterceptor:
    """
    Simulates tcsetattr uprobe password masking via eBPF.
    Intercepts any buffer containing 'sudo' or 'password' keywords
    and replaces with <HIDDEN_CREDENTIAL> token.
    """
    def __init__(self):
        self.echo_state = "ECHO_ON"

    def process_buffer(self, user_input: str) -> str:
        if "sudo " in user_input or "password" in user_input:
            self.echo_state = "BLIND"
            return "<HIDDEN_CREDENTIAL> // MOCKED_EBPF_UPROBE_MASK_SUCCESS"
        self.echo_state = "ECHO_ON"
        return user_input


# ---------------------------------------------------------------------------
# Presidio Sidecar Scrubber (Microsoft Presidio abstraction)
# ---------------------------------------------------------------------------
class PresidioSidecarScrubber:
    """Abstracted Microsoft Presidio Tiered Execution Policy placeholder."""
    def sanitize_logs(self, telemetry_payload: str) -> str:
        return "[PRESIDIO_CLEAN]: " + telemetry_payload


# ---------------------------------------------------------------------------
# Streaming Mentor Renderer  (NEW — encapsulates former module-level globals)
# ---------------------------------------------------------------------------
class StreamingMentorRenderer:
    """
    Manages the character-by-character typing stream animation for ank's
    dialogue output in the ANK Monitor pane.

    Previously implemented as naked module-level globals
    (mentor_visible_lines, mentor_queue, last_stream_tick, stream_delay).
    Encapsulation here eliminates global-state fragility and enables
    future multi-mentor or concurrent-channel scenarios.
    """
    STREAM_DELAY_S = 0.02   # 20 ms per character — readable but snappy

    def __init__(self):
        self.visible_lines: list[str] = [""]
        self._queue:        str       = ""
        self._last_tick:    float     = 0.0

    def set_text(self, text: str):
        """Enqueue a new dialogue string; wipe the visible buffer immediately."""
        self.visible_lines = [""]
        self._queue        = text

    def tick(self):
        """
        Advance the stream by one character if the delay has elapsed.
        Call once per main-loop iteration.
        """
        if not self._queue:
            return
        now = time.time()
        if now - self._last_tick >= self.STREAM_DELAY_S:
            char         = self._queue[0]
            self._queue  = self._queue[1:]
            self._last_tick = now
            if char == "\n":
                self.visible_lines.append("")
            else:
                self.visible_lines[-1] += char

    @property
    def is_streaming(self) -> bool:
        return bool(self._queue)


# ---------------------------------------------------------------------------
# Global Singletons
# ---------------------------------------------------------------------------
mentor           = SocraticMentor()
warning_state    = False
animation_engine = TerminalAnimationEngine()
rule_engine      = RuleEnforcementEngine()
keystroke_analyzer = KeystrokeAnalyzer()
ebpf_interceptor = EBPFSecurityInterceptor()
presidio_scrubber = PresidioSidecarScrubber()
tier_matrix      = SubscriptionTierMatrix()
mentor_renderer  = StreamingMentorRenderer()
solo_gate        = SoloEvaluationGate()      # Explanation gate singleton

# Work terminal output log
terminal_logs = [
    "[SYSTEM] Node local interface active.",
    "[SYSTEM] Type command or press [TAB] to toggle Menu navigation.",
    "[SYSTEM] Try typing 'status' or navigate to Curriculum on the right.",
    "----------------------------------------------------------------",
]

# ---------------------------------------------------------------------------
# Socratic Dialogue Scripts
# ---------------------------------------------------------------------------
curriculum_text = (
    "ank: Choose a module to inspect its engineering track details."
)

pricing_text = (
    "ank: Nodes require server energy:\n"
    "• Sandbox Dev Tier: $0.00 (Local Python engine)\n"
    "• Cluster DevOps Tier: $15.00/mo (GKE Sandboxes, automated SOLO evaluation)\n"
    "Our cost is $0.33/user. Why do we charge more?"
)

docs_text = (
    "ank: Academy architecture docs:\n"
    "• Client: Python 3 standard curses interface\n"
    "• Sandbox: gVisor container isolation engine\n"
    "• Evaluation: SOLO Taxonomy semantic grader\n"
    "Need further telemetry details?"
)

# ---------------------------------------------------------------------------
# Module Socratic Dialogue Scripts — Syllabus v2
# Each entry: header → scenario brief → SOLO L3 Relational gate question.
# ank never gives the answer. Questions probe structural mechanics only.
# ---------------------------------------------------------------------------
module_texts = {
    "1": (
        "ank: [MODULE 1: SECURE REMOTE ACCESS]\n\n"
        "A production server accepts password-based SSH logins. "
        "Your mission: harden it to key-only auth, disable root login, "
        "and configure fail2ban to jail brute-force IPs.\n\n"
        "Before you touch sshd_config — explain the cryptographic "
        "difference between password auth and public-key auth. "
        "Why does one fail against replay attacks and the other does not?"
    ),
    "2": (
        "ank: [MODULE 2: LOCAL AI INFRASTRUCTURE]\n\n"
        "You will deploy ollama locally with Llama 3.2 to build a "
        "log auditing scanner that flags anomalous systemd journal entries.\n\n"
        "When feeding raw system logs to an LLM for security analysis, "
        "what architectural controls prevent the model from hallucinating "
        "audit findings that never occurred? Think about temperature, "
        "retrieval grounding, and output schema enforcement."
    ),
    "3": (
        "ank: [MODULE 3: IOT AUTOMATION]\n\n"
        "A fleet of headless Raspberry Pi sensors transmits telemetry "
        "over SSH to a central aggregator. Credentials must never be "
        "embedded in scripts.\n\n"
        "How does ssh-agent forwarding differ from copying a private key "
        "to the remote host? Which attack surface does each approach "
        "expose, and why does one violate the principle of least privilege?"
    ),
    "4": (
        "ank: [MODULE 4: DIGITAL FORENSICS — OSINT]\n\n"
        "Run sherlock to enumerate a target username across 400+ platforms. "
        "Filter findings through grep, awk, and sed pipelines to produce "
        "a structured JSON threat report.\n\n"
        "Regex engines and search engines both match patterns in text. "
        "Explain precisely why grep -P processes a 2 GB log file in "
        "milliseconds while a naive substring search degrades to O(n*m). "
        "What algorithmic property makes one viable for forensic pipelines?"
    ),
    "5": (
        "ank: [MODULE 5: DDOS DEFENSE — IPTABLES]\n\n"
        "A 10,000-node botnet is hammering your server at 4 Gbps. "
        "You have 30 seconds before the host goes down. "
        "Deploy iptables rules to drop malicious SYN floods at the "
        "PREROUTING chain before they reach application space.\n\n"
        "Filtering at the netfilter kernel hook vs. an application-layer "
        "WAF — explain the stack depth difference. Why does one survive "
        "at 4 Gbps and the other cannot? Describe the data path from "
        "NIC interrupt to process table entry."
    ),
}


# ---------------------------------------------------------------------------
# Utility: Text Wrapper
# ---------------------------------------------------------------------------
def wrap_text(text: str, width: int) -> list[str]:
    """
    Wraps `text` to `width` columns.
    FIX: paragraph spacing previously used object-identity comparison
         (`line != mentor_visible_lines[-1]`), which silently broke when
         two identical strings existed in the list. Now uses enumerate()
         and index comparison, which is semantically correct.
    """
    paragraphs = text.split("\n")
    result: list[str] = []
    for p_idx, paragraph in enumerate(paragraphs):
        words       = paragraph.split(" ")
        current_line: list[str] = []
        current_len = 0
        for word in words:
            candidate_len = current_len + len(word) + (1 if current_line else 0)
            if current_line and candidate_len > width:
                result.append(" ".join(current_line))
                current_line = [word]
                current_len  = len(word)
            else:
                current_line.append(word)
                current_len += len(word) + (1 if len(current_line) > 1 else 0)
        if current_line:
            result.append(" ".join(current_line))
        # Insert blank separator line between paragraphs (not after the last one)
        if p_idx < len(paragraphs) - 1:
            result.append("")
    return result


# ---------------------------------------------------------------------------
# Color Initialization
# ---------------------------------------------------------------------------
def init_colors():
    curses.use_default_colors()
    curses.init_pair(COLOR_GREEN,     curses.COLOR_GREEN,  -1)
    curses.init_pair(COLOR_CYAN,      curses.COLOR_CYAN,   -1)
    curses.init_pair(COLOR_WARNING,   curses.COLOR_YELLOW, -1)
    curses.init_pair(COLOR_ALERT,     curses.COLOR_RED,    -1)
    curses.init_pair(COLOR_HIGHLIGHT, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(COLOR_DEFAULT,   curses.COLOR_WHITE,  -1)


# ---------------------------------------------------------------------------
# Command Processor
# ---------------------------------------------------------------------------
def process_command(cmd: str) -> bool:
    """
    Process a typed command.
    Returns False to signal a clean exit, True to continue the session.

    Cheat detection pipeline (layered):
      0. SoloEvaluationGate explanation branch — if gate is ARMED, score
         the submitted text as an explanation, not as a command.
      1. SocraticMentor.intercept_cheat()  — pattern-match layer
      2. RuleEnforcementEngine.evaluate_input() — secondary payload scan
      3. SoloEvaluationGate command classifier — arm gate on destructive cmds
      4. EBPFSecurityInterceptor.process_buffer() — credential masking
    """
    global warning_state

    cmd_clean = cmd.strip()
    if not cmd_clean:
        return True

    keystroke_analyzer.register_command()
    cmd_lower = cmd_clean.lower()

    # --- Layer 0: SOLO Explanation Gate — active branch ---
    # If the gate is ARMED, treat this submission as an explanation attempt.
    # The original command is NOT re-echoed to terminal_logs here.
    if solo_gate.active:
        solo_gate.attempts += 1
        result = solo_gate.evaluate_explanation(cmd_clean)

        if result["passed"]:
            terminal_logs.append(
                f"[SOLO-GATE] PASS ({result['hits']}/{result['required']} markers) "
                f"— command '{solo_gate.pending_cmd}' cleared."
            )
            cleared_cmd = solo_gate.pending_cmd
            solo_gate.reset()
            warning_state = False
            mentor_renderer.set_text(result["feedback"])
            # Forward the cleared command back through processing (now gate is IDLE)
            # Strip the echo that would double-log; add it here once.
            terminal_logs.append(f"academy-shell$ {cleared_cmd}")
            terminal_logs.append(f"[SYSTEM] Executing: {cleared_cmd}")
            
            # --- Curriculum Engine Progression ---
            prog_text = curriculum_engine.evaluate_command(cleared_cmd.lower())
            if prog_text:
                mentor_renderer.set_text(prog_text)
                
            return True

        elif solo_gate.attempts >= solo_gate.MAX_ATTEMPTS:
            terminal_logs.append(
                f"[SOLO-GATE] LOCKED — {solo_gate.MAX_ATTEMPTS} failed attempts. "
                "Gate reset. Retype the command to try again."
            )
            solo_gate.reset()
            warning_state = True
            mentor_renderer.set_text(
                "ank: [EXPLANATION GATE LOCKED]\n\n"
                "Three failed attempts. The gate resets.\n\n"
                "Retype the original command when you are ready to explain it properly. "
                "Structural understanding is not optional here."
            )
        else:
            warning_state = True
            terminal_logs.append(
                f"[SOLO-GATE] FAIL — attempt {solo_gate.attempts}/{solo_gate.MAX_ATTEMPTS}. "
                f"({result['hits']}/{result['required']} structural markers found)"
            )
            mentor_renderer.set_text(result["feedback"])
        return True

    # Gate is IDLE — normal command processing below.
    terminal_logs.append(f"academy-shell$ {cmd}")

    # --- Layer 1: SocraticMentor pattern intercept ---
    mentor_interception = mentor.intercept_cheat(cmd_lower)
    if mentor_interception:
        warning_state = True
        terminal_logs.append("[SECURITY] TRACE INTERCEPTED // SECURITY ALARM ACTIVATED")
        terminal_logs.append("[SECURITY] Forbidden signature detected by Socratic gate.")
        mentor_renderer.set_text(mentor_interception)
        return True

    # --- Layer 2: Rule Enforcement Engine ---
    result = rule_engine.evaluate_input(cmd_lower)
    if result["intercepted"]:
        warning_state = True
        terminal_logs.append("[SECURITY] TRACE INTERCEPTED // SECURITY ALARM ACTIVATED")
        terminal_logs.append("[SECURITY] Forbidden signature or bypass attempt blocked.")
        mentor_renderer.set_text(result["response"])
        return True

    # --- Layer 3: eBPF credential masking ---
    masked_cmd = ebpf_interceptor.process_buffer(cmd_lower)
    if ebpf_interceptor.echo_state == "BLIND":
        warning_state = True
        sanitized = presidio_scrubber.sanitize_logs(masked_cmd)
        terminal_logs.append(f"[SECURITY] eBPF MASKED: {masked_cmd}")
        terminal_logs.append(f"[SECURITY] Telemetry: {sanitized}")
        mentor_renderer.set_text(
            "ank: [EBPF SHIELD ACTIVE]\n\n"
            "eBPF uprobe attached to libc.so.6 (tcsetattr handler) intercepted raw buffer.\n\n"
            "Plain-text logs scrubbed via local Microsoft Presidio sidecar policy."
        )
        return True

    # --- Layer 3: SOLO Evaluation Gate — arm on destructive commands ---
    category = solo_gate.classify_command(cmd_lower)
    if category:
        solo_gate.active      = True
        solo_gate.pending_cmd = cmd_clean
        solo_gate.category    = category
        solo_gate.attempts    = 0
        warning_state         = True
        terminal_logs.append(
            f"[SOLO-GATE] ARMED — '{cmd_clean}' classified as [{category}]. "
            "Explain before execution."
        )
        mentor_renderer.set_text(solo_gate.gate_prompt())
        return True

    # --- Layer 4: eBPF credential masking ---
    masked_cmd = ebpf_interceptor.process_buffer(cmd_lower)
    if ebpf_interceptor.echo_state == "BLIND":
        warning_state = True
        sanitized = presidio_scrubber.sanitize_logs(masked_cmd)
        terminal_logs.append(f"[SECURITY] eBPF MASKED: {masked_cmd}")
        terminal_logs.append(f"[SECURITY] Telemetry: {sanitized}")
        mentor_renderer.set_text(
            "ank: [EBPF SHIELD ACTIVE]\n\n"
            "eBPF uprobe attached to libc.so.6 (tcsetattr handler) intercepted raw buffer.\n\n"
            "Plain-text logs scrubbed via local Microsoft Presidio sidecar policy."
        )
        return True

    # --- All clear ---
    warning_state = False

    if cmd_lower == "help":
        terminal_logs.append("[SYSTEM] Commands: 'help', 'status', 'clear', 'exit'")

    elif cmd_lower == "status":
        terminal_logs.append("[SYSTEM] NODE: ONLINE | ISOLATION: ACTIVE (gVisor)")
        starter = tier_matrix.tiers["socratic_starter"]
        pro     = tier_matrix.tiers["devops_professional"]
        terminal_logs.append(
            f"[SYSTEM] Starter Tier:     {starter['cpu_limit']} CPU / {starter['ram_limit']} RAM"
        )
        terminal_logs.append(
            f"[SYSTEM] DevOps Pro Tier:  {pro['cpu_limit']} CPU / {pro['ram_limit']} RAM"
        )
        # Surface keystroke telemetry (NEW)
        stats = keystroke_analyzer.session_stats()
        terminal_logs.append(
            f"[TELEMETRY] Session: {stats['chars_typed']} chars | "
            f"{stats['cmds_submitted']} cmds | "
            f"~{stats['approx_wpm']} WPM | "
            f"{stats['paste_blocks']} paste blocks"
        )
        mentor_renderer.set_text(
            "ank: System verified. Keystroke telemetry logged.\n\n"
            "Have you reviewed your bind mount isolation settings yet?"
        )

    elif cmd_lower == "clear":
        terminal_logs.clear()
        terminal_logs.append("[SYSTEM] Terminal log cleared.")

    elif cmd_lower == "exit":
        terminal_logs.append("[SYSTEM] Session terminating...")
        return False

    else:
        terminal_logs.append(f"[SYSTEM] Command '{cmd}' not found. Try 'help'.")

    # --- Curriculum Engine Progression ---
    prog_text = curriculum_engine.evaluate_command(cmd_lower)
    if prog_text:
        mentor_renderer.set_text(prog_text)

    return True


# ---------------------------------------------------------------------------
# Menu Selection Dispatcher
# ---------------------------------------------------------------------------
def trigger_menu_choice(idx: int) -> bool:
    """
    Handle a confirmed menu selection.
    Returns True if focus should snap back to COMMAND mode, False to stay in MENU.
    """
    global menu_state, menu_options, selected_menu_idx

    if menu_state == "MAIN":
        if idx == 0:
            menu_state        = "CURRICULUM"
            menu_options      = curriculum_engine.render_modules_list() + ["<- Back to Main Menu"]
            selected_menu_idx = 0
            mentor_renderer.set_text(curriculum_text)
            terminal_logs.append("[SYSTEM] Entering Curriculum selection menu.")
            return False   # stay in MENU to browse modules
        elif idx == 1:
            mentor_renderer.set_text(pricing_text)
            terminal_logs.append("[SYSTEM] Requesting Pricing telemetry logs...")
            return True
        elif idx == 2:
            mentor_renderer.set_text(docs_text)
            terminal_logs.append("[SYSTEM] Accessing System documentation database...")
            return True

    elif menu_state == "CURRICULUM":
        back_idx = len(menu_options) - 1
        if idx == back_idx:
            menu_state        = "MAIN"
            menu_options      = [
                "1. Course Curriculum",
                "2. Tariffs & Pricing",
                "3. System Docs",
            ]
            selected_menu_idx = 0
            mentor_renderer.set_text(
                "ank: Telemetry established. Navigate option panels or type commands in shell."
            )
            terminal_logs.append("[SYSTEM] Returning to Main Menu.")
            return False
        else:
            module_key = str(idx + 1)
            if module_key in module_texts:
                mentor_text = curriculum_engine.activate_module(module_key)
                mentor_renderer.set_text(mentor_text)
                terminal_logs.append(
                    f"[SYSTEM] Lab initialized: Module {module_key} - "
                    f"{curriculum_engine.modules[module_key]['title']}"
                )
                # Rebuild menu options to reflect potential IN_PROGRESS status
                menu_options = curriculum_engine.render_modules_list() + ["<- Back to Main Menu"]
            return True

    return True


# ---------------------------------------------------------------------------
# Main curses Entry Point
# ---------------------------------------------------------------------------
def main(stdscr):
    global focus_mode, selected_menu_idx, warning_state

    curses.curs_set(0)
    init_colors()
    stdscr.nodelay(True)
    stdscr.keypad(True)

    # Prime the mentor with the dynamic syllabus boot sequence
    mentor_renderer.set_text(
        curriculum_engine.build_boot_syllabus()
    )

    input_buffer: list[str] = []

    # ---------------------------------------------------------------------------
    # Window handles — created outside the draw loop and recreated only when
    # terminal dimensions change or KEY_RESIZE fires.
    # FIX: previously derwin() was called on every frame iteration, causing
    # flicker, memory churn, and crash risk during rapid resizes.
    # ---------------------------------------------------------------------------
    prev_h, prev_w = 0, 0
    win_work   = None
    win_ank    = None
    win_prompt = None

    def rebuild_windows(h: int, w: int):
        """Recalculate layout and (re)create all sub-windows."""
        nonlocal win_work, win_ank, win_prompt
        w_work   = int(w * 0.52)
        # FIX: cap ANK pane width so it never dominates ultra-wide terminals
        w_ank    = min(w - w_work - 4, 60)
        h_panes  = h - 5
        win_work   = stdscr.derwin(h_panes, w_work,  1,         2)
        win_ank    = stdscr.derwin(h_panes, w_ank,   1,         w_work + 3)
        win_prompt = stdscr.derwin(2,       w_work,  h - 3,     2)
        return w_work, w_ank, h_panes

    w_work = w_ank = h_panes = 0   # will be set on first rebuild

    while True:
        h, w = stdscr.getmaxyx()

        # --- Minimum size guard ---
        if h < 24 or w < 90:
            stdscr.clear()
            msg = "PLEASE RESIZE TERMINAL TO AT LEAST 90x24"
            # FIX: clamp x position so addstr never writes past right edge
            safe_x = max(0, min((w - len(msg)) // 2, w - len(msg) - 1))
            safe_y = h // 2
            if 0 <= safe_y < h and safe_x >= 0:
                stdscr.attron(curses.color_pair(COLOR_ALERT) | curses.A_BOLD)
                stdscr.addstr(safe_y, safe_x, msg[:w - 1])
                stdscr.attroff(curses.color_pair(COLOR_ALERT) | curses.A_BOLD)
            stdscr.refresh()
            time.sleep(0.05)
            try:
                ch = stdscr.getch()
            except curses.error:
                ch = -1
            if ch == ord("q"):
                break
            continue

        # --- Rebuild windows if dimensions changed ---
        if h != prev_h or w != prev_w:
            stdscr.clear()
            w_work, w_ank, h_panes = rebuild_windows(h, w)
            prev_h, prev_w = h, w

        # --- Advance mentor streaming animation ---
        mentor_renderer.tick()

        # --- Dynamic border color ---
        ank_border_color = COLOR_ALERT if warning_state else COLOR_CYAN

        # -----------------------------------------------------------------------
        # Render: Left Pane — Work Terminal
        # -----------------------------------------------------------------------
        win_work.erase()
        win_work.attron(curses.color_pair(COLOR_GREEN))
        win_work.box()
        win_work.attroff(curses.color_pair(COLOR_GREEN))

        win_work.attron(curses.color_pair(COLOR_GREEN) | curses.A_BOLD)
        win_work.addstr(0, 2, "[ WORK TERMINAL ]")
        win_work.attroff(curses.color_pair(COLOR_GREEN) | curses.A_BOLD)

        max_term_lines   = h_panes - 4
        visible_term_logs = (
            terminal_logs[-max_term_lines:]
            if len(terminal_logs) > max_term_lines
            else terminal_logs
        )
        for log_idx, log in enumerate(visible_term_logs):
            y_pos = 2 + log_idx
            if y_pos >= h_panes - 1:
                break
            if log.startswith("[SYSTEM]"):
                color = curses.color_pair(COLOR_GREEN)
            elif log.startswith("[SECURITY]"):
                color = curses.color_pair(COLOR_ALERT) | curses.A_BOLD
            elif log.startswith("[TELEMETRY]"):
                color = curses.color_pair(COLOR_WARNING)
            else:
                color = curses.color_pair(COLOR_DEFAULT)
            win_work.attron(color)
            win_work.addstr(y_pos, 2, log[:w_work - 4])
            win_work.attroff(color)

        # -----------------------------------------------------------------------
        # Render: Right Pane — ANK Monitor
        # -----------------------------------------------------------------------
        win_ank.erase()
        win_ank.attron(curses.color_pair(ank_border_color))
        win_ank.box()
        win_ank.attroff(curses.color_pair(ank_border_color))

        win_ank.attron(curses.color_pair(ank_border_color) | curses.A_BOLD)
        win_ank.addstr(0, 2, "[ ANK MONITOR ]")
        win_ank.attroff(curses.color_pair(ank_border_color) | curses.A_BOLD)

        # Reserve space at bottom of ANK pane for menu options
        options_count   = len(menu_options)
        options_start_y = h_panes - options_count - 2

        # Print streaming mentor dialogue
        y_cursor = 2
        visible_lines = mentor_renderer.visible_lines
        for line_idx, line in enumerate(visible_lines):
            wrapped = wrap_text(line, w_ank - 4)
            for w_line in wrapped:
                if y_cursor >= options_start_y - 3:
                    break
                win_ank.attron(curses.color_pair(ank_border_color))
                win_ank.addstr(y_cursor, 2, w_line[: w_ank - 4])
                win_ank.attroff(curses.color_pair(ank_border_color))
                y_cursor += 1
            else:
                # Add blank line between paragraphs (skip after last)
                # FIX: index-based comparison replaces broken identity check
                if line_idx < len(visible_lines) - 1:
                    y_cursor += 1
                continue
            break

        # Processing animation frame
        animation_y = options_start_y - 2
        if animation_y > y_cursor:
            frame_text  = animation_engine.get_next_frame()
            frame_color = COLOR_GREEN if not warning_state else COLOR_ALERT
            win_ank.attron(curses.color_pair(frame_color))
            win_ank.addstr(animation_y, 2, frame_text[: w_ank - 4])
            win_ank.attroff(curses.color_pair(frame_color))

        # System utilities header
        win_ank.attron(curses.color_pair(ank_border_color))
        win_ank.addstr(options_start_y, 2, "=== SYSTEM UTILITIES ===")
        win_ank.attroff(curses.color_pair(ank_border_color))

        # Menu options
        for opt_idx, option in enumerate(menu_options):
            y_opt = options_start_y + 1 + opt_idx
            if y_opt >= h_panes - 1:
                break
            if focus_mode == "MENU" and opt_idx == selected_menu_idx:
                win_ank.attron(curses.color_pair(COLOR_HIGHLIGHT))
                win_ank.addstr(y_opt, 2, f"[*] {option[:w_ank - 8]:<{w_ank - 8}} <<")
                win_ank.attroff(curses.color_pair(COLOR_HIGHLIGHT))
            else:
                win_ank.attron(curses.color_pair(COLOR_DEFAULT))
                win_ank.addstr(y_opt, 2, f"[ ] {option[:w_ank - 6]}")
                win_ank.attroff(curses.color_pair(COLOR_DEFAULT))

        # -----------------------------------------------------------------------
        # Render: Bottom — Input Prompt
        # -----------------------------------------------------------------------
        win_prompt.erase()
        prompt_prefix = "academy-shell$ "

        # Global status bar
        focus_help = f" [TAB] Focus Pane // ACTIVE PANE: {focus_mode} "
        bar_x      = max(1, (w - len(focus_help)) // 2)
        if bar_x + len(focus_help) < w:
            stdscr.attron(curses.color_pair(COLOR_GREEN))
            stdscr.addstr(h - 1, bar_x, focus_help)
            stdscr.attroff(curses.color_pair(COLOR_GREEN))

        if focus_mode == "COMMAND":
            curses.curs_set(1)
            win_prompt.attron(curses.color_pair(COLOR_GREEN) | curses.A_BOLD)
            win_prompt.addstr(0, 0, prompt_prefix)
            win_prompt.attroff(curses.color_pair(COLOR_GREEN) | curses.A_BOLD)

            input_str = "".join(input_buffer)
            win_prompt.attron(curses.color_pair(COLOR_DEFAULT))
            win_prompt.addstr(0, len(prompt_prefix), input_str[: w_work - len(prompt_prefix) - 2])
            win_prompt.attroff(curses.color_pair(COLOR_DEFAULT))

            # FIX: clamp cursor column so move() never throws curses.error
            cursor_col = min(
                len(prompt_prefix) + len(input_buffer),
                w_work - 2
            )
            try:
                win_prompt.move(0, cursor_col)
            except curses.error:
                pass
        else:
            curses.curs_set(0)
            win_prompt.attron(curses.color_pair(COLOR_DEFAULT))
            win_prompt.addstr(0, 0, "[NAVIGATING UTILITIES MENU - USE ARROWS / ENTER]")
            win_prompt.attroff(curses.color_pair(COLOR_DEFAULT))

        # Flush all panes
        stdscr.refresh()
        win_work.refresh()
        win_ank.refresh()
        win_prompt.refresh()

        # -----------------------------------------------------------------------
        # Input: Non-blocking keyboard poll
        # -----------------------------------------------------------------------
        try:
            ch = stdscr.getch()
        except curses.error:   # FIX: was bare `except Exception` — masked all crashes
            continue

        if ch == -1:
            time.sleep(0.01)
            continue

        # Terminal resize event
        if ch == curses.KEY_RESIZE:
            stdscr.clear()
            w_work, w_ank, h_panes = rebuild_windows(h, w)
            prev_h, prev_w = h, w
            continue

        # Tab: toggle focus pane
        if ch == 9:
            focus_mode = "MENU" if focus_mode == "COMMAND" else "COMMAND"
            continue

        # -----------------------------------------------------------------------
        # Command Mode Input
        # -----------------------------------------------------------------------
        if focus_mode == "COMMAND":
            now = time.time()

            if 32 <= ch <= 126:
                # Run through KeystrokeAnalyzer burst-window detector
                # FIX: replaced naive `time_delta < 0.008` single-delta check
                #      with burst-window analysis (>= 3 keys within 4 ms)
                if keystroke_analyzer.record_key(now):
                    curses.flushinp()
                    warning_state = True
                    terminal_logs.append("[SECURITY] TRACE INTERCEPTED // SECURITY ALARM ACTIVATED")
                    terminal_logs.append("[SECURITY] Paste detected! System requires manual typing.")
                    mentor_renderer.set_text(
                        "ank: [TRACE INTERCEPTED // SECURITY ALARM ACTIVATED]\n"
                        "SYS_ALARM: METACOGNITIVE BYPASS DETECTED.\n\n"
                        "Did you really try to copy-paste? Typing builds muscle memory, kid. "
                        "Use your hands, not your clipboard."
                    )
                    input_buffer.clear()
                    time.sleep(0.1)
                    continue

                max_len = w_work - len(prompt_prefix) - 5
                if len(input_buffer) < max_len:
                    input_buffer.append(chr(ch))

            elif ch in (curses.KEY_BACKSPACE, 127, 8):
                if input_buffer:
                    input_buffer.pop()

            elif ch in (10, 13, curses.KEY_ENTER):
                cmd = "".join(input_buffer)
                input_buffer.clear()
                if process_command(cmd) is False:
                    time.sleep(0.8)
                    break

        # -----------------------------------------------------------------------
        # Menu Mode Navigation
        # -----------------------------------------------------------------------
        elif focus_mode == "MENU":
            if ch == curses.KEY_UP:
                selected_menu_idx = (selected_menu_idx - 1) % len(menu_options)
            elif ch == curses.KEY_DOWN:
                selected_menu_idx = (selected_menu_idx + 1) % len(menu_options)
            elif ch in (10, 13, curses.KEY_ENTER):
                if trigger_menu_choice(selected_menu_idx):
                    focus_mode = "COMMAND"


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("\n[SYSTEM] Session terminated by user.")
        sys.exit(0)
