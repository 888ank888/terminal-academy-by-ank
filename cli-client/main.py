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
        self.modules = {
            "1": {"title": "Cyber Security: iptables Firewalls",          "status": "READY"},
            "2": {"title": "Local AI Infrastructure: ollama & Llama 3.2", "status": "MOCK_MODE"},
            "3": {"title": "IoT Automation: Headless Raspberry Pi Bash",   "status": "LOCKED"},
            "4": {"title": "Digital Forensics: Sherlock OSINT Pipelines",  "status": "LOCKED"},
            "5": {"title": "Cloud DevOps: Docker Compose & Nginx Matrix",  "status": "LOCKED"},
        }

    def render_modules_list(self) -> list:
        return [f"[{k}] {v['title']} ({v['status']})" for k, v in self.modules.items()]


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

module_texts = {
    "1": (
        "ank: [MODULE 1: CYBER SECURITY]\n\n"
        "Your task is to defend a server from a 10,000-node botnet. "
        "We will use iptables rules to drop malicious traffic at the packet level. "
        "How does filtering packets at the kernel level compare to application-level firewalling?"
    ),
    "2": (
        "ank: [MODULE 2: LOCAL AI INFRASTRUCTURE]\n\n"
        "You will deploy ollama locally with Llama 3.2 to write a log auditing scanner. "
        "When using an LLM to analyze system logs, how do you prevent hallucinated audit reports?"
    ),
    "3": (
        "ank: [MODULE 3: IOT AUTOMATION]\n\n"
        "Telemetry data from a remote headless Raspberry Pi sensor network must be safely "
        "collected over SSH. "
        "Why is public-key authentication preferred over passwords for automated script synchronization?"
    ),
    "4": (
        "ank: [MODULE 4: DIGITAL FORENSICS]\n\n"
        "Run sherlock pipelines to track usernames across social networks and filter findings "
        "using grep, awk, and sed. "
        "How do regex engines process large raw logs differently than normal search engines?"
    ),
    "5": (
        "ank: [MODULE 5: CLOUD DEVOPS]\n\n"
        "Build self-healing microservices behind an Nginx reverse proxy with Docker Compose. "
        "How does a bind mount configuration differ from a named volume in container data persistence?"
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
      1. SocraticMentor.intercept_cheat()  — pattern-match layer (FIX: now wired)
      2. RuleEnforcementEngine.evaluate_input() — secondary payload scan
      3. EBPFSecurityInterceptor.process_buffer() — credential masking
    """
    global warning_state

    cmd_clean = cmd.strip()
    if not cmd_clean:
        return True

    terminal_logs.append(f"academy-shell$ {cmd}")
    keystroke_analyzer.register_command()

    cmd_lower = cmd_clean.lower()

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
                mentor_renderer.set_text(module_texts[module_key])
                terminal_logs.append(
                    f"[SYSTEM] Inspecting Module {module_key}: "
                    f"{curriculum_engine.modules[module_key]['title']}"
                )
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

    # Prime the mentor with the welcome message
    mentor_renderer.set_text(
        "ank: Telemetry established. Navigate option panels or type commands in shell."
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
