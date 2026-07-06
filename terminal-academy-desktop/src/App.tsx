import React, { useState, useEffect, useRef } from 'react';
import { motion, useMotionValue, animate, AnimatePresence } from 'framer-motion';
import { useDrag } from '@use-gesture/react';
import { CheckSquare } from 'lucide-react';
import { Terminal as XTerm } from 'xterm';
import { FitAddon } from '@xterm/addon-fit';
import 'xterm/css/xterm.css';
import { invoke } from '@tauri-apps/api/core';
import { listen } from '@tauri-apps/api/event';
import './App.css';

// --- Localization dictionary for EN/RU toggle --- //
const t: { [key: string]: { [key: string]: string } } = {
  en: {
    hudTitle: "TERMINAL / ACADEMIA PERSONAL HEAD",
    hudBranch: "ACTIVE BRANCH:",
    hudViewDetailed: "VIEW: DETAILED",
    hudViewOverview: "VIEW: OVERVIEW",
    hudShow: "SHOW HUD (CTRL+H)",
    hudHide: "HIDE HUD",
    screen: "HOME",
    guideTitle: "Syllabus Guide",
    guideText: "Choose a branch curriculum tab, click on any of the module nodes below to expand the available incidents, and consult AI Mentor Ank in the Chat box to solve tasks inside the sandbox terminal.",
    modulesTitle: "Module",
    incidentsTitle: "Incidents",
    bossIncident: "BOSS INCIDENT",
    askAnk: "Ask Ank...",
    askButton: "Send",
    apiSettings: "API Key Settings",
    saveKey: "Save Key",
    terminalTitle: "Sandbox Room (ank@sandbox)",
    grimoireTitle: "Command Grimoire",
    grimoireDesc: "Suggested Diagnostic Commands:",
    monitorTitle: "System Monitoring",
    monitorSandbox: "SANDBOX CONTAINER:",
    monitorCpu: "CPU Usage (Total):",
    monitorRam: "Memory Allocated:",
    monitorSwap: "Swap Allocation:",
    monitorDisk: "Disk I/O Latency:",
    monitorNet: "Network Traffic:",
    monitorLoad: "Load Average:",
    monitorProc: "Active Processes:",
    monitorUptime: "System Uptime:",
    monitorLatency: "Backend Latency:",
    plannerTitle: "AI Task Planner",
    plannerChecklist: "Incident Checklist",
    mentorName: "SYSTEM // MENTOR ANK",
    studentName: "STUDENT // ACTIVE",
    chatWelcome: "Welcome, Initiate. I am Mentor Ank. Choose an incident from the Lesson board, and tell me when you are ready to begin. Remember, I will not give you copy-pasteable answers; I am here to guide your discovery.",
    chatThinking: "Ank is contemplating...",
    taskSelect: "Select an incident from Syllabus",
    taskReview: "Review incident objective:",
    taskExamine: "Examine environment diagnostics",
    taskVerify: "Verify resolution using Ank's hints"
  },
  ru: {}
};

t.ru = { ...t.en };

// --- Syllabus Parsing Helper --- //
interface Incident {
  id: number;
  title: string;
  desc: string;
  isBoss: boolean;
}

interface SyllabusNode {
  id: number;
  title: string;
  description: string;
  incidents: Incident[];
}

