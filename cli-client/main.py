import curses
import time
import sys

# Color Pair Constants
COLOR_DEFAULT = 1
COLOR_GREEN = 2
COLOR_CYAN = 3
COLOR_WARNING = 4
COLOR_ALERT = 5
COLOR_HIGHLIGHT = 6

# Dynamic state variables
focus_mode = "COMMAND"  # COMMAND or MENU
selected_menu_idx = 0
menu_state = "MAIN"  # MAIN or CURRICULUM
menu_options = [
    "1. Course Curriculum",
    "2. Tariffs & Pricing",
    "3. System Docs"
]

class AcademyCurriculumEngine:
    def __init__(self):
        self.modules = {
            "1": {"title": "Cyber Security: iptables Firewalls", "status": "READY"},
            "2": {"title": "Local AI Infrastructure: ollama & Llama 3.2", "status": "MOCK_MODE"},
            "3": {"title": "IoT Automation: Headless Raspberry Pi Bash", "status": "LOCKED"},
            "4": {"title": "Digital Forensics: Sherlock OSINT Pipelines", "status": "LOCKED"},
            "5": {"title": "Cloud DevOps: Docker Compose & Nginx Matrix", "status": "LOCKED"}
        }

    def render_modules_list(self) -> list:
        return [f"[{k}] {v['title']} ({v['status']})" for k, v in self.modules.items()]

curriculum_engine = AcademyCurriculumEngine()

class SocraticMentor:
    def __init__(self):
        self.name = "ank"
        self.tone = "sarcastic_architect"
        self.scan_lines = ["TRACE INTERCEPTED", "SYS_ALARM: METACOGNITIVE BYPASS DETECTED"]

    def intercept_cheat(self, user_input):
        """Detects if the student attempts to bypass productive struggle"""
        forbidden_patterns = ["password123", "bypass_gate", "--force-approve", "admin_bypass", "token_key"]
        for pattern in forbidden_patterns:
            if pattern in user_input:
                return f"[ank]: [TRACE INTERCEPTED // SECURITY ALARM ACTIVATED]\nSYS_ALARM: METACOGNITIVE BYPASS DETECTED.\n\nNice try, kid. You cannot script your way out of understanding. Try explaining the command honestly."
        return None

class TerminalAnimationEngine:
    def __init__(self):
        # Frame cycles for the node-radar/loading indicators
        self.loading_frames = [" [=---] ", " [-=--] ", " [--=-] ", " [---=] "]
        self.current_frame = 0
        self.last_tick = 0
        self.frame_delay = 0.15 # 150ms per frame
        self.cached_frame = "STATUS: PROCESSING  [=---] "

    def get_next_frame(self) -> str:
        current_time = time.time()
        if current_time - self.last_tick >= self.frame_delay:
            frame = self.loading_frames[self.current_frame]
            self.current_frame = (self.current_frame + 1) % len(self.loading_frames)
            self.cached_frame = f"STATUS: PROCESSING {frame}"
            self.last_tick = current_time
        return self.cached_frame

# Global mentor instance, warning state and animation engine
mentor = SocraticMentor()
warning_state = False
animation_engine = TerminalAnimationEngine()

# Text Streaming Engine variables
mentor_visible_lines = []
mentor_queue = ""
last_stream_tick = 0
stream_delay = 0.02  # 20ms per character typing speed

# Work terminal output logs
terminal_logs = [
    "[SYSTEM] Node local interface active.",
    "[SYSTEM] Type command or press [TAB] to toggle Menu navigation.",
    "[SYSTEM] Try typing 'status' or navigate to Curriculum on the right.",
    "----------------------------------------------------------------"
]