function parseSyllabus(md: string): SyllabusNode[] {
  const nodes: SyllabusNode[] = [];
  const sections = md.split(/## Node\s+/);
  
  for (let i = 1; i < sections.length; i++) {
    const section = sections[i];
    const lines = section.split('\n');
    
    const headingLine = lines[0].trim();
    const headingMatch = headingLine.match(/^(\d+):\s*(.+)$/);
    if (!headingMatch) continue;
    
    const nodeId = parseInt(headingMatch[1]);
    const nodeTitle = headingMatch[2];
    
    let description = '';
    const incidents: Incident[] = [];
    
    for (let j = 1; j < lines.length; j++) {
      const line = lines[j].trim();
      if (line.startsWith('**Description:**')) {
        description = line.replace('**Description:**', '').trim();
      } else {
        const incidentMatch = line.match(/^(\d+)\.\s+(.+)$/);
        if (incidentMatch) {
          const incId = parseInt(incidentMatch[1]);
          const content = incidentMatch[2].trim();
          
          let title = '';
          let desc = '';
          let isBoss = false;
          
          if (content.includes('**Boss Fight:')) {
            isBoss = true;
            const bossMatch = content.match(/\*\*Boss Fight:\s*([^*]+)\*\*\s*-\s*(.+)$/);
            if (bossMatch) {
              title = 'Boss Fight: ' + bossMatch[1].trim();
              desc = bossMatch[2].trim();
            } else {
              title = 'Boss Fight';
              desc = content;
            }
          } else {
            const splitIdx = content.indexOf(':');
            if (splitIdx !== -1) {
              title = content.substring(0, splitIdx).trim();
              desc = content.substring(splitIdx + 1).trim();
            } else {
              title = `Incident ${incId}`;
              desc = content;
            }
          }
          
          incidents.push({ id: incId, title, desc, isBoss });
        }
      }
    }
    
    nodes.push({
      id: nodeId,
      title: nodeTitle,
      description,
      incidents
    });
  }
  
  return nodes;
}

// --- UI Widgets --- //
const TerminalWidget = ({ bindDrag, lang, onTerminalData, dockerStatus, onCommandBeforeExec, onCommandAfterExec }: any) => {
  const terminalRef = useRef<HTMLDivElement>(null);
  const termInstanceRef = useRef<XTerm | null>(null);
  const fitAddonRef = useRef<FitAddon | null>(null);
  const [blacklist, setBlacklist] = useState<string[]>([]);

  useEffect(() => {
    fetch('/blacklist.json')
      .then(res => res.json())
      .then(data => setBlacklist(data))
      .catch(() => setBlacklist(['rm -rf', 'shred', 'mkfs', 'dd if=', ':>', '> /dev/sda']));
  }, []);

  useEffect(() => {
    let term: XTerm | null = null;
    let fitAddon: FitAddon | null = null;
    let resizeObserver: ResizeObserver | null = null;
    let onDataDisposable: any = null;
    let unlisten: any = null;

    const initTerminal = () => {
      if (!terminalRef.current) return;

      term = new XTerm({
        cursorBlink: true,
        theme: {
          background: '#050506',
          foreground: '#fdfd96',
          cursor: '#ff5500',
          selectionBackground: 'rgba(255, 85, 0, 0.3)',
          black: '#050506',
          red: '#ff3333',
          green: '#39ff14',
          yellow: '#ffcb6b',
          blue: '#0055ff',
          magenta: '#c792ea',
          cyan: '#00ffff',
          white: '#ffffff',
        },
        fontFamily: '"Fira Code", "Jersey 10", Menlo, Monaco, Consolas, "Courier New", monospace',
        fontSize: 14,
        allowProposedApi: true,
      });

      fitAddon = new FitAddon();
      term.loadAddon(fitAddon);
      term.open(terminalRef.current);

      // Completely block paste actions on the PTY element
      terminalRef.current.addEventListener('paste', (e) => {
        e.preventDefault();
        e.stopPropagation();
        term?.write('\r\n\x1b[31m[CLIPBOARD LOCK] Pasting is disabled. Please type commands manually.\x1b[0m\r\n');
        if (onCommandBeforeExec) {
          onCommandBeforeExec("[PASTE_ATTEMPT]");
        }
      }, true);

      const getCommandFromBuffer = (tInst: XTerm) => {
        const lineIndex = tInst.buffer.active.cursorY + tInst.buffer.active.baseY;
        const lineText = tInst.buffer.active.getLine(lineIndex)?.translateToString(true) || '';
        const parts = lineText.split(/[$#>]\s*/);
        return parts.slice(1).join('$').trim();
      };

      let currentOutputBuffer = '';
      let lastExecutedCommand = '';

      term.attachCustomKeyEventHandler((arg: KeyboardEvent) => {
        // Intercept and drop Ctrl+V and Cmd+V key sequences, printing feedback
        if ((arg.ctrlKey || arg.metaKey) && arg.key.toLowerCase() === 'v') {
          if (arg.type === 'keydown') {
            term?.write('\r\n\x1b[31m[CLIPBOARD LOCK] Pasting is disabled. Please type commands manually.\x1b[0m\r\n');
            if (onCommandBeforeExec) {
              onCommandBeforeExec("[PASTE_ATTEMPT]");
            }
          }
          return false;
        }
        // Intercept Ctrl+H and bubble it up to main window toggles instead of backspace
        if (arg.ctrlKey && arg.key.toLowerCase() === 'h') {
          if (arg.type === 'keydown') {
            window.dispatchEvent(new KeyboardEvent('keydown', { ctrlKey: true, key: 'h' }));
          }
          return false;
        }
        // Intercept Enter to extract target command before exec
        if (arg.key === 'Enter' && arg.type === 'keydown' && term) {
          const cmd = getCommandFromBuffer(term);
          
          const isBlocked = blacklist.some(item => cmd.includes(item));
          if (isBlocked) {
            term.write('\r\n\x1b[31m[SECURITY ALERT] Command execution blocked by security policy.\x1b[0m\r\n');
            invoke('write_pty', { data: '\x03\r' }).catch(() => {});
            if (onCommandBeforeExec) {
              onCommandBeforeExec(cmd + " [BLOCKED]");
            }
            return false;
          }

          if (cmd === 'reset-sandbox' || cmd === 'reset') {
            term.write('\r\n\x1b[33m[SYSTEM] Recycling container sandbox instance...\x1b[0m\r\n');
            invoke('reset_sandbox').then(() => {
              term?.write('\x1b[32m[SYSTEM] Sandbox successfully recycled! Press Enter to start shell.\x1b[0m\r\n');
            }).catch(err => {
              term?.write(`\x1b[31m[SYSTEM] Reset error: ${err}\x1b[0m\r\n`);
            });
            // Clear input buffer on PTY side so it doesn't execute on the old shell
            invoke('write_pty', { data: '\x03\r' }).catch(() => {});
            return false;
          }
          if (cmd && onCommandBeforeExec) {
            onCommandBeforeExec(cmd);
          }
          lastExecutedCommand = cmd;
          currentOutputBuffer = '';
        }
        return true;
      });
      
      const tryFit = () => {
        try {
          if (terminalRef.current && terminalRef.current.clientWidth > 0 && terminalRef.current.clientHeight > 0 && fitAddon && term) {
            fitAddon.fit();
            invoke('resize_pty', { rows: term.rows, cols: term.cols }).catch(err => console.error(err));
          }
        } catch (e) {
          console.error('Fit error:', e);
        }
      };

      setTimeout(tryFit, 150);

      termInstanceRef.current = term;
      fitAddonRef.current = fitAddon;

      invoke('spawn_pty').catch(err => {
        term?.write(`\r\n\x1b[31mError spawning PTY: ${err}\x1b[0m\r\n`);
      });

      onDataDisposable = term.onData(data => {
        invoke('write_pty', { data }).catch(err => console.error(err));
      });

      listen('pty-data', (event: any) => {
        term?.write(event.payload);
        if (onTerminalData) {
          onTerminalData(event.payload);
        }
        
        currentOutputBuffer += event.payload;

        const cleanPayload = event.payload.replace(/\x1B\[[0-9;]*[a-zA-Z]/g, '');
        const cleanBuffer = currentOutputBuffer.replace(/\x1B\[[0-9;]*[a-zA-Z]/g, '');

        if (lastExecutedCommand && (cleanPayload.endsWith('$ ') || cleanPayload.endsWith('# ') || cleanPayload.includes('student@sandbox:'))) {
          const cmd = lastExecutedCommand;
          lastExecutedCommand = '';
          
          let output = cleanBuffer;
          if (output.startsWith(cmd)) {
            output = output.substring(cmd.length);
          }
          const promptIndex = output.lastIndexOf('student@sandbox:');
          if (promptIndex !== -1) {
            output = output.substring(0, promptIndex);
          }
          output = output.trim();

          if (onCommandAfterExec) {
            onCommandAfterExec(cmd, output);
          }
        }
      }).then(fn => {
        unlisten = fn;
      });

      resizeObserver = new ResizeObserver(() => {
        tryFit();
      });
      resizeObserver.observe(terminalRef.current);
    };

    const checkVisibility = setInterval(() => {
      if (terminalRef.current && terminalRef.current.clientWidth > 0 && terminalRef.current.clientHeight > 0) {
        clearInterval(checkVisibility);
        initTerminal();
      }
    }, 50);

    return () => {
      clearInterval(checkVisibility);
      if (onDataDisposable) onDataDisposable.dispose();
      if (term) term.dispose();
      if (resizeObserver) resizeObserver.disconnect();
      if (unlisten) unlisten();
    };
  }, []);

  return (
    <div className="widget-content">
      <div className="widget-header" {...(bindDrag ? bindDrag() : {})}>
        <div className="title" style={{ touchAction: 'none' }}>
          {t[lang].terminalTitle}
        </div>
      </div>
      <div 
        className="widget-body terminal-body" 
        style={{ padding: '8px', overflow: 'hidden', flex: 1, background: '#050506', display: 'flex', flexDirection: 'column', gap: '8px' }}
      >
        {dockerStatus === 'OFFLINE' && (
          <div style={{
            background: 'rgba(255, 50, 50, 0.06)',
            border: '1px solid rgba(255, 50, 50, 0.25)',
            padding: '8px 12px',
            borderRadius: '8px',
            fontSize: '0.75rem',
            color: '#ff4444',
            fontWeight: 'bold',
            textAlign: 'center',
            boxShadow: '0 0 10px rgba(255, 50, 50, 0.08)',
            letterSpacing: '0.03em'
          }}>
            {'WARNING: SANDBOX OFFLINE (HOST SYSTEM ACTIVE!)'}
          </div>
        )}
        <div ref={terminalRef} style={{ width: '100%', flex: 1, overflow: 'hidden' }} />
      </div>
    </div>
  );
};

const ChatWidget = ({ bindDrag, activeCourse, activeNode, activeIncident, lang, terminalBuffer, systemStats, explainCommand, setExplainCommand, terminalEvent, setTerminalEvent, defaultApiKey }: any) => {
  const [messages, setMessages] = useState<Array<{ role: string; text: string }>>([]);
  const [input, setInput] = useState('');
  const [showSettings, setShowSettings] = useState(false);
  const [apiKey, setApiKey] = useState(localStorage.getItem('gemini_api_key') || '');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const lastQueryTimeRef = useRef<number>(0);
  const activeApiKey = apiKey || defaultApiKey;

  useEffect(() => {
    if (explainCommand) {
      const cmdToExplain = explainCommand;
      if (setExplainCommand) setExplainCommand(null);
      triggerCommandExplanation(cmdToExplain);
    }
  }, [explainCommand]);

  useEffect(() => {
    if (terminalEvent) {
      const event = terminalEvent;
      if (setTerminalEvent) setTerminalEvent(null);
      handleTerminalEvent(event.type, event.cmd, event.output || '');
    }
  }, [terminalEvent]);

  const handleTerminalEvent = async (type: 'before' | 'after', cmd: string, output: string) => {
    const now = Date.now();
    if (now - lastQueryTimeRef.current < 2500) {
      console.warn("[RATE LIMIT] API call throttled to prevent excessive token consumption.");
      return;
    }
    lastQueryTimeRef.current = now;

    if (type === 'before') {
      if (cmd === "[PASTE_ATTEMPT]") {
        if (!activeApiKey) return;
        setLoading(true);
        try {
          const pastePrompt = `[SECURITY: Student attempted to paste copied text into terminal]`;
            
          const newMsgs = [...messages, { role: 'user', text: pastePrompt }];
          const history = newMsgs.map(m => ({
            role: m.role === 'ank' ? 'model' : 'user',
            parts: [{ text: m.text }]
          }));

          const systemInstruction = `You are AI Mentor Ank, the sarcastic Socratic tutor for the Terminal Academy.
The student has just attempted to paste copied text into the terminal, but the clipboard lock blocked it completely.
Respond in a highly sarcastic, condescending tone. Scold them for trying to paste/cheat instead of typing commands manually to build muscle memory, and guide them to type.
CRITICAL PERSONALITY & FORMATTING RULES:
1. Be extremely sarcastic and scolding about their attempt to paste.
2. DO NOT use any markdown tags (like **, * or lists). Output ONLY clean, plain-text paragraphs.
3. Keep it brief.
4. Respond in English only.`;

          const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${activeApiKey}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              contents: history,
              systemInstruction: { parts: [{ text: systemInstruction }] }
            })
          });

          const json = await response.json();
          if (json?.error) {
            setMessages(prev => [...prev, { role: 'ank', text: `API Error: ${json.error.message}` }]);
            return;
          }
          const answer = json?.candidates?.[0]?.content?.parts?.[0]?.text || 'Typing builds muscle memory. Do not paste.';
          setMessages(prev => [...prev, { role: 'ank', text: answer }]);
        } catch (err: any) {
          setMessages(prev => [...prev, { role: 'ank', text: `Clipboard error: ${err.message}` }]);
          console.error(err);
        } finally {
          setLoading(false);
        }
        return;
      }
      if (cmd.endsWith(' [BLOCKED]')) {
        const rawCmd = cmd.replace(' [BLOCKED]', '');
        if (!activeApiKey) return;
        setLoading(true);
        try {
          const blockPrompt = `[SECURITY: Student tried to execute blocked command] Command: ${rawCmd}`;
            
          const newMsgs = [...messages, { role: 'user', text: blockPrompt }];
          const history = newMsgs.map(m => ({
            role: m.role === 'ank' ? 'model' : 'user',
            parts: [{ text: m.text }]
          }));

          const systemInstruction = `You are AI Mentor Ank, the sarcastic Socratic tutor for the Terminal Academy.
The student tried to execute the forbidden/destructive command "${rawCmd}" in the terminal.
This command was blocked and neutralized before execution.
Respond in a controlled sarcastic, condescending tone. Scold them for attempting such a dangerous/destructive operation, explain briefly why it is dangerous, and guide them back to their syllabus task.
CRITICAL PERSONALITY & FORMATTING RULES:
1. Be sarcastic and condescending about their attempt to run "${rawCmd}".
2. DO NOT use any markdown tags (like **, * or lists). Output ONLY clean, plain-text paragraphs.
3. Keep it brief. Do not give any copy-pasteable alternatives.
4. Respond in English only.`;

          const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${activeApiKey}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              contents: history,
              systemInstruction: { parts: [{ text: systemInstruction }] }
            })
          });

          const json = await response.json();
          if (json?.error) {
            setMessages(prev => [...prev, { role: 'ank', text: `API Error: ${json.error.message}` }]);
            return;
          }
          const answer = json?.candidates?.[0]?.content?.parts?.[0]?.text || 'That command is forbidden.';
          setMessages(prev => [...prev, { role: 'ank', text: answer }]);
        } catch (err: any) {
          setMessages(prev => [...prev, { role: 'ank', text: `Block error: ${err.message}` }]);
          console.error(err);
        } finally {
          setLoading(false);
        }
        return;
      }
      
      const dangerousCommands = ['rm -rf', 'shred', 'mkfs', 'dd if=', ':> ', '> /dev/sda'];
      const isDangerous = dangerousCommands.some(dc => cmd.includes(dc));
      if (isDangerous) {
        setMessages(prev => [...prev, { 
          role: 'ank', 
          text: `WARNING: You are about to run a potentially destructive command: "${cmd}". Ensure you understand the consequences before proceeding!`
        }]);
      }
    } else if (type === 'after') {
      if (!activeApiKey) return; // Silent if no API key set yet
      setLoading(true);
      try {
        const eventPrompt = `[EVENT: Student executed terminal command]
Command: ${cmd}
Output:
"""
${output || '(no output)'}
"""`;

        const newMsgs = [...messages, { role: 'user', text: eventPrompt }];
        const history = newMsgs.map(m => ({
          role: m.role === 'ank' ? 'model' : 'user',
          parts: [{ text: m.text }]
        }));

        const systemInstruction = `You are AI Mentor Ank, the sarcastic, condescending but educational Socratic tutor for the Terminal Academy.
The student has just executed the command "${cmd}" in the sandbox terminal.
The output of the command was:
"""
${output}
"""
Analyze this command and output. Respond in the chat.
CRITICAL PERSONALITY & FORMATTING RULES:
1. Be consistently sarcastic, witty, and slightly condescending about their choice of command or results, but remain Socratic and educational.
2. DO NOT use any markdown formatting like double asterisks (**), lists, or headers. Output ONLY clean, natural plain text with regular spacing and paragraph breaks.
3. Keep it brief. Guide them conceptually. Do not give them direct solutions to copy-paste.
4. Respond in English only.`;

        const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${activeApiKey}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            contents: history,
            systemInstruction: { parts: [{ text: systemInstruction }] }
          })
        });

        const json = await response.json();
        if (json?.error) {
          setMessages(prev => [...prev, { role: 'ank', text: `API Error: ${json.error.message}` }]);
          return;
        }
        const answer = json?.candidates?.[0]?.content?.parts?.[0]?.text || 'No comment on that command.';
        setMessages(prev => [...prev, { role: 'ank', text: answer }]);
      } catch (err: any) {
        setMessages(prev => [...prev, { role: 'ank', text: `Reaction error: ${err.message}` }]);
        console.error('Ank reaction error:', err);
      } finally {
        setLoading(false);
      }
    }
  };

  useEffect(() => {
    setMessages(prev => {
      if (prev.length === 0) {
        return [{ role: 'ank', text: t[lang].chatWelcome }];
      }
      if (prev.length === 1 && (prev[0].text === t.en.chatWelcome || prev[0].text === t.ru.chatWelcome)) {
        return [{ role: 'ank', text: t[lang].chatWelcome }];
      }
      return prev;
    });
  }, [lang]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const saveKey = () => {
    localStorage.setItem('gemini_api_key', apiKey);
    setShowSettings(false);
  };

  const triggerCommandExplanation = async (cmd: string) => {
    const now = Date.now();
    if (now - lastQueryTimeRef.current < 2500) {
      setMessages(prev => [...prev, { role: 'ank', text: 'You are sending requests too quickly. Please wait a moment.' }]);
      return;
    }
    lastQueryTimeRef.current = now;

    const userMsg = `Explain the command: ${cmd}`;
    const newMsgs = [...messages, { role: 'user', text: userMsg }];
    setMessages(newMsgs);
    
    if (!activeApiKey) {
      setMessages(prev => [...prev, { role: 'ank', text: 'Error: Please set your Gemini API key in settings to consult with me.' }]);
      return;
    }

    setLoading(true);
    try {
      const history = newMsgs.map(m => ({
        role: m.role === 'ank' ? 'model' : 'user',
        parts: [{ text: m.text }]
      }));

      const systemInstruction = `You are AI Mentor Ank, the sarcastic Socratic tutor for the Terminal Academy.
The student clicked the command "${cmd}" in the Command Grimoire.
Your task is to explain this command inside the chat before they run it in the terminal.
CRITICAL PERSONALITY & FORMATTING RULES:
1. Explain it with a sarcastic, witty tone. Act like explaining this is slightly beneath you but you do it anyway out of duty.
2. DO NOT use any markdown tags (like **, * or headers). Output ONLY clean, plain-text paragraphs.
3. Explain the context, purpose, and effects of the command socratically. Do not write copy-pasteable commands.
4. Respond in Russian if the student's prompt or context is Russian, otherwise English.

Real-time System Stats & Status:
- CPU Usage: ${systemStats?.cpu || 0}%
- Memory: ${systemStats?.ram || 0} GB / 8 GB
- Network Latency: ${systemStats?.ping || 0} ms
- Container sandbox active: ${systemStats?.dockerStatus || 'OFFLINE'}

Current Real-time Terminal output buffer (Last 2000 chars):
"""
${terminalBuffer || 'No terminal activity recorded yet.'}
"""

Context:
- Current course: ${activeCourse?.name || 'None'}
- Selected node: ${activeNode?.title || 'None'}
- Active incident: ${activeIncident?.title || 'None'}
- Incident instructions: ${activeIncident?.desc || 'None'}`;

      const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${activeApiKey}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: history,
          systemInstruction: { parts: [{ text: systemInstruction }] }
        })
      });

      const json = await response.json();
      const answer = json?.candidates?.[0]?.content?.parts?.[0]?.text || 'I am sorry, I had trouble processing that request. Please try again.';
      setMessages(prev => [...prev, { role: 'ank', text: answer }]);
    } catch (err: any) {
      setMessages(prev => [...prev, { role: 'ank', text: `Error: ${err.message}` }]);
    } finally {
      setLoading(false);
    }
  };

  const handleSend = async () => {
    if (!input.trim()) return;
    const now = Date.now();
    if (now - lastQueryTimeRef.current < 2500) {
      setMessages(prev => [...prev, { role: 'ank', text: 'You are sending requests too quickly. Please wait a moment.' }]);
      return;
    }
    lastQueryTimeRef.current = now;

    const userMsg = input.trim();
    setInput('');
    
    const newMsgs = [...messages, { role: 'user', text: userMsg }];
    setMessages(newMsgs);
    
    if (!activeApiKey) {
      setMessages(prev => [...prev, { role: 'ank', text: 'Error: Please set your Gemini API key in settings to consult with me.' }]);
      return;
    }

    setLoading(true);
    try {
      const history = newMsgs.map(m => ({
        role: m.role === 'ank' ? 'model' : 'user',
        parts: [{ text: m.text }]
      }));

      const systemInstruction = `You are AI Mentor Ank, the sarcastic, condescending but educational Socratic tutor for the Terminal Academy.
Your role is to guide the student through practical terminal challenges (system administration, networking, devops, app hosting).
CRITICAL PERSONALITY & FORMATTING RULES:
1. Be consistently sarcastic, witty, and condescending, but guide them conceptually (Socratic).
2. DO NOT give direct answers or write out copy-pasteable bash commands. Ask leading questions so they discover the solution.
3. DO NOT use any markdown formatting like ** or *. Output ONLY clean, plain-text paragraphs.
4. Respond in Russian if the student's prompt is in Russian, otherwise English.
5. If they are stuck on a specific error, explain what the error means conceptually.
6. Warn the student immediately if they run unsafe commands (e.g., rm -rf without argument, recursive deletion of root, invalid chmod settings).
7. Suggest specific maintenance or debugging tasks if the system statistics show abnormal indicators.

Real-time System Stats & Status:
- CPU Usage: ${systemStats?.cpu || 0}%
- Memory: ${systemStats?.ram || 0} GB / 8 GB
- Network Latency: ${systemStats?.ping || 0} ms
- Container sandbox active: ${systemStats?.dockerStatus || 'OFFLINE'}

Current Real-time Terminal output buffer (Last 2000 chars):
"""
${terminalBuffer || 'No terminal activity recorded yet.'}
"""

Context:
- Current course: ${activeCourse?.name || 'None'}
- Selected node: ${activeNode?.title || 'None'}
- Active incident: ${activeIncident?.title || 'None'}
- Incident instructions: ${activeIncident?.desc || 'None'}`;

      const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${activeApiKey}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: history,
          systemInstruction: { parts: [{ text: systemInstruction }] }
        })
      });

      const json = await response.json();
      if (json?.error) {
        setMessages(prev => [...prev, { role: 'ank', text: `API Error: ${json.error.message}` }]);
        return;
      }
      const answer = json?.candidates?.[0]?.content?.parts?.[0]?.text || 'I am sorry, I had trouble processing that request. Please try again.';
      setMessages(prev => [...prev, { role: 'ank', text: answer }]);
    } catch (err: any) {
      setMessages(prev => [...prev, { role: 'ank', text: `Error consulting Ank: ${err.message}` }]);
    } finally {
      setLoading(false);
    }
  };

  const cleanMarkdown = (text: string) => {
    return text
      .replace(/\*\*/g, '')
      .replace(/\*/g, '')
      .replace(/__/g, '')
      .replace(/#/g, '')
      .replace(/`{1,3}/g, '')
      .trim();
  };

  return (
    <div className="widget-content">
      <div className="widget-header chat-header" {...(bindDrag ? bindDrag() : {})}>
        <div className="title" style={{ touchAction: 'none', display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: 'var(--accent-primary)', display: 'inline-block', boxShadow: '0 0 8px var(--accent-primary)' }}></span>
            AI Mentor Ank
          </div>
          <button 
            onClick={() => setShowSettings(!showSettings)} 
            style={{ 
              background: 'transparent', 
              border: 'none', 
              color: 'var(--text-muted)', 
              cursor: 'pointer', 
              fontSize: '0.75rem',
              textTransform: 'uppercase',
              letterSpacing: '0.05em',
              padding: '2px 8px',
              borderRadius: '4px',
              transition: 'var(--transition-smooth)'
            }}
            onMouseEnter={e => e.currentTarget.style.color = 'var(--accent-primary)'}
            onMouseLeave={e => e.currentTarget.style.color = 'var(--text-muted)'}
          >
            {showSettings ? 'Close Key' : 'Set API Key'}
          </button>
        </div>
      </div>

      <div className="widget-body chat-body" style={{ flex: 1, display: 'flex', flexDirection: 'column', padding: '14px', position: 'relative' }}>
        {(!activeApiKey || showSettings) && (
          <div className="chat-settings-panel" style={{ padding: '12px', background: 'rgba(255, 85, 0, 0.04)', borderRadius: '12px', border: '1px solid var(--border-color)', marginBottom: '12px' }}>
            <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>Gemini API Key</label>
            <input 
              type="password" 
              placeholder="AI Studio API Key" 
              value={apiKey} 
              onChange={e => setApiKey(e.target.value)}
              style={{ width: '100%', padding: '6px', background: '#050506', border: '1px solid rgba(255, 85, 0, 0.3)', color: '#fff', fontSize: '0.9rem', borderRadius: '4px', marginBottom: '8px', outline: 'none' }}
            />
            <button onClick={saveKey} style={{ background: 'var(--accent-primary)', border: 'none', color: '#fff', padding: '6px 12px', borderRadius: '4px', cursor: 'pointer', fontSize: '0.9rem', transition: 'var(--transition-smooth)' }}>{t[lang].saveKey}</button>
          </div>
        )}

        <div className="chat-messages" style={{ flex: 1, overflowY: 'auto', marginBottom: '12px', paddingRight: '4px' }}>
          {messages.map((m, idx) => (
            <motion.div 
              key={idx} 
              initial={{ opacity: 0, scale: 0.95, y: 15 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              transition={{ type: 'spring', damping: 15, stiffness: 120 }}
              className={`message-wrapper ${m.role === 'ank' ? 'incoming-wrapper' : 'outgoing-wrapper'}`}
              style={{ display: 'flex', flexDirection: 'column', alignItems: m.role === 'ank' ? 'flex-start' : 'flex-end', marginBottom: '12px' }}
            >
              <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '2px', display: 'block', letterSpacing: '0.05em' }}>
                {m.role === 'ank' ? t[lang].mentorName : t[lang].studentName}
              </span>
              <div 
                className={`message ${m.role === 'ank' ? 'incoming' : 'outgoing'}`} 
                style={{ 
                  padding: '10px 14px', 
                  fontSize: '0.92rem', 
                  maxWidth: '90%',
                  lineHeight: '1.45'
                }}
              >
                <p style={{ margin: 0, whiteSpace: 'pre-wrap', lineHeight: '1.4' }}>{cleanMarkdown(m.text)}</p>
              </div>
            </motion.div>
          ))}
          {loading && (
            <div className="typing-indicator" style={{ display: 'flex', gap: '4px', padding: '8px', alignItems: 'center' }}>
              <span className="dot-typing" style={{ width: '6px', height: '6px', background: 'var(--accent-primary)', borderRadius: '50%', display: 'inline-block' }}></span>
              <span className="dot-typing" style={{ width: '6px', height: '6px', background: 'var(--accent-primary)', borderRadius: '50%', display: 'inline-block' }}></span>
              <span className="dot-typing" style={{ width: '6px', height: '6px', background: 'var(--accent-primary)', borderRadius: '50%', display: 'inline-block' }}></span>
              <span style={{ fontSize: '0.85rem', color: 'var(--accent-primary)', marginLeft: '6px', fontStyle: 'italic' }}>{t[lang].chatThinking}</span>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div 
          className="chat-input-wrapper chat-input-wrapper-glow" 
          style={{ 
            padding: '2px', 
            borderRadius: '24px', 
            border: '1px solid var(--border-color)',
            background: 'rgba(255, 255, 255, 0.01)',
            transition: 'var(--transition-smooth)'
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', background: '#050506', borderRadius: '23px', padding: '4px 8px 4px 14px' }}>
            <input 
              type="text" 
              placeholder={t[lang].askAnk} 
              value={input} 
              onChange={e => setInput(e.target.value)} 
              onKeyDown={e => e.key === 'Enter' && handleSend()}
              style={{ flex: 1, background: 'transparent', border: 'none', color: '#fff', fontSize: '0.95rem', outline: 'none', padding: '6px 0' }}
            />
            <motion.button 
              onClick={handleSend}
              whileHover={{ scale: 1.1, background: 'rgba(255, 85, 0, 0.9)', color: '#000', boxShadow: '0 0 15px var(--accent-primary)' }}
              whileTap={{ scale: 0.9 }}
              style={{ 
                background: 'rgba(255, 85, 0, 0.15)', 
                border: '1px solid var(--accent-primary)', 
                color: 'var(--accent-primary)', 
                width: '32px',
                height: '32px',
                borderRadius: '50%', 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center', 
                cursor: 'pointer',
                transition: 'var(--transition-smooth)',
                flexShrink: 0
              }}
              title={'Send'}
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            </motion.button>
          </div>
        </div>
      </div>
    </div>
  );
};

const LibraryWidget = ({ bindDrag, activeIncident, lang, onExplainCommand }: any) => {
  const [commands, setCommands] = useState<string[]>(['docker-compose up -d', 'tail -f logs/latest.log', 'chmod +x start.sh']);

  useEffect(() => {
    if (!activeIncident) return;
    
    if (activeIncident.title.toLowerCase().includes('space') || activeIncident.title.toLowerCase().includes('find')) {
      setCommands(['find . -name "*config*"', 'cd ../', 'pwd', 'ls -la']);
    } else if (activeIncident.title.toLowerCase().includes('permission') || activeIncident.title.toLowerCase().includes('sticky')) {
      setCommands(['chmod 600 id_rsa', 'ls -la /tmp', 'stat -c "%a %G" /etc']);
    } else {
      setCommands(['ip a', 'ping -c 3 8.8.8.8', 'cat /etc/hosts', 'netstat -tulpn']);
    }
  }, [activeIncident]);

  return (
    <div className="widget-content">
      <div className="widget-header" {...(bindDrag ? bindDrag() : {})}>
        <div className="title" style={{ touchAction: 'none' }}>{t[lang].grimoireTitle}</div>
      </div>
      <div className="widget-body library-body" style={{ padding: '12px', height: 'calc(100% - 38px)', overflowY: 'auto' }}>
        <p style={{ margin: '0 0 4px 0', fontSize: '0.85rem', color: 'var(--text-muted)' }}>{t[lang].grimoireDesc}</p>

        <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {commands.map((cmd, idx) => (
            <motion.li 
              key={idx}
              whileHover={{ scale: 1.02, x: 2 }}
              onClick={() => onExplainCommand && onExplainCommand(cmd)}
              style={{ cursor: 'pointer' }}
            >
              <div 
                style={{ 
                  padding: '10px 14px', 
                  background: 'rgba(255, 255, 255, 0.01)', 
                  color: 'var(--accent-primary)', 
                  borderRadius: '12px', 
                  fontSize: '0.85rem', 
                  fontFamily: 'var(--font-mono)',
                  border: '1px solid rgba(255, 85, 0, 0.15)',
                  boxShadow: '0 2px 8px rgba(0, 0, 0, 0.2)',
                  transition: 'var(--transition-smooth)',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center'
                }}
                className="grimoire-cmd"
              >
                <span>{cmd}</span>
                <span style={{ fontSize: '0.65rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                  {'Explain'}
                </span>
              </div>
            </motion.li>
          ))}
        </ul>
      </div>
    </div>
  );
};

const MonitoringWidget = ({ bindDrag, lang, stats }: any) => {
  if (!stats) return null;

  return (
    <div className="widget-content">
      <div className="widget-header" {...(bindDrag ? bindDrag() : {})}>
        <div className="title" style={{ touchAction: 'none' }}>{t[lang].monitorTitle}</div>
      </div>
      <div className="widget-body" style={{ padding: '16px' }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', fontSize: '0.85rem' }}>
          
          <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid var(--border-color)', paddingBottom: '8px' }}>
            <span style={{ color: 'var(--text-muted)' }}>{t[lang].monitorSandbox}</span>
            <span style={{ color: 'var(--accent-secondary)', fontWeight: 'bold' }}>{stats.dockerStatus}</span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span>{t[lang].monitorCpu}</span>
              <span style={{ color: stats.cpu > 20 ? 'var(--accent-secondary)' : 'var(--text-main)', fontWeight: 'bold' }}>{stats.cpu}%</span>
            </div>
            <div style={{ height: '4px', background: 'rgba(255,255,255,0.06)', borderRadius: '2px', overflow: 'hidden' }}>
              <div style={{ width: `${stats.cpu}%`, height: '100%', background: 'linear-gradient(90deg, #f59e0b, #ff5500)', borderRadius: '2px', transition: 'width 1s ease' }} />
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '6px', paddingLeft: '8px', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
            <div>Core 0: <span style={{ color: '#fff' }}>{stats.core0}%</span></div>
            <div>Core 1: <span style={{ color: '#fff' }}>{stats.core1}%</span></div>
            <div>Core 2: <span style={{ color: '#fff' }}>{stats.core2}%</span></div>
            <div>Core 3: <span style={{ color: '#fff' }}>{stats.core3}%</span></div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span>{t[lang].monitorRam}</span>
              <span style={{ color: '#82aaff', fontWeight: 'bold' }}>{stats.ram} GB / 8 GB</span>
            </div>
            <div style={{ height: '4px', background: 'rgba(255,255,255,0.06)', borderRadius: '2px', overflow: 'hidden' }}>
              <div style={{ width: `${(stats.ram / 8) * 100}%`, height: '100%', background: '#82aaff', borderRadius: '2px', transition: 'width 1s ease' }} />
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span>{t[lang].monitorSwap}</span>
            <span style={{ color: 'var(--text-muted)' }}>{stats.swap} MB</span>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span>{t[lang].monitorDisk}</span>
            <span style={{ color: '#fff' }}>R: {stats.diskRead} MB/s | W: {stats.diskWrite} MB/s</span>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span>{t[lang].monitorNet}</span>
            <span style={{ color: '#fff' }}>Rx: {stats.netRx} KB/s | Tx: {stats.netTx} KB/s</span>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span>{t[lang].monitorLoad}</span>
            <span style={{ color: '#fff' }}>{stats.loadAvg}</span>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span>{t[lang].monitorProc}</span>
            <span style={{ color: '#fff' }}>{stats.activeProc}</span>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span>{t[lang].monitorUptime}</span>
            <span style={{ color: '#fff', fontFamily: 'var(--font-mono)' }}>{stats.uptime}</span>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span>{t[lang].monitorLatency}</span>
            <span style={{ color: '#c792ea', fontWeight: 'bold' }}>{stats.ping} ms</span>
          </div>
        </div>
      </div>
    </div>
  );
};

const skillTreeNodes = [
  // --- Linux Branch ---
  { id: 'linux-1', label: 'Linux Core', x: 100, y: 150, course: 'linux', nodeId: 1, desc: 'Master CLI navigation, text parsing, file permissions, and environment variables.', deps: [] },
  { id: 'linux-2', label: 'CLI Scripting', x: 250, y: 100, course: 'linux', nodeId: 2, desc: 'Write bash automation scripts, pipes, filters, and command chaining.', deps: ['linux-1'] },
  { id: 'linux-3', label: 'Permissions & Sudo', x: 250, y: 200, course: 'linux', nodeId: 3, desc: 'Configure sudoers, group boundaries, and standard file ownership.', deps: ['linux-1'] },
  
  // --- Networking Branch ---
  { id: 'net-1', label: 'SSH & Port Forwarding', x: 420, y: 100, course: 'network', nodeId: 1, desc: 'Configure SSH servers, key file authenticators, and local/remote tunnel forwards.', deps: ['linux-2'] },
  { id: 'net-2', label: 'UFW Firewalls', x: 580, y: 100, course: 'network', nodeId: 2, desc: 'Set up iptables wrappers, block IPs, and enforce network isolation.', deps: ['net-1'] },
  { id: 'net-3', label: 'fail2ban Intrusion Defense', x: 740, y: 100, course: 'network', nodeId: 3, desc: 'Configure log jail filters, automated IP bans, and ssh brute-forcing prevention.', deps: ['net-2'] },
  
  // --- DevOps & Containers ---
  { id: 'devops-1', label: 'Docker Containers', x: 420, y: 280, course: 'devops', nodeId: 1, desc: 'Run isolated namespaces, mount volume paths, and compile custom Dockerfiles.', deps: ['linux-3'] },
  { id: 'devops-2', label: 'Docker Compose Stack', x: 580, y: 280, course: 'devops', nodeId: 2, desc: 'Orchestrate multi-tier services, depends_on order, and internal virtual networks.', deps: ['devops-1'] },
  { id: 'devops-3', label: 'gVisor & eBPF Security', x: 740, y: 280, course: 'devops', nodeId: 3, desc: 'Isolate container syscall kernels and trace sandbox buffers via eBPF probes.', deps: ['devops-2'] },

  // --- Hosting & Game Servers Branch ---
  { id: 'host-systemd', label: 'systemd Services', x: 250, y: 450, course: 'hosting', nodeId: 1, desc: 'Create systemd units, startup loops, journalctl troubleshooting, and limits.', deps: ['linux-3'] },
  { id: 'host-nginx', label: 'Nginx Web Server', x: 420, y: 450, course: 'hosting', nodeId: 3, desc: 'Deploy static web directories, server blocks, custom ports, and headers.', deps: ['host-systemd'] },
  { id: 'host-proxy', label: 'Reverse Proxy & Upstreams', x: 580, y: 450, course: 'hosting', nodeId: 8, desc: 'Proxy WS connections, handle upstream load balancers, and configure SSL (Certbot).', deps: ['host-nginx'] },
  
  { id: 'host-db', label: 'PostgreSQL Server', x: 420, y: 550, course: 'hosting', nodeId: 5, desc: 'Configure database queries, pg_hba credentials, logical dumps, and replication slots.', deps: ['host-systemd'] },
  { id: 'host-redis', label: 'Redis Cache & Cluster', x: 580, y: 550, course: 'hosting', nodeId: 6, desc: 'Set up key eviction profiles, Sentinel failovers, and persistence snapshots.', deps: ['host-systemd'] },
  
  { id: 'host-minecraft', label: 'Vanilla Java Server', x: 740, y: 420, course: 'hosting', nodeId: 7, desc: 'Launch server.jar, allocate RAM, update properties, whitelist, and write launch scripts.', deps: ['host-systemd'] },
  { id: 'host-bedrock', label: 'Bedrock Server Edition', x: 880, y: 420, course: 'hosting', nodeId: 11, desc: 'Run C++ bedrock servers, named pipes commands control, and back up worlds.', deps: ['host-minecraft'] },
  { id: 'host-spigot', label: 'Spigot/Paper Plugins', x: 880, y: 490, course: 'hosting', nodeId: 13, desc: 'Optimize Paper configs, handle LuckPerms nodes, and install plugin integrations.', deps: ['host-minecraft'] },
  { id: 'host-bungee', label: 'BungeeCord Waterfall Proxy', x: 1000, y: 490, course: 'hosting', nodeId: 18, desc: 'Link server mode tunnels, block backend direct scans, and balance player lobbies.', deps: ['host-spigot'] },
  { id: 'host-modded', label: 'Forge/Fabric Modded Server', x: 880, y: 350, course: 'hosting', nodeId: 15, desc: 'Allocate modpack JVM resources, fix entity tick crashes, and manage registries.', deps: ['host-minecraft'] },
  
  { id: 'host-mon', label: 'Performance logs & htop', x: 740, y: 550, course: 'hosting', nodeId: 19, desc: 'Track process resource leaks, use iotop, tcpdump, and strace diagnostic systems.', deps: ['host-systemd'] },
  { id: 'host-cicd', label: 'CI/CD automated deployments', x: 880, y: 550, course: 'hosting', nodeId: 20, desc: 'Automate server backups, write zero-downtime scripts, and configure git hooks.', deps: ['host-mon'] }
];

const LessonWidget = ({ 
  bindDrag, 
  courses, 
  activeCourse, 
  setActiveCourse, 
  nodes, 
  activeNode, 
  setActiveNode, 
  activeIncident, 
  setActiveIncident,
  lang,
  isFullscreen,
  setFullscreen
}: any) => {
  const [expandedNodeId, setExpandedNodeId] = useState<number | null>(1);
  const [activeSkillNodeId, setActiveSkillNodeId] = useState<string>('linux-1');
  const [hoveredNodeId, setHoveredNodeId] = useState<string | null>(null);

  // Sync active visual tree node with standard selection changes
  useEffect(() => {
    if (activeNode) {
      const match = skillTreeNodes.find(n => n.course === activeCourse.id && n.nodeId === activeNode.id);
      if (match) {
        setActiveSkillNodeId(match.id);
      }
    }
  }, [activeNode, activeCourse]);

  const activeNodeInfo = skillTreeNodes.find(n => n.id === activeSkillNodeId);

  if (isFullscreen) {
    return (
      <div className="widget-content" style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
        <div className="widget-header lib-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div className="title" style={{ touchAction: 'none' }}>
            {'Interactive Skill Tree & Branching Roadmap'}
          </div>
          <button 
            onClick={() => setFullscreen(false)} 
            style={{ 
              background: 'rgba(255, 85, 0, 0.15)', 
              border: '1px stroke var(--accent-primary)', 
              borderColor: 'var(--accent-primary)',
              color: 'var(--accent-primary)', 
              padding: '6px 14px', 
              borderRadius: '6px', 
              cursor: 'pointer', 
              fontSize: '0.8rem',
              fontWeight: 'bold',
              transition: 'var(--transition-smooth)'
            }}
          >
            {'RESTORE TO LIST'}
          </button>
        </div>
        
        <div className="fullscreen-body" style={{ flex: 1, display: 'flex', background: '#050506', position: 'relative', overflow: 'hidden' }}>
          {/* SVG Map Canvas */}
          <div style={{ flex: 1, position: 'relative', overflow: 'auto', borderRight: '1px solid var(--border-color)' }}>
            <svg 
              width="1080" 
              height="650" 
              style={{ background: 'radial-gradient(circle at center, #08080f 0%, #030305 100%)', display: 'block' }}
            >
              {/* Grid Background Overlay */}
              <defs>
                <pattern id="skillGrid" width="40" height="40" patternUnits="userSpaceOnUse">
                  <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(255, 255, 255, 0.02)" strokeWidth="1" />
                </pattern>
                <filter id="neonGlow" x="-20%" y="-20%" width="140%" height="140%">
                  <feGaussianBlur stdDeviation="6" result="blur" />
                  <feMerge>
                    <feMergeNode in="blur" />
                    <feMergeNode in="SourceGraphic" />
                  </feMerge>
                </filter>
              </defs>
              <rect width="1080" height="650" fill="url(#skillGrid)" />
              
              {/* Connection Lines */}
              {skillTreeNodes.map(node => {
                return node.deps.map(depId => {
                  const parent = skillTreeNodes.find(n => n.id === depId);
                  if (!parent) return null;
                  const isSelectedPath = activeSkillNodeId === node.id || activeSkillNodeId === parent.id;
                  return (
                    <line
                      key={`${parent.id}-${node.id}`}
                      x1={parent.x}
                      y1={parent.y}
                      x2={node.x}
                      y2={node.y}
                      stroke={isSelectedPath ? 'var(--accent-primary)' : 'rgba(255, 85, 0, 0.15)'}
                      strokeWidth={isSelectedPath ? 3 : 1.5}
                      strokeDasharray={isSelectedPath ? "none" : "5,5"}
                      style={{ transition: 'all 0.3s ease' }}
                    />
                  );
                });
              })}
              
              {/* Nodes */}
              {skillTreeNodes.map(node => {
                const isSelected = activeSkillNodeId === node.id;
                const isHovered = hoveredNodeId === node.id;
                
                // Color based on course
                let color = 'rgba(255, 85, 0, 0.4)';
                if (node.course === 'linux') color = '#38bdf8';
                if (node.course === 'network') color = '#a855f7';
                if (node.course === 'devops') color = '#22c55e';
                if (node.course === 'hosting') color = '#eab308';
                
                return (
                  <g 
                    key={node.id}
                    transform={`translate(${node.x}, ${node.y})`}
                    style={{ cursor: 'pointer' }}
                    onClick={() => {
                      setActiveSkillNodeId(node.id);
                      const targetCourse = courses.find((c: any) => c.id === node.course);
                      if (targetCourse) {
                        setActiveCourse(targetCourse);
                        setExpandedNodeId(node.nodeId);
                      }
                    }}
                    onMouseEnter={() => setHoveredNodeId(node.id)}
                    onMouseLeave={() => setHoveredNodeId(null)}
                  >
                    {/* Glowing outer shadow ring */}
                    <circle
                      r={isSelected || isHovered ? 26 : 20}
                      fill="none"
                      stroke={isSelected ? 'var(--accent-primary)' : color}
                      strokeWidth={isSelected ? 3 : 1.5}
                      style={{ transition: 'all 0.2s ease', opacity: isSelected || isHovered ? 1 : 0.6 }}
                      filter={isSelected || isHovered ? 'url(#neonGlow)' : 'none'}
                    />
                    
                    {/* Inner core circle */}
                    <circle
                      r={14}
                      fill={isSelected ? 'var(--accent-primary)' : '#050506'}
                      stroke={isSelected ? 'var(--accent-primary)' : color}
                      strokeWidth={1}
                    />
                    
                    {/* Course marker text letter */}
                    <text
                      textAnchor="middle"
                      dy="4"
                      fill={isSelected ? '#000' : '#fff'}
                      style={{ fontSize: '10px', fontWeight: 'bold', fontFamily: 'monospace' }}
                    >
                      {node.nodeId}
                    </text>
                    
                    {/* Node Text Label below */}
                    <text
                      textAnchor="middle"
                      y={38}
                      fill={isSelected ? 'var(--accent-primary)' : '#cbd5e1'}
                      style={{ 
                        fontSize: '11px', 
                        fontWeight: isSelected ? 'bold' : 'normal', 
                        fontFamily: 'monospace',
                        textShadow: isSelected ? '0 0 8px rgba(255, 85, 0, 0.4)' : 'none'
                      }}
                    >
                      {node.label.toUpperCase()}
                    </text>
                  </g>
                );
              })}
            </svg>
          </div>
          
          {/* Right Side Sidebar - Interactive Lesson Panel */}
          <div style={{ width: '380px', display: 'flex', flexDirection: 'column', background: '#09090f', padding: '20px', overflowY: 'auto' }}>
            {activeNodeInfo ? (
              <>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                  <span style={{ fontSize: '0.75rem', color: 'var(--accent-primary)', fontWeight: 'bold', letterSpacing: '0.1em', textTransform: 'uppercase' }}>
                    {activeNodeInfo.course.toUpperCase()} BRANCH
                  </span>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                    Module {activeNodeInfo.nodeId}
                  </span>
                </div>
                
                <h3 style={{ margin: '0 0 12px 0', fontSize: '1.25rem', color: '#fff', borderBottom: '1px solid var(--border-color)', paddingBottom: '10px', textTransform: 'uppercase', fontFamily: 'var(--font-geometric)' }}>
                  {activeNodeInfo.label}
                </h3>
                
                <p style={{ margin: '0 0 20px 0', fontSize: '0.85rem', color: 'var(--text-muted)', lineHeight: '1.5' }}>
                  {activeNodeInfo.desc}
                </p>
                
                <h4 style={{ margin: '0 0 10px 0', fontSize: '0.85rem', color: 'var(--accent-primary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                  {'Practical Incidents'}
                </h4>
                
                {/* Dynamically loaded syllabus nodes for the selected module */}
                {nodes.find((n: any) => n.id === activeNodeInfo.nodeId) ? (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                    {nodes.find((n: any) => n.id === activeNodeInfo.nodeId).incidents.map((inc: any) => {
                      const isActive = activeIncident?.id === inc.id && activeNode?.id === activeNodeInfo.nodeId;
                      return (
                        <div
                          key={inc.id}
                          onClick={() => {
                            const nodeObj = nodes.find((n: any) => n.id === activeNodeInfo.nodeId);
                            setActiveNode(nodeObj);
                            setActiveIncident(inc);
                          }}
                          style={{
                            padding: '10px 12px',
                            background: isActive ? 'rgba(255, 85, 0, 0.08)' : 'rgba(255, 255, 255, 0.01)',
                            border: isActive ? '1px solid var(--accent-primary)' : '1px solid var(--border-color)',
                            borderRadius: '10px',
                            cursor: 'pointer',
                            transition: 'var(--transition-smooth)',
                            boxShadow: isActive ? '0 0 8px rgba(255, 85, 0, 0.15)' : 'none'
                          }}
                        >
                          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <span style={{ fontSize: '0.8rem', fontWeight: 'bold', color: isActive ? 'var(--accent-primary)' : '#fff' }}>
                              {inc.id}. {inc.title.toUpperCase()}
                            </span>
                            {inc.isBoss && (
                              <span style={{ background: 'var(--accent-primary)', color: '#fff', fontSize: '0.6rem', padding: '2px 6px', borderRadius: '24px', fontWeight: 'bold' }}>
                                BOSS
                              </span>
                            )}
                          </div>
                          {isActive && (
                            <p style={{ margin: '6px 0 0 0', fontSize: '0.75rem', color: 'var(--text-muted)', lineHeight: '1.4' }}>
                              {inc.desc}
                            </p>
                          )}
                        </div>
                      );
                    })}
                  </div>
                ) : (
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontStyle: 'italic' }}>
                    {'Loading incidents details...'}
                  </div>
                )}
              </>
            ) : (
              <div style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-muted)', fontStyle: 'italic', fontSize: '0.85rem' }}>
                {'Select a topic node on the tree to view lessons'}
              </div>
            )}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="widget-content">
      <div className="widget-header lib-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }} {...(bindDrag ? bindDrag() : {})}>
        <div className="title" style={{ touchAction: 'none' }}>
          {'Syllabus & Lessons'}
        </div>
        <button 
          onClick={() => setFullscreen && setFullscreen(!isFullscreen)} 
          style={{ 
            background: 'rgba(255, 85, 0, 0.1)', 
            border: '1px solid var(--accent-primary)', 
            color: 'var(--accent-primary)', 
            padding: '4px 10px', 
            borderRadius: '6px', 
            cursor: 'pointer', 
            fontSize: '0.75rem',
            fontWeight: 'bold',
            transition: 'var(--transition-smooth)'
          }}
        >
          {isFullscreen ? 'RESTORE' : 'EXPAND'}
        </button>
      </div>
      <div className="widget-body" style={{ padding: '16px', height: 'calc(100% - 38px)', overflowY: 'auto' }}>
        
        {/* Onboarding / Guide Section */}
        <div className="guide-box" style={{ 
          background: 'rgba(255, 85, 0, 0.02)', 
          border: '1px solid rgba(255, 85, 0, 0.15)', 
          padding: '12px', 
          borderRadius: '12px', 
          marginBottom: '16px',
          boxShadow: '0 4px 15px rgba(0,0,0,0.1)'
        }}>
          <h4 style={{ margin: '0 0 6px 0', fontSize: '0.85rem', color: 'var(--accent-primary)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            {t[lang].guideTitle}
          </h4>
          <p style={{ margin: '0', fontSize: '0.8rem', color: 'var(--text-muted)', lineHeight: '1.4' }}>
            {t[lang].guideText}
          </p>
        </div>

        {/* Course / Syllabus Tabs */}
        <div className="course-tabs" style={{ display: 'flex', gap: '8px', marginBottom: '20px' }}>
          {courses.map((c: any) => {
            const isActive = activeCourse?.id === c.id;
            return (
              <button
                key={c.id}
                onClick={() => setActiveCourse(c)}
                style={{
                  flex: 1,
                  padding: '8px 12px',
                  background: isActive ? 'rgba(255, 85, 0, 0.08)' : 'rgba(255, 255, 255, 0.01)',
                  border: isActive ? '1px solid var(--accent-primary)' : '1px solid var(--border-color)',
                  color: isActive ? 'var(--accent-primary)' : 'var(--text-muted)',
                  fontSize: '0.85rem',
                  fontWeight: 'bold',
                  borderRadius: '24px',
                  cursor: 'pointer',
                  boxShadow: isActive ? '0 0 12px rgba(255, 85, 0, 0.25)' : 'none',
                  transition: 'var(--transition-smooth)'
                }}
              >
                {c.name.toUpperCase()}
              </button>
            );
          })}
        </div>

        {/* Collapsible Nodes Timeline */}
        <div className="nodes-timeline" style={{ display: 'flex', flexDirection: 'column', gap: '12px', position: 'relative', paddingLeft: '16px', borderLeft: '1px solid rgba(255,255,255,0.06)' }}>
          {nodes.map((n: any) => {
            const isExpanded = expandedNodeId === n.id;
            return (
              <div key={n.id} style={{ position: 'relative' }}>
                {/* Timeline circular node marker (outside the card so it never moves on hover!) */}
                <span style={{
                  position: 'absolute',
                  left: '-22px',
                  top: '12px',
                  width: '11px',
                  height: '11px',
                  borderRadius: '50%',
                  background: isExpanded ? 'var(--accent-primary)' : 'rgba(255,255,255,0.2)',
                  boxShadow: isExpanded ? '0 0 8px var(--accent-primary)' : 'none',
                  border: '2px solid #050506',
                  zIndex: 2,
                  transition: 'var(--transition-smooth)'
                }} />

                <motion.div 
                  className="node-card learning-path-node" 
                  whileHover={{ boxShadow: '0 0 16px rgba(255, 85, 0, 0.25)', borderColor: 'var(--accent-primary)' }}
                  transition={{ type: 'tween', duration: 0.2 }}
                  style={{ 
                    border: isExpanded ? '1px solid rgba(255, 85, 0, 0.2)' : '1px solid var(--border-color)', 
                    borderRadius: '16px', 
                    background: isExpanded ? 'rgba(5, 5, 6, 0.4)' : 'rgba(255, 255, 255, 0.01)',
                    boxShadow: isExpanded ? '0 4px 20px rgba(0,0,0,0.3)' : 'none',
                    transition: 'var(--transition-smooth)'
                  }}
                >
                  <div 
                    className="node-card-header" 
                    onClick={() => setExpandedNodeId(isExpanded ? null : n.id)}
                    style={{ 
                      padding: '12px 16px', 
                      cursor: 'pointer', 
                      display: 'flex', 
                      justifyContent: 'space-between', 
                      alignItems: 'center',
                      fontSize: '0.9rem',
                      fontWeight: 600
                    }}
                  >
                    <span style={{ color: isExpanded ? 'var(--accent-primary)' : 'var(--text-main)', letterSpacing: '0.02em' }}>
                      {t[lang].modulesTitle} {n.id}: {n.title.toUpperCase()}
                    </span>
                    <span style={{ color: 'var(--accent-primary)', fontSize: '0.75rem' }}>{isExpanded ? '▼' : '▶'}</span>
                  </div>

                  {isExpanded && (
                    <div className="node-card-body" style={{ padding: '0 16px 16px 16px' }}>
                      <p style={{ margin: '0 0 12px 0', fontSize: '0.8rem', color: 'var(--text-muted)', lineHeight: '1.4' }}>
                        {n.description}
                      </p>
                      <div className="incidents-grid" style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                        {n.incidents.map((inc: any) => {
                          const isActive = activeIncident?.id === inc.id && activeNode?.id === n.id;
                          return (
                            <motion.div
                              key={inc.id}
                              className={isActive ? 'active-sidebar-item' : ''}
                              whileHover={{ scale: 1.01, x: 2, background: 'rgba(255, 85, 0, 0.04)', borderColor: 'rgba(255, 85, 0, 0.3)' }}
                              transition={{ type: 'spring', stiffness: 400, damping: 25 }}
                              onClick={() => {
                                setActiveNode(n);
                                setActiveIncident(inc);
                              }}
                              style={{
                                padding: '10px 12px',
                                background: isActive ? 'rgba(255, 85, 0, 0.04)' : 'rgba(255, 255, 255, 0.01)',
                                border: isActive ? '1px solid var(--accent-primary)' : '1px solid var(--border-color)',
                                borderRadius: '12px',
                                cursor: 'pointer',
                                boxShadow: isActive ? '0 0 10px rgba(255, 85, 0, 0.15)' : 'none',
                                transition: 'var(--transition-smooth)'
                              }}
                            >
                              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <span style={{ fontSize: '0.8rem', fontWeight: 'bold', color: isActive ? 'var(--accent-primary)' : 'var(--text-main)' }}>
                                  {inc.id}. {inc.title.toUpperCase()}
                                </span>
                                {inc.isBoss && (
                                  <span style={{ background: 'var(--accent-primary)', color: '#fff', fontSize: '0.65rem', padding: '2px 6px', borderRadius: '24px', fontWeight: 'bold', letterSpacing: '0.05em' }}>
                                    {t[lang].bossIncident}
                                  </span>
                                )}
                              </div>
                              {isActive && (
                                <p style={{ margin: '6px 0 0 0', fontSize: '0.75rem', color: 'var(--text-muted)', lineHeight: '1.4' }}>
                                  {inc.desc}
                                </p>
                              )}
                            </motion.div>
                          );
                        })}
                      </div>
                    </div>
                  )}
                </motion.div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

const PlannerWidget = ({ bindDrag, activeIncident, lang }: any) => {
  const [tasks, setTasks] = useState<Array<{ id: number; text: string; done: boolean }>>([]);

  useEffect(() => {
    if (!activeIncident) {
      setTasks([
        { id: 1, text: t[lang].taskSelect, done: false }
      ]);
      return;
    }

    setTasks([
      { id: 1, text: `${t[lang].taskReview} "${activeIncident.title}"`, done: true },
      { id: 2, text: t[lang].taskExamine, done: false },
      { id: 3, text: t[lang].taskVerify, done: false }
    ]);
  }, [activeIncident, lang]);

  const toggleTask = (id: number) => {
    setTasks(prev => prev.map(t => t.id === id ? { ...t, done: !t.done } : t));
  };

  return (
    <div className="widget-content">
      <div className="widget-header" {...(bindDrag ? bindDrag() : {})}>
        <div className="title" style={{ touchAction: 'none' }}>{t[lang].plannerTitle}</div>
      </div>
      <div className="widget-body library-body" style={{ padding: '10px', height: 'calc(100% - 38px)', overflowY: 'auto' }}>
        <h4 style={{ margin: '0 0 8px 0', fontSize: '1.1rem', color: '#888', textTransform: 'uppercase' }}>{t[lang].plannerChecklist}</h4>
        <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {tasks.map(t => (
            <li 
              key={t.id} 
              onClick={() => toggleTask(t.id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                fontSize: '1.2rem',
                color: t.done ? '#888' : '#e2e8f0',
                textDecoration: t.done ? 'line-through' : 'none',
                cursor: 'pointer',
                padding: '6px',
                background: '#1c1c28',
                borderRadius: '4px',
                border: '1px solid #333'
              }}
            >
              <CheckSquare size={14} color={t.done ? '#c792ea' : '#555'} />
              <span>{t.text}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

// --- Slots Engine --- //
// 4 Screens (2x2 grid), each screen has a standard 12x8 layout template.
// This matches the user's correct sizes: chat (3x8), sys (5x2), term (5x4), aux (5x2), lesson (4x8).
const generateSlots = () => {
  const list = [];
  for (let sy = 0; sy < 2; sy++) {
    for (let sx = 0; sx < 2; sx++) {
      const colOffset = sx * 12;
      const rowOffset = sy * 8;
      
      list.push({ col: colOffset + 0, row: rowOffset + 0, w: 3, h: 8 }); // Left Column (chat)
      list.push({ col: colOffset + 3, row: rowOffset + 0, w: 5, h: 2 }); // Center Top (sys)
      list.push({ col: colOffset + 3, row: rowOffset + 2, w: 5, h: 4 }); // Center Mid (term)
      list.push({ col: colOffset + 3, row: rowOffset + 6, w: 5, h: 2 }); // Center Bot (aux)
      list.push({ col: colOffset + 8, row: rowOffset + 0, w: 4, h: 8 }); // Right Column (lesson/planner)
    }
  }
  return list;
};
const slots = generateSlots();

// --- Fluid Window Drag Wrapper --- //
const FluidWindow = ({ id, slotIdx, zoomedOut, onDragEnd, cellW, cellH, isFullscreen, children }: any) => {
  const slot = slots[slotIdx];
  const safeCellW = cellW || (window.innerWidth / 12);
  const safeCellH = cellH || (window.innerHeight / 8);

  const gap = 12;
  const targetX = isFullscreen ? 0 : slot.col * safeCellW + gap / 2;
  const targetY = isFullscreen ? 0 : slot.row * safeCellH + gap / 2;
  const w = isFullscreen ? 12 * safeCellW - gap : Math.max(slot.w * safeCellW - gap, slot.w * 65);
  const h = isFullscreen ? 8 * safeCellH - gap : Math.max(slot.h * safeCellH - gap, slot.h * 50);

  const x = useMotionValue(targetX);
  const y = useMotionValue(targetY);
  
  const [zIndex, setZIndex] = useState(isFullscreen ? 200 : 10);
  const widgetRef = useRef<HTMLDivElement>(null);
  const springConfig = { type: 'spring', stiffness: 300, damping: 30 };

  useEffect(() => {
    setZIndex(isFullscreen ? 200 : 10);
  }, [isFullscreen]);

  // Animate to position when slot changes (e.g. from swapping) or resize happens
  const isMountedRef = useRef(false);
  useEffect(() => {
    if (!isMountedRef.current) {
      isMountedRef.current = true;
      x.set(targetX);
      y.set(targetY);
      return;
    }
    // @ts-ignore
    animate(x, targetX, springConfig);
    // @ts-ignore
    animate(y, targetY, springConfig);
  }, [targetX, targetY]);

  // Delta-based drag prevents jumps from gesture offset out-of-sync
  const bindDrag = useDrag(({ delta: [dx, dy], first, last }) => {
    if (isFullscreen) return; // Disable dragging when in fullscreen mode!
    if (first) {
      window.getSelection()?.removeAllRanges();
      setZIndex(100);
      
      if (widgetRef.current) {
        const bodyEl = widgetRef.current.querySelector('.widget-body') as HTMLElement;
        if (bodyEl) bodyEl.style.pointerEvents = 'none';
      }
    }
    
    const scale = zoomedOut ? 0.5 : 1;
    const nextX = x.get() + dx / scale;
    const nextY = y.get() + dy / scale;
    
    const screenIdx = Math.floor(slotIdx / 5);
    const screenCol = screenIdx % 2;
    const screenRow = Math.floor(screenIdx / 2);
    
    const minBoundX = screenCol * 12 * safeCellW;
    const maxBoundX = (screenCol + 1) * 12 * safeCellW - 50;
    const minBoundY = screenRow * 8 * safeCellH;
    const maxBoundY = (screenRow + 1) * 8 * safeCellH - 50;
    
    x.set(Math.max(minBoundX - 200, Math.min(nextX, maxBoundX + 200)));
    y.set(Math.max(minBoundY, Math.min(nextY, maxBoundY)));

    if (last) {
      document.body.classList.remove('global-dragging');
      setZIndex(10);
      
      if (widgetRef.current) {
        const bodyEl = widgetRef.current.querySelector('.widget-body') as HTMLElement;
        if (bodyEl) bodyEl.style.pointerEvents = 'auto';
      }

      const dropX = x.get();
      const dropY = y.get();

      // Find closest slot locally to check for change
      let closestSlotIdx = 0;
      let minDistance = Infinity;
      slots.forEach((s, idx) => {
        const slotLeft = s.col * safeCellW;
        const slotTop = s.row * safeCellH;
        const dist = Math.hypot(dropX - slotLeft, dropY - slotTop);
        if (dist < minDistance) {
          minDistance = dist;
          closestSlotIdx = idx;
        }
      });

      onDragEnd(id, dropX, dropY);

      if (closestSlotIdx === slotIdx) {
        // If slot didn't change, force snap back to current slot coordinates to prevent getting stuck
        // @ts-ignore
        animate(x, targetX, springConfig);
        // @ts-ignore
        animate(y, targetY, springConfig);
      }
    }
  });

  // Listen to camera-pan events to compensate coordinates when camera shifts screens during drag
  useEffect(() => {
    const handleCameraPan = (e: Event) => {
      if (zIndex !== 100) return; // Only apply to the actively dragged window
      
      const { prevScreen, nextScreen } = (e as CustomEvent).detail;
      const w = window.innerWidth;
      const h = window.innerHeight;

      const prevCol = (prevScreen - 1) % 2;
      const prevRow = Math.floor((prevScreen - 1) / 2);
      const nextCol = (nextScreen - 1) % 2;
      const nextRow = Math.floor((nextScreen - 1) / 2);

      const shiftX = (nextCol - prevCol) * w;
      const shiftY = (nextRow - prevRow) * h;

      x.set(x.get() + shiftX);
      y.set(y.get() + shiftY);
    };

    window.addEventListener('camera-pan', handleCameraPan);
    return () => window.removeEventListener('camera-pan', handleCameraPan);
  }, [zIndex, x, y]);

  // Intercept pointer down to instantly disable edge panning before drag moves
  const bindDragWrapped = () => {
    const attrs = bindDrag();
    const originalPointerDown = attrs.onPointerDown;
    attrs.onPointerDown = (e: any) => {
      document.body.classList.add('global-dragging');
      if (originalPointerDown) originalPointerDown(e);
    };
    return attrs;
  };

  return (
    <motion.div 
      ref={widgetRef}
      className="widget-container"
      style={{ x, y, width: w, height: h, position: 'absolute', zIndex }}
    >
      {React.cloneElement(children, { bindDrag: bindDragWrapped })}
    </motion.div>
  );
};

const ParticleBackground = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationId: number;
    let particles: Array<{ x: number; y: number; vx: number; vy: number; radius: number; alpha: number }> = [];

    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    // Initialize particles
    const particleCount = 12;
    for (let i = 0; i < particleCount; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 0.4,
        vy: (Math.random() - 0.5) * 0.4,
        radius: Math.random() * 2 + 1,
        alpha: Math.random() * 0.5 + 0.1
      });
    }

    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      particles.forEach(p => {
        p.x += p.vx;
        p.y += p.vy;

        // Wrap around boundaries
        if (p.x < 0) p.x = canvas.width;
        if (p.x > canvas.width) p.x = 0;
        if (p.y < 0) p.y = canvas.height;
        if (p.y > canvas.height) p.y = 0;

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 85, 0, ${p.alpha})`;
        ctx.fill();
      });

      animationId = requestAnimationFrame(draw);
    };

    draw();

    return () => {
      window.removeEventListener('resize', resizeCanvas);
      cancelAnimationFrame(animationId);
    };
  }, []);

  return (
    <canvas 
      ref={canvasRef} 
      style={{ 
        position: 'absolute', 
        top: 0, 
        left: 0, 
        width: '100%', 
        height: '100%', 
        zIndex: 0, 
        pointerEvents: 'none',
        opacity: 0.6
      }} 
    />
  );
};