# Socratic dialogues for menu selections
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
        "Telemetry data from a remote headless Raspberry Pi sensor network must be safely collected over SSH. "
        "Why is public-key authentication preferred over passwords for automated script synchronization?"
    ),
    "4": (
        "ank: [MODULE 4: DIGITAL FORENSICS]\n\n"
        "Run sherlock pipelines to track usernames across social networks and filter findings using grep, awk, and sed. "
        "How do regex engines process large raw logs differently than normal search engines?"
    ),
    "5": (
        "ank: [MODULE 5: CLOUD DEVOPS]\n\n"
        "Build self-healing microservices behind an Nginx reverse proxy with Docker Compose. "
        "How does a bind mount configuration differ from a named volume in container data persistence?"
    )
}

def wrap_text(text, width):
    """Wraps text helper to fit terminal window width limits."""
    lines = []
    for paragraph in text.split('\n'):
        words = paragraph.split(' ')
        current_line = []
        current_len = 0
        for word in words:
            if current_len + len(word) + len(current_line) > width:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_len = len(word)
            else:
                current_line.append(word)
                current_len += len(word)
        if current_line:
            lines.append(" ".join(current_line))
    return lines

def set_mentor_text(text):
    global mentor_queue, mentor_visible_lines
    mentor_visible_lines = [""]
    mentor_queue = text

def init_colors():
    curses.use_default_colors()
    curses.init_pair(COLOR_GREEN, curses.COLOR_GREEN, -1)
    curses.init_pair(COLOR_CYAN, curses.COLOR_CYAN, -1)
    curses.init_pair(COLOR_WARNING, curses.COLOR_YELLOW, -1)
    curses.init_pair(COLOR_ALERT, curses.COLOR_RED, -1)
    curses.init_pair(COLOR_DEFAULT, curses.COLOR_WHITE, -1)
    # Highlight selection colors: black text on matrix green background
    curses.init_pair(COLOR_HIGHLIGHT, curses.COLOR_BLACK, curses.COLOR_GREEN)

def update_streamer():
    """Appends characters sequentially from queue to simulate typing."""
    global mentor_queue, mentor_visible_lines, last_stream_tick
    current_time = time.time()
    
    if mentor_queue and (current_time - last_stream_tick >= stream_delay):
        next_char = mentor_queue[0]
        mentor_queue = mentor_queue[1:]
        last_stream_tick = current_time
        
        if next_char == '\n':
            mentor_visible_lines.append("")
        else:
            mentor_visible_lines[-1] += next_char

def process_command(cmd):
    global warning_state
    cmd_clean = cmd.strip().lower()
    if not cmd_clean:
        return True

    terminal_logs.append(f"academy-shell$ {cmd}")
    
    # Check for cheat patterns using mentor instance
    cheat_reply = mentor.intercept_cheat(cmd_clean)
    if cheat_reply:
        warning_state = True
        terminal_logs.append("[SECURITY] TRACE INTERCEPTED // SECURITY ALARM ACTIVATED")
        terminal_logs.append("[SECURITY] Forbidden signature or bypass attempt blocked.")
        set_mentor_text(cheat_reply)
        return True
    
    warning_state = False

    if cmd_clean == "help":
        terminal_logs.append("[SYSTEM] Commands: 'help', 'status', 'clear', 'exit'")
    elif cmd_clean == "status":
        terminal_logs.append("[SYSTEM] NODE: ONLINE | ISOLATION: ACTIVE (gVisor)")
        set_mentor_text("ank: System is verified. Have you checked your bind mount settings?")
    elif cmd_clean == "clear":
        terminal_logs.clear()
        terminal_logs.append("[SYSTEM] Terminal log cleared.")
    elif cmd_clean == "exit":
        terminal_logs.append("[SYSTEM] Session terminating...")
        return False
    else:
        terminal_logs.append(f"[SYSTEM] Command '{cmd}' not found. Try 'help'.")
    
    return True

def trigger_menu_choice(idx):
    global menu_state, menu_options, selected_menu_idx
    if menu_state == "MAIN":
        if idx == 0:
            menu_state = "CURRICULUM"
            menu_options = curriculum_engine.render_modules_list() + ["<- Back to Main Menu"]
            selected_menu_idx = 0
            set_mentor_text(curriculum_text)
            terminal_logs.append("[SYSTEM] Entering Curriculum selection menu.")
            return False
        elif idx == 1:
            set_mentor_text(pricing_text)
            terminal_logs.append("[SYSTEM] Requesting Pricing telemetry logs...")
            return True
        elif idx == 2:
            set_mentor_text(docs_text)
            terminal_logs.append("[SYSTEM] Accessing System documentation database...")
            return True
    elif menu_state == "CURRICULUM":
        if idx == 5:  # Back to Main Menu
            menu_state = "MAIN"
            menu_options = [
                "1. Course Curriculum",
                "2. Tariffs & Pricing",
                "3. System Docs"
            ]
            selected_menu_idx = 0
            set_mentor_text("ank: Telemetry established. Navigate option panels or type commands in shell.")
            terminal_logs.append("[SYSTEM] Returning to Main Menu.")
            return False
        else:
            module_key = str(idx + 1)
            if module_key in module_texts:
                set_mentor_text(module_texts[module_key])
                terminal_logs.append(f"[SYSTEM] Inspecting Module {module_key}: {curriculum_engine.modules[module_key]['title']}")
            return True
    return True