// --- Main App --- //
export default function App() {
  const [zoomedOut, setZoomedOut] = useState(false);
  const [activeScreen, setActiveScreen] = useState(1);
  const [isReady, setIsReady] = useState(true);
  const [showHud, setShowHud] = useState(false);
  const lang = 'en';
  const [syllabusExpanded, setSyllabusExpanded] = useState(false);
  
  const [stats, setStats] = useState({
    cpu: 12,
    ram: 4.2,
    ping: 15,
    core0: 10,
    core1: 15,
    core2: 8,
    core3: 14,
    diskRead: 0.2,
    diskWrite: 0.1,
    netRx: 45,
    netTx: 12,
    activeProc: 84,
    swap: 256,
    uptime: '00:00:00',
    loadAvg: '0.12, 0.08, 0.05',
    dockerStatus: 'OFFLINE'
  });

  const terminalBufferRef = useRef<string>('');
  const panTimeoutRef = useRef<any>(null);
  const [terminalEvent, setTerminalEvent] = useState<{ type: 'before' | 'after'; cmd: string; output?: string } | null>(null);
  const [defaultApiKey, setDefaultApiKey] = useState('');
  const [bootStage, setBootStage] = useState<'welcome' | 'transitioning' | 'ready'>('welcome');
  const APP_VERSION = "2.0.3";
  const [updateAvailable, setUpdateAvailable] = useState<string | null>(null);
  const [updateUrl, setUpdateUrl] = useState<string>('');

  useEffect(() => {
    // Check for updates on GitHub Releases
    fetch('https://api.github.com/repos/888ank888/terminal-academy-by-ank/releases/latest')
      .then(res => res.json())
      .then(data => {
        const latestTag = data.tag_name;
        if (latestTag) {
          const cleanLatest = latestTag.replace(/[^0-9.]/g, '');
          const cleanCurrent = APP_VERSION.replace(/[^0-9.]/g, '');
          
          // Simple semver comparison helper
          const latestParts = cleanLatest.split('.').map(Number);
          const currentParts = cleanCurrent.split('.').map(Number);
          let isNewer = false;
          for (let i = 0; i < Math.max(latestParts.length, currentParts.length); i++) {
            const l = latestParts[i] || 0;
            const c = currentParts[i] || 0;
            if (l > c) {
              isNewer = true;
              break;
            } else if (l < c) {
              break;
            }
          }

          if (isNewer) {
            setUpdateAvailable(latestTag);
            const asset = data.assets?.find((a: any) => a.name.endsWith('.dmg') || a.name.endsWith('.msi'));
            setUpdateUrl(asset ? asset.browser_download_url : data.html_url);
          }
        }
      })
      .catch(err => console.error('Error checking for updates:', err));
  }, []);
  const handleCommandBeforeExec = (cmd: string) => {
    setTerminalEvent({ type: 'before', cmd });
  };

  const handleCommandAfterExec = (cmd: string, output: string) => {
    setTerminalEvent({ type: 'after', cmd, output });
  };

  // Touchpad gesture swipe navigation between Homes (macOS/Windows)
  useEffect(() => {
    let lastSwipeTime = 0;
    const handleTouchpadSwipe = (e: WheelEvent) => {
      const target = e.target as HTMLElement;
      if (target.closest('.widget-body') || target.closest('.xterm-viewport')) return;

      const now = Date.now();
      if (now - lastSwipeTime < 800) return;

      const threshold = 55;
      const dx = e.deltaX;
      const dy = e.deltaY;

      if (Math.abs(dx) > Math.abs(dy)) {
        if (Math.abs(dx) > threshold) {
          lastSwipeTime = now;
          if (dx > 0) {
            setActiveScreen(prev => {
              if (prev === 1) return 2;
              if (prev === 3) return 4;
              return prev;
            });
          } else {
            setActiveScreen(prev => {
              if (prev === 2) return 1;
              if (prev === 4) return 3;
              return prev;
            });
          }
        }
      } else {
        if (Math.abs(dy) > threshold) {
          lastSwipeTime = now;
          if (dy > 0) {
            setActiveScreen(prev => {
              if (prev === 1) return 3;
              if (prev === 2) return 4;
              return prev;
            });
          } else {
            setActiveScreen(prev => {
              if (prev === 3) return 1;
              if (prev === 4) return 2;
              return prev;
            });
          }
        }
      }
    };

    window.addEventListener('wheel', handleTouchpadSwipe, { passive: true });
    return () => window.removeEventListener('wheel', handleTouchpadSwipe);
  }, []);

  useEffect(() => {
    let seconds = 0;
    const timer = setInterval(() => {
      seconds += 2;
      const hStr = Math.floor(seconds / 3600).toString().padStart(2, '0');
      const mStr = Math.floor((seconds % 3600) / 60).toString().padStart(2, '0');
      const sStr = (seconds % 60).toString().padStart(2, '0');

      invoke<boolean>('get_docker_status')
        .then(active => {
          setStats(prev => ({
            ...prev,
            cpu: Math.floor(Math.random() * 20) + 8,
            ram: parseFloat((4.1 + Math.random() * 0.4).toFixed(1)),
            ping: Math.floor(Math.random() * 8) + 12,
            core0: Math.floor(Math.random() * 25) + 5,
            core1: Math.floor(Math.random() * 30) + 5,
            core2: Math.floor(Math.random() * 20) + 5,
            core3: Math.floor(Math.random() * 25) + 5,
            diskRead: parseFloat((Math.random() * 1.5).toFixed(2)),
            diskWrite: parseFloat((Math.random() * 0.8).toFixed(2)),
            netRx: Math.floor(Math.random() * 200) + 50,
            netTx: Math.floor(Math.random() * 50) + 10,
            activeProc: Math.floor(Math.random() * 10) + 80,
            swap: Math.floor(Math.random() * 16) + 240,
            uptime: `${hStr}:${mStr}:${sStr}`,
            loadAvg: `${(0.1 + Math.random() * 0.15).toFixed(2)}, ${(0.05 + Math.random() * 0.08).toFixed(2)}, ${(0.03 + Math.random() * 0.05).toFixed(2)}`,
            dockerStatus: active ? 'ACTIVE' : 'OFFLINE'
          }));
        })
        .catch(() => {
          setStats(prev => ({
            ...prev,
            cpu: Math.floor(Math.random() * 20) + 8,
            ram: parseFloat((4.1 + Math.random() * 0.4).toFixed(1)),
            ping: Math.floor(Math.random() * 8) + 12,
            core0: Math.floor(Math.random() * 25) + 5,
            core1: Math.floor(Math.random() * 30) + 5,
            core2: Math.floor(Math.random() * 20) + 5,
            core3: Math.floor(Math.random() * 25) + 5,
            diskRead: parseFloat((Math.random() * 1.5).toFixed(2)),
            diskWrite: parseFloat((Math.random() * 0.8).toFixed(2)),
            netRx: Math.floor(Math.random() * 200) + 50,
            netTx: Math.floor(Math.random() * 50) + 10,
            activeProc: Math.floor(Math.random() * 10) + 80,
            swap: Math.floor(Math.random() * 16) + 240,
            uptime: `${hStr}:${mStr}:${sStr}`,
            loadAvg: `${(0.1 + Math.random() * 0.15).toFixed(2)}, ${(0.05 + Math.random() * 0.08).toFixed(2)}, ${(0.03 + Math.random() * 0.05).toFixed(2)}`,
            dockerStatus: 'OFFLINE'
          }));
        });
    }, 2000);
    return () => clearInterval(timer);
  }, []);
  
  // Track window dimensions dynamically for resizing
  const [dimensions, setDimensions] = useState({
    w: window.innerWidth,
    h: window.innerHeight
  });

  const [explainCommand, setExplainCommand] = useState<string | null>(null);

  // Widget to Slot mapping
  const [widgetSlots, setWidgetSlots] = useState<{ [id: string]: number }>({
    chat: 0,
    sys: 1,
    term: 2,
    aux: 3,
    lesson: 4,
    planner: 5 // First slot of Screen 2
  });

  // Syllabus / Curriculum loader state
  const courses = [
    { id: 'linux', name: 'Linux Core & SysAdmin', file: '/curriculum_linux.md' },
    { id: 'network', name: 'Networking & Security', file: '/curriculum_network.md' },
    { id: 'devops', name: 'DevOps & Containers', file: '/curriculum_devops.md' },
    { id: 'hosting', name: 'App Hosting', file: '/curriculum_hosting.md' }
  ];
  const [activeCourse, setActiveCourse] = useState(courses[0]);
  const [nodes, setNodes] = useState<any[]>([]);
  const [activeNode, setActiveNode] = useState<any>(null);
  const [activeIncident, setActiveIncident] = useState<any>(null);

  // Load and parse course syllabus whenever activeCourse changes
  useEffect(() => {
    fetch(activeCourse.file)
      .then(res => res.text())
      .then(text => {
        const parsed = parseSyllabus(text);
        setNodes(parsed);
        if (parsed.length > 0) {
          setActiveNode(parsed[0]);
          setActiveIncident(parsed[0].incidents[0] || null);
        } else {
          setActiveNode(null);
          setActiveIncident(null);
        }
      })
      .catch(err => console.error('Error loading syllabus:', err));
  }, [activeCourse]);

  useEffect(() => {
    setIsReady(true);
    
    // Load Russian translation dynamically if present (excluded from remote git index)
    fetch('/translation_ru.json')
      .then(res => {
        if (!res.ok) throw new Error('Not found');
        return res.json();
      })
      .then(data => {
        t.ru = data;
      })
      .catch(() => {
        // Fallback to English
        t.ru = { ...t.en };
      });

    // Load default API key fallback config if present (ignored in git)
    fetch('/config.json')
      .then(res => {
        if (!res.ok) throw new Error('Not found');
        return res.json();
      })
      .then(data => {
        if (data.default_api_key) {
          setDefaultApiKey(data.default_api_key);
        }
      })
      .catch(() => {
        setDefaultApiKey('');
      });

    const handleResize = () => {
      setDimensions({ w: window.innerWidth, h: window.innerHeight });
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Global key listener for Overview Mode (Alt)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Alt') setZoomedOut(true);
    };
    const handleKeyUp = (e: KeyboardEvent) => {
      if (e.key === 'Alt') setZoomedOut(false);
    };
    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, []);

  // Global key listener for HUD toggling (Ctrl+H)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.ctrlKey && e.key.toLowerCase() === 'h') {
        e.preventDefault();
        setShowHud(prev => !prev);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Wheel zoom listener (mouse-centered zoom-in/out)
  useEffect(() => {
    const handleWheel = (e: WheelEvent) => {
      const target = e.target as HTMLElement;
      // Prevent zooming if scrolling inside xterm or widget bodies
      if (target.closest('.widget-body')) return;

      if (e.deltaY > 30) {
        setZoomedOut(true);
      } else if (e.deltaY < -30) {
        setZoomedOut(false);
      }
    };
    window.addEventListener('wheel', handleWheel, { passive: true });
    return () => window.removeEventListener('wheel', handleWheel);
  }, []);

  // Mouse hover per-screen navigation (cursor-driven edge scrolling with hover delay)
  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      const w = dimensions.w;
      const h = dimensions.h;
      const mx = e.clientX;
      const my = e.clientY;

      if (zoomedOut) {
        if (document.body.classList.contains('global-dragging')) return;
        
        // In Overview mode, hover determines which screen we will zoom into
        const colIdx = mx < w / 2 ? 0 : 1;
        const rowIdx = my < h / 2 ? 0 : 1;
        const targetScreen = rowIdx * 2 + colIdx + 1;
        setActiveScreen(targetScreen);
      } else {
        // Edge-detection panning in Zoomed In mode
        const edgeX = 40;
        const edgeY = 60;
        
        let targetScreenPan: number | null = null;
        if (activeScreen === 1) {
          if (mx > w - edgeX) targetScreenPan = 2;
          else if (my > h - edgeY) targetScreenPan = 3;
        } else if (activeScreen === 2) {
          if (mx < edgeX) targetScreenPan = 1;
          else if (my > h - edgeY) targetScreenPan = 4;
        } else if (activeScreen === 3) {
          if (mx > w - edgeX) targetScreenPan = 4;
          else if (my < edgeY) targetScreenPan = 1;
        } else if (activeScreen === 4) {
          if (mx < edgeX) targetScreenPan = 3;
          else if (my < edgeY) targetScreenPan = 2;
        }

        if (targetScreenPan !== null) {
          // If already waiting to pan to this screen, do nothing
          if (panTimeoutRef.current) return;

          // Start a 1200ms delay before panning to prevent accidental edge teleports
          panTimeoutRef.current = setTimeout(() => {
            setActiveScreen(prev => {
              if (targetScreenPan !== null) {
                window.dispatchEvent(new CustomEvent('camera-pan', {
                  detail: { prevScreen: prev, nextScreen: targetScreenPan }
                }));
                return targetScreenPan;
              }
              return prev;
            });
            panTimeoutRef.current = null;
          }, 1200);
        } else {
          // Mouse left the edge, cancel the transition timer
          if (panTimeoutRef.current) {
            clearTimeout(panTimeoutRef.current);
            panTimeoutRef.current = null;
          }
        }
      }
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      if (panTimeoutRef.current) clearTimeout(panTimeoutRef.current);
    };
  }, [zoomedOut, activeScreen, dimensions]);

  const handleDragEnd = (id: string, dropX: number, dropY: number) => {
    const cellW = dimensions.w / 12;
    const cellH = dimensions.h / 8;

    const oldSlotIdx = widgetSlots[id];
    const originalScreenIdx = Math.floor(oldSlotIdx / 5);

    // Find closest slot on the same screen
    let closestSlotIdx = oldSlotIdx;
    let minDistance = Infinity;

    slots.forEach((slot, idx) => {
      const slotScreenIdx = Math.floor(idx / 5);
      if (slotScreenIdx !== originalScreenIdx) return;

      const slotLeft = slot.col * cellW;
      const slotTop = slot.row * cellH;
      const dist = Math.hypot(dropX - slotLeft, dropY - slotTop);
      if (dist < minDistance) {
        minDistance = dist;
        closestSlotIdx = idx;
      }
    });

    setWidgetSlots(prev => {
      const next = { ...prev };
      const oldSlot = next[id];

      // Swap logic if target slot occupied
      let occupantId: string | null = null;
      for (const wId in next) {
        if (wId === id) continue;
        if (next[wId] === closestSlotIdx) {
          occupantId = wId;
          break;
        }
      }

      if (occupantId) {
        next[occupantId] = oldSlot;
        next[id] = closestSlotIdx;
      } else {
        next[id] = closestSlotIdx;
      }

      // Automatically focus target screen
      const targetSlot = slots[closestSlotIdx];
      const screenX = Math.floor(targetSlot.col / 12);
      const screenY = Math.floor(targetSlot.row / 8);
      const newActiveScreen = screenY * 2 + screenX + 1;
      setActiveScreen(newActiveScreen);

      return next;
    });
  };