def main(stdscr):
    global focus_mode, selected_menu_idx, warning_state
    curses.curs_set(0) # Hide cursor initially
    init_colors()
    
    stdscr.nodelay(True)
    stdscr.keypad(True)
    
    input_buffer = []
    last_key_time = 0
    
    # Initialize initial mentor prompt text streaming
    set_mentor_text("ank: Telemetry established. Navigate option panels or type commands in shell.")

    while True:
        h, w = stdscr.getmaxyx()
        
        # Sizing checks for layout safety
        if h < 24 or w < 90:
            stdscr.clear()
            stdscr.attron(curses.color_pair(COLOR_ALERT) | curses.A_BOLD)
            stdscr.addstr(h//2, max(1, (w - 38)//2), "PLEASE RESIZE TERMINAL TO AT LEAST 90x24")
            stdscr.attroff(curses.color_pair(COLOR_ALERT) | curses.A_BOLD)
            stdscr.refresh()
            time.sleep(0.1)
            ch = stdscr.getch()
            if ch == ord('q'):
                break
            continue

        # Layout Calculations
        w_work = int(w * 0.52)
        w_ank = w - w_work - 4
        h_panes = h - 5

        # Create Curses Sub-Windows dynamically
        # Work Terminal: y=1, x=2, h=h_panes, w=w_work
        win_work = stdscr.derwin(h_panes, w_work, 1, 2)
        # ANK Monitor: y=1, x=w_work + 3, h=h_panes, w=w_ank
        win_ank = stdscr.derwin(h_panes, w_ank, 1, w_work + 3)
        # Input prompt: y=h-3, x=2, h=2, w=w_work
        win_prompt = stdscr.derwin(2, w_work, h - 3, 2)

        # Update the Mentor character-by-character typing stream
        update_streamer()

        # Choose dynamic border color for ANK Monitor
        ank_border_color = COLOR_ALERT if warning_state else COLOR_CYAN

        # Render Left Pane (Work Terminal)
        win_work.erase()
        win_work.attron(curses.color_pair(COLOR_GREEN))
        win_work.box()
        win_work.attroff(curses.color_pair(COLOR_GREEN))
        
        win_work.attron(curses.color_pair(COLOR_GREEN) | curses.A_BOLD)
        win_work.addstr(0, 2, "[ WORK TERMINAL ]")
        win_work.attroff(curses.color_pair(COLOR_GREEN) | curses.A_BOLD)
        
        # Print visible terminal output logs
        max_term_lines = h_panes - 4
        visible_term_logs = terminal_logs[-max_term_lines:] if len(terminal_logs) > max_term_lines else terminal_logs
        for idx, log in enumerate(visible_term_logs):
            y_pos = 2 + idx
            if y_pos < h_panes - 1:
                color = curses.color_pair(COLOR_DEFAULT)
                if log.startswith("[SYSTEM]"):
                    color = curses.color_pair(COLOR_GREEN)
                elif log.startswith("[SECURITY]"):
                    color = curses.color_pair(COLOR_ALERT) | curses.A_BOLD
                elif log.startswith("academy-shell$"):
                    color = curses.color_pair(COLOR_DEFAULT)
                
                win_work.attron(color)
                win_work.addstr(y_pos, 2, log[:w_work - 4])
                win_work.attroff(color)

        # Render Right Pane (ANK Monitor)
        win_ank.erase()
        win_ank.attron(curses.color_pair(ank_border_color))
        win_ank.box()
        win_ank.attroff(curses.color_pair(ank_border_color))
        
        win_ank.attron(curses.color_pair(ank_border_color) | curses.A_BOLD)
        win_ank.addstr(0, 2, "[ ANK MONITOR ]")
        win_ank.attroff(curses.color_pair(ank_border_color) | curses.A_BOLD)

        # Render Selector Options (Fixed at the bottom of the ANK pane)
        options_count = len(menu_options)
        options_start_y = h_panes - options_count - 2

        # Print streaming mentor text
        y_cursor = 2
        for line in mentor_visible_lines:
            wrapped = wrap_text(line, w_ank - 4)
            for w_line in wrapped:
                if y_cursor < options_start_y - 3:
                    win_ank.attron(curses.color_pair(ank_border_color))
                    win_ank.addstr(y_cursor, 2, w_line)
                    win_ank.attroff(curses.color_pair(ank_border_color))
                    y_cursor += 1
            if line != mentor_visible_lines[-1]:
                y_cursor += 1

        # Render active animation frame
        animation_y = options_start_y - 2
        if animation_y > y_cursor:
            frame_text = animation_engine.get_next_frame()
            win_ank.attron(curses.color_pair(COLOR_GREEN if not warning_state else COLOR_ALERT))
            win_ank.addstr(animation_y, 2, frame_text[:w_ank-4])
            win_ank.attroff(curses.color_pair(COLOR_GREEN if not warning_state else COLOR_ALERT))

        win_ank.attron(curses.color_pair(ank_border_color))
        win_ank.addstr(options_start_y, 2, "=== SYSTEM UTILITIES ===")
        win_ank.attroff(curses.color_pair(ank_border_color))

        for idx, option in enumerate(menu_options):
            y_opt = options_start_y + 1 + idx
            if y_opt < h_panes - 1:
                if focus_mode == "MENU" and idx == selected_menu_idx:
                    # Highlight selected option with pointer
                    win_ank.attron(curses.color_pair(COLOR_HIGHLIGHT))
                    win_ank.addstr(y_opt, 2, f"[*] {option[:w_ank-8]:<{w_ank-8}} <<")
                    win_ank.attroff(curses.color_pair(COLOR_HIGHLIGHT))
                else:
                    win_ank.attron(curses.color_pair(COLOR_DEFAULT))
                    win_ank.addstr(y_opt, 2, f"[ ] {option[:w_ank-6]}")
                    win_ank.attroff(curses.color_pair(COLOR_DEFAULT))

        # Render Bottom Input Prompt Pane
        win_prompt.erase()
        prompt_prefix = "academy-shell$ "
        
        # Display focus indicators at the bottom line
        stdscr.attron(curses.color_pair(COLOR_GREEN))
        focus_help = f" [TAB] Focus Pane // ACTIVE PANE: {focus_mode} "
        stdscr.addstr(h - 1, max(1, (w - len(focus_help)) // 2), focus_help)
        stdscr.attroff(curses.color_pair(COLOR_GREEN))

        if focus_mode == "COMMAND":
            curses.curs_set(1)  # Show terminal cursor in command mode
            win_prompt.attron(curses.color_pair(COLOR_GREEN) | curses.A_BOLD)
            win_prompt.addstr(0, 0, prompt_prefix)
            win_prompt.attroff(curses.color_pair(COLOR_GREEN) | curses.A_BOLD)

            # Display currently typed input buffer
            input_str = "".join(input_buffer)
            win_prompt.attron(curses.color_pair(COLOR_DEFAULT))
            win_prompt.addstr(0, len(prompt_prefix), input_str[:w_work - len(prompt_prefix) - 2])
            win_prompt.attroff(curses.color_pair(COLOR_DEFAULT))
            
            # Position cursor in win_prompt relative coordinates
            win_prompt.move(0, len(prompt_prefix) + len(input_buffer))
        else:
            curses.curs_set(0)  # Hide cursor in menu mode
            win_prompt.attron(curses.color_pair(COLOR_DEFAULT))
            win_prompt.addstr(0, 0, "[NAVIGATING UTILITIES MENU - USE ARROWS / ENTER]")
            win_prompt.attroff(curses.color_pair(COLOR_DEFAULT))

        # Refresh sub-windows sequentially
        stdscr.refresh()
        win_work.refresh()
        win_ank.refresh()
        win_prompt.refresh()

        # Keyboard non-blocking poll
        try:
            ch = stdscr.getch()
        except Exception:
            continue

        if ch == -1:
            time.sleep(0.01)
            continue

        # Handle resize
        if ch == curses.KEY_RESIZE:
            stdscr.clear()
            continue

        # Focus Switching via Tab
        if ch == 9:  # Tab key ASCII value
            focus_mode = "MENU" if focus_mode == "COMMAND" else "COMMAND"
            continue

        # Input logic depending on focused sub-window
        if focus_mode == "COMMAND":
            current_key_time = time.time()
            
            if last_key_time > 0:
                time_delta = current_key_time - last_key_time
            else:
                time_delta = 1.0

            # Timing-based paste prevention
            if time_delta < 0.008 and ch not in (curses.KEY_RESIZE, -1):
                curses.flushinp()
                warning_state = True
                terminal_logs.append("[SECURITY] TRACE INTERCEPTED // SECURITY ALARM ACTIVATED")
                terminal_logs.append("[SECURITY] Paste detected! System requires manual typing.")
                set_mentor_text(
                    "ank: [TRACE INTERCEPTED // SECURITY ALARM ACTIVATED]\n"
                    "SYS_ALARM: METACOGNITIVE BYPASS DETECTED.\n\n"
                    "Did you really try to copy-paste? Typing builds muscle memory, kid. "
                    "Use your hands, not your clipboard."
                )
                input_buffer.clear()
                last_key_time = 0
                time.sleep(0.1)
                continue

            last_key_time = current_key_time

            # Backspace
            if ch in (curses.KEY_BACKSPACE, 127, 8):
                if input_buffer:
                    input_buffer.pop()
            
            # Enter command
            elif ch in (10, 13, curses.KEY_ENTER):
                cmd = "".join(input_buffer)
                input_buffer.clear()
                if process_command(cmd) is False:
                    time.sleep(0.8)
                    break
            
            # Keyboard character typing
            elif 32 <= ch <= 126:
                max_len = w_work - len(prompt_prefix) - 5
                if len(input_buffer) < max_len:
                    input_buffer.append(chr(ch))

        elif focus_mode == "MENU":
            # Menu Navigation
            if ch == curses.KEY_UP:
                selected_menu_idx = (selected_menu_idx - 1) % len(menu_options)
            elif ch == curses.KEY_DOWN:
                selected_menu_idx = (selected_menu_idx + 1) % len(menu_options)
            elif ch in (10, 13, curses.KEY_ENTER):
                if trigger_menu_choice(selected_menu_idx):
                    # Auto toggle focus back to command line for seamless Socratic reply
                    focus_mode = "COMMAND"

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("\n[SYSTEM] Session terminated by user.")
        sys.exit(0)