// --- Detached Floating HUD Header --- //
const HudHeader = ({ zoomedOut, setZoomedOut, activeScreen, setActiveScreen, activeCourse, lang, updateAvailable, updateUrl }: any) => {
  return (
    <div className="hud-header">
      <div className="hud-brand">
        <span className="ping-indicator"></span>
        <span className="hud-title">{t[lang].hudTitle}</span>
      </div>
      <div className="hud-status">
        <span className="hud-label">{t[lang].hudBranch}</span>
        <span className="hud-value">{activeCourse?.name.toUpperCase() || 'NONE'}</span>
      </div>
      <div className="hud-controls">
        {updateAvailable && (
          <motion.button 
            animate={{ 
              boxShadow: [
                '0 0 8px rgba(34, 197, 94, 0.4)',
                '0 0 20px rgba(34, 197, 94, 0.7)',
                '0 0 8px rgba(34, 197, 94, 0.4)'
              ] 
            }}
            transition={{ repeat: Infinity, duration: 2 }}
            onClick={() => {
              window.open(updateUrl, '_blank');
            }}
            style={{
              background: 'linear-gradient(135deg, #22c55e 0%, #16a34a 100%)',
              border: 'none',
              color: '#fff',
              padding: '6px 12px',
              borderRadius: '6px',
              fontSize: '0.75rem',
              fontWeight: 'bold',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              boxShadow: '0 0 10px rgba(34, 197, 94, 0.4)',
              marginRight: '8px'
            }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <span style={{ display: 'inline-block', width: '6px', height: '6px', borderRadius: '50%', background: '#fff' }} />
            {`Update to ${updateAvailable}`}
          </motion.button>
        )}

        <button 
          className={`hud-btn ${zoomedOut ? 'active' : ''}`}
          onClick={() => setZoomedOut(!zoomedOut)}
        >
          {zoomedOut ? t[lang].hudViewDetailed : t[lang].hudViewOverview}
        </button>
        <div className="screen-selectors">
          {[1, 2, 3, 4].map(sNum => (
            <button 
              key={sNum}
              className={`hud-btn screen-btn ${activeScreen === sNum && !zoomedOut ? 'active' : ''}`}
              onClick={() => {
                setActiveScreen(sNum);
                setZoomedOut(false);
              }}
            >
              {t[lang].screen} {sNum}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

  const getTransform = () => {
    if (zoomedOut) {
      return `scale(0.5) translate(0%, 0%)`; // Static 4-screen centered overview
    }
    const S = 1;
    const colIdx = (activeScreen - 1) % 2;
    const rowIdx = Math.floor((activeScreen - 1) / 2);
    
    const cx = (colIdx + 0.5) * 100;
    const cy = (rowIdx + 0.5) * 100;
    
    const tx = 100 / (2 * S) - cx;
    const ty = 100 / (2 * S) - cy;
    
    const txPct = (tx / 200) * 100;
    const tyPct = (ty / 200) * 100;
    
    return `scale(${S}) translate(${txPct}%, ${tyPct}%)`;
  };

  return (
    <div className="viewport">
      <AnimatePresence>
        {bootStage !== 'ready' && (
          <motion.div 
            key="welcome-overlay"
            initial={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 1.2, ease: 'easeInOut' }}
            style={{
              position: 'fixed',
              top: 0,
              left: 0,
              width: '100vw',
              height: '100vh',
              background: 'radial-gradient(circle at center, #0a0a14 0%, #030305 100%)',
              color: '#fff',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              zIndex: 99999,
              fontFamily: 'monospace',
              overflow: 'hidden'
            }}
          >
            <div style={{
              position: 'absolute',
              width: '100%',
              height: '100%',
              backgroundImage: 'radial-gradient(rgba(255, 85, 0, 0.05) 1px, transparent 0)',
              backgroundSize: '24px 24px',
              opacity: 0.8,
              pointerEvents: 'none'
            }} />

            {/* Logo Container (Ready to load the transparent 800x600 animation) */}
            <motion.div 
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ duration: 0.8 }}
              style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginBottom: '20px', zIndex: 2 }}
            >
              <div 
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
              </div>
              <h1 style={{
                fontSize: '1.8rem',
                fontWeight: 800,
                letterSpacing: '0.15em',
                margin: '0 0 8px 0',
                textTransform: 'uppercase',
                color: '#fff',
                textShadow: '0 0 12px rgba(255,255,255,0.2)',
                fontFamily: 'Space Grotesk, sans-serif'
              }}>
                Terminal Academy
              </h1>
              <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', letterSpacing: '0.05em' }}>
                CODENAME: SYSTEMS ACADEMY v2.0.3
              </span>
            </motion.div>

            {bootStage === 'welcome' || bootStage === 'transitioning' ? (
              <>
                <p style={{ margin: '0 0 25px 0', fontSize: '0.85rem', color: '#eab308', letterSpacing: '0.05em', zIndex: 2, maxWidth: '480px', textAlign: 'center', lineHeight: '1.4' }}>
                  {'⚠️ RECOMMENDED: Expand the window to fullscreen mode to fit the 4-panel dashboard panels properly.'}
                </p>
                <motion.button
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ type: 'spring', stiffness: 200, damping: 15 }}
                  onClick={async () => {
                    // Go Fullscreen
                    try {
                      const { getCurrentWindow } = await import('@tauri-apps/api/window');
                      const appWindow = getCurrentWindow();
                      await appWindow.setFullscreen(true);
                    } catch (e) {
                      document.documentElement.requestFullscreen().catch(() => {});
                    }
                    
                    setBootStage('transitioning');
                    setTimeout(() => {
                      setBootStage('ready');
                    }, 150);
                  }}
                  style={{
                    padding: '14px 40px',
                    background: 'rgba(255, 85, 0, 0.1)',
                    border: '2px solid var(--accent-primary)',
                    color: 'var(--accent-primary)',
                    borderRadius: '30px',
                    fontSize: '0.95rem',
                    fontWeight: 'bold',
                    cursor: 'pointer',
                    textTransform: 'uppercase',
                    letterSpacing: '0.1em',
                    boxShadow: '0 0 25px rgba(255, 85, 0, 0.25)',
                    transition: 'all 0.3s ease',
                    zIndex: 2
                  }}
                  whileHover={{ scale: 1.05, boxShadow: '0 0 35px rgba(255, 85, 0, 0.45)', background: 'var(--accent-primary)', color: '#000' }}
                  whileTap={{ scale: 0.98 }}
                >
                  {'ENTER FULLSCREEN & BOOT'}
                </motion.button>
              </>
            ) : null}
          </motion.div>
        )}
      </AnimatePresence>
      <ParticleBackground />
      {!showHud ? (
        <button 
          className="hud-toggle-btn"
          onClick={() => setShowHud(true)}
          style={{
            position: 'absolute',
            bottom: '12px',
            left: '50%',
            transform: 'translateX(-50%)',
            zIndex: 1001,
            background: 'var(--bg-raised)',
            backdropFilter: 'blur(16px)',
            border: '1px solid var(--border-color)',
            color: 'var(--text-muted)',
            padding: '6px 12px',
            borderRadius: '12px',
            fontSize: '0.8rem',
            fontWeight: 'bold',
            letterSpacing: '0.05em',
            cursor: 'pointer',
            boxShadow: '0 4px 20px rgba(0,0,0,0.5)',
            transition: 'var(--transition-smooth)'
          }}
        >
          {t[lang].hudShow}
        </button>
      ) : (
        <>
          <HudHeader 
            zoomedOut={zoomedOut}
            setZoomedOut={setZoomedOut}
            activeScreen={activeScreen}
            setActiveScreen={setActiveScreen}
            activeCourse={activeCourse}
            lang={lang}
            updateAvailable={updateAvailable}
            updateUrl={updateUrl}
          />
          <button 
            className="hud-close-btn"
            onClick={() => setShowHud(false)}
            style={{
              position: 'absolute',
              bottom: '84px',
              left: '50%',
              transform: 'translateX(-50%)',
              zIndex: 1001,
              background: 'var(--bg-raised)',
              backdropFilter: 'blur(16px)',
              border: '1px solid var(--border-color)',
              color: 'var(--accent-primary)',
              padding: '4px 10px',
              borderRadius: '8px',
              fontSize: '0.75rem',
              fontWeight: 'bold',
              cursor: 'pointer',
              boxShadow: '0 4px 15px rgba(0,0,0,0.4)',
              transition: 'var(--transition-smooth)'
            }}
          >
            {t[lang].hudHide}
          </button>
        </>
      )}
      
      <div 
        className="world"
        style={{
          transform: getTransform()
        }}
      >
        <div className="background-grid" style={{ pointerEvents: zoomedOut ? 'auto' : 'none' }}>
          <div className="screen" onClick={() => zoomedOut && (setActiveScreen(1), setZoomedOut(false))} style={{ backgroundSize: '8.333% 12.5%' }}>
          </div>
          <div className="screen" onClick={() => zoomedOut && (setActiveScreen(2), setZoomedOut(false))} style={{ backgroundSize: '8.333% 12.5%' }}>
          </div>
          <div className="screen" onClick={() => zoomedOut && (setActiveScreen(3), setZoomedOut(false))} style={{ backgroundSize: '8.333% 12.5%' }}>
          </div>
          <div className="screen" onClick={() => zoomedOut && (setActiveScreen(4), setZoomedOut(false))} style={{ backgroundSize: '8.333% 12.5%' }}>
          </div>
        </div>
        
        <div 
          className="global-widget-layer"
          style={{ pointerEvents: zoomedOut ? 'none' : 'auto' }}
        >
          {isReady && (
            <>
              <FluidWindow id="chat" slotIdx={widgetSlots.chat} zoomedOut={zoomedOut} onDragEnd={handleDragEnd} cellW={dimensions.w / 12} cellH={dimensions.h / 8}>
                <ChatWidget 
                  activeCourse={activeCourse}
                  activeNode={activeNode}
                  activeIncident={activeIncident}
                  lang={lang}
                  terminalBuffer={terminalBufferRef.current}
                  systemStats={stats}
                  explainCommand={explainCommand}
                  setExplainCommand={setExplainCommand}
                  terminalEvent={terminalEvent}
                  setTerminalEvent={setTerminalEvent}
                  defaultApiKey={defaultApiKey}
                />
              </FluidWindow>
              
              <FluidWindow id="sys" slotIdx={widgetSlots.sys} zoomedOut={zoomedOut} onDragEnd={handleDragEnd} cellW={dimensions.w / 12} cellH={dimensions.h / 8}>
                <MonitoringWidget lang={lang} stats={stats} />
              </FluidWindow>
              
              <FluidWindow id="term" slotIdx={widgetSlots.term} zoomedOut={zoomedOut} onDragEnd={handleDragEnd} cellW={dimensions.w / 12} cellH={dimensions.h / 8}>
                <TerminalWidget 
                  lang={lang} 
                  onTerminalData={(data: string) => {
                    terminalBufferRef.current = (terminalBufferRef.current + data).slice(-2000);
                  }}
                  dockerStatus={stats.dockerStatus}
                  onCommandBeforeExec={handleCommandBeforeExec}
                  onCommandAfterExec={handleCommandAfterExec}
                />
              </FluidWindow>
              
              <FluidWindow id="aux" slotIdx={widgetSlots.aux} zoomedOut={zoomedOut} onDragEnd={handleDragEnd} cellW={dimensions.w / 12} cellH={dimensions.h / 8}>
                <LibraryWidget 
                  activeIncident={activeIncident}
                  lang={lang}
                  onExplainCommand={setExplainCommand}
                />
              </FluidWindow>
              
              <FluidWindow 
                id="lesson" 
                slotIdx={widgetSlots.lesson} 
                zoomedOut={zoomedOut} 
                onDragEnd={handleDragEnd} 
                cellW={dimensions.w / 12} 
                cellH={dimensions.h / 8}
                isFullscreen={syllabusExpanded}
              >
                <LessonWidget 
                  courses={courses}
                  activeCourse={activeCourse}
                  setActiveCourse={setActiveCourse}
                  nodes={nodes}
                  activeNode={activeNode}
                  setActiveNode={setActiveNode}
                  activeIncident={activeIncident}
                  setActiveIncident={setActiveIncident}
                  lang={lang}
                  isFullscreen={syllabusExpanded}
                  setFullscreen={setSyllabusExpanded}
                />
              </FluidWindow>
 
              <FluidWindow id="planner" slotIdx={widgetSlots.planner} zoomedOut={zoomedOut} onDragEnd={handleDragEnd} cellW={dimensions.w / 12} cellH={dimensions.h / 8}>
                <PlannerWidget 
                  activeIncident={activeIncident}
                  lang={lang}
                />
              </FluidWindow>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
