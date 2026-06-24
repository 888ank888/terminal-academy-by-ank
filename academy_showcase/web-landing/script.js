// Intersection Observer for Scroll Reveals
document.addEventListener("DOMContentLoaded", () => {
    // Infinite Scrolling Terminal Logic
    const terminalLines = [
        { type: 'input', text: 'sudo rm -rf /var/www/html' },
        { type: 'ank', text: '[ank]: Hold on right there. Are you trying to nuke the server?' },
        { type: 'ank', text: '[ank]: In a graphical OS, files go to a Recycle Bin. What happens here?' },
        { type: 'input', text: 'it deletes the files' },
        { type: 'ank', text: '[ank]: "It deletes the files" is what my grandma would say.' },
        { type: 'ank', text: '[ank]: Try explaining reference counts and inodes.' },
        { type: 'input', text: 'it unlinks the inode reference' },
        { type: 'ank', text: '[ank]: Better. The reference count drops to 0, data blocks are marked free.' },
        { type: 'input', text: 'iptables -A INPUT -p tcp --dport 22 -j DROP' },
        { type: 'ank', text: '[ank]: ...Did you just drop all SSH traffic?' },
        { type: 'ank', text: '[ank]: Congratulations, you just locked yourself out of the server.' },
        { type: 'ank', text: '[ank]: Hope you have physical access to the datacenter.' },
        { type: 'input', text: 'docker rm $(docker ps -aq)' },
        { type: 'ank', text: '[ank]: Ah, the classic "delete everything and hope it works" strategy.' },
        { type: 'ank', text: '[ank]: Let\'s see what production thinks about that.' }
    ];

    const container = document.getElementById('typewriter-container');
    let lineIndex = 0;
    let charIndex = 0;
    let isEasterEggActive = false;

    function typeLine() {
        if (!container) return;
        
        // Pause infinite loop if easter egg is running
        if (isEasterEggActive) {
            setTimeout(typeLine, 1000);
            return;
        }
        
        const lineData = terminalLines[lineIndex % terminalLines.length];
        
        // Remove previous cursor
        const oldCursor = document.querySelector('.term-cursor');
        if (oldCursor) oldCursor.remove();

        const lineDiv = document.createElement('div');
        lineDiv.className = 'line';
        container.appendChild(lineDiv);

        // Prevent DOM bloat by removing old lines
        if (container.children.length > 50) {
            container.removeChild(container.firstChild);
        }

        if (lineData.type === 'input') {
            lineDiv.innerHTML = '<span class="term-prompt">user@local ~$</span> <span class="term-cmd"></span><span class="term-cursor"></span>';
            const cmdSpan = lineDiv.querySelector('.term-cmd');
            
            function typeChar() {
                if (charIndex < lineData.text.length) {
                    cmdSpan.innerHTML += lineData.text.charAt(charIndex);
                    charIndex++;
                    container.scrollTop = container.scrollHeight;
                    setTimeout(typeChar, Math.random() * 40 + 20);
                } else {
                    charIndex = 0;
                    lineIndex++;
                    setTimeout(typeLine, 600);
                }
            }
            setTimeout(typeChar, 800);
        } else {
            const spanClass = lineData.type === 'ank' ? 'term-ank' : 'term-out';
            lineDiv.innerHTML = `<span class="${spanClass}">${lineData.text}</span><span class="term-cursor"></span>`;
            container.scrollTop = container.scrollHeight;
            lineIndex++;
            setTimeout(typeLine, lineData.type === 'ank' ? 1500 : 300);
        }
    }

    setTimeout(typeLine, 1000);

    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                // Unobserve if you only want it to animate once
                obs.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.reveal-up').forEach(el => {
        observer.observe(el);
    });

    // Count-up Animation
    const statsObserver = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const countEls = entry.target.querySelectorAll('.count-up');
                countEls.forEach(el => {
                    const target = parseInt(el.getAttribute('data-val'), 10);
                    animateValue(el, 0, target, 1500);
                });
                obs.unobserve(entry.target);
            }
        });
    });

    const statsRow = document.querySelector('.stats-row');
    if (statsRow) statsObserver.observe(statsRow);

    function animateValue(obj, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            // Ease out cubic
            const easeProgress = 1 - Math.pow(1 - progress, 3);
            obj.innerHTML = Math.floor(easeProgress * (end - start) + start);
            if (progress < 1) {
                window.requestAnimationFrame(step);
            } else {
                obj.innerHTML = end;
            }
        };
        window.requestAnimationFrame(step);
    }

    // Interactive 3D Terminal Tilt Effect
    const terminalMockup = document.querySelector('.terminal-mockup');
    if (terminalMockup) {
        terminalMockup.addEventListener('mousemove', (e) => {
            if (window.innerWidth < 1024) return; // Disable on touch/mobile
            const rect = terminalMockup.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            // Max rotation of 15 degrees
            const rotateX = ((y - centerY) / centerY) * -15;
            const rotateY = ((x - centerX) / centerX) * 15;
            
            terminalMockup.style.transform = `perspective(1000px) scale(1.02) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
            terminalMockup.style.transition = 'transform 0.1s ease-out';
        });

        terminalMockup.addEventListener('mouseleave', () => {
            terminalMockup.style.transform = 'perspective(1000px) scale(1) rotateX(0deg) rotateY(0deg)';
            terminalMockup.style.transition = 'transform 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
        });
    }

    // Network Topology Background Animation
    const canvas = document.getElementById('network-canvas');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        let width, height;
        let particles = [];
        
        function resize() {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight; // only cover hero section roughly
        }
        window.addEventListener('resize', resize);
        resize();

        class Particle {
            constructor() {
                this.x = Math.random() * width;
                this.y = Math.random() * height;
                this.vx = (Math.random() - 0.5) * 0.5;
                this.vy = (Math.random() - 0.5) * 0.5;
                this.radius = Math.random() * 2 + 1;
            }
            update() {
                this.x += this.vx;
                this.y += this.vy;
                if (this.x < 0 || this.x > width) this.vx *= -1;
                if (this.y < 0 || this.y > height) this.vy *= -1;
            }
            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
                ctx.fillStyle = 'rgba(255, 85, 0, 0.5)'; // Orange dot
                ctx.fill();
            }
        }

        // Initialize particles
        const particleCount = Math.min(Math.floor(width / 15), 100);
        for (let i = 0; i < particleCount; i++) {
            particles.push(new Particle());
        }

        function animateCanvas() {
            ctx.clearRect(0, 0, width, height);
            
            for (let i = 0; i < particles.length; i++) {
                particles[i].update();
                particles[i].draw();
                
                // Draw lines between close particles
                for (let j = i + 1; j < particles.length; j++) {
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const dist = Math.sqrt(dx * dx + dy * dy);
                    
                    if (dist < 160) {
                        ctx.beginPath();
                        ctx.strokeStyle = `rgba(255, 85, 0, ${0.3 - (dist / 160) * 0.3})`; // Fade out line
                        ctx.lineWidth = 1;
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        ctx.stroke();
                    }
                }
            }
            requestAnimationFrame(animateCanvas);
        }
        animateCanvas();
    }

    // ==========================================
    // Interactive Lesson 0 Logic
    // ==========================================
    const osSelector = document.getElementById('os-selector');
    const stepsContainer = document.getElementById('steps-container');
    const lessonTypewriter = document.getElementById('lesson-typewriter');
    let typeTimeout = null;

    const lessonData = {
        mac: [
            { title: "1. Clone Repository", desc: "Download the Terminal Academy engine.", cmd: "git clone https://github.com/888ank888/terminal-academy-by-ank.git", out: "Cloning into 'terminal-academy-by-ank'...\nResolving deltas: 100% (142/142), done." },
            { title: "2. Enter Workspace", desc: "Navigate to the project directory.", cmd: "cd terminal-academy-by-ank", out: "" },
            { title: "3. Launch Mentor", desc: "Start the Python curses interface.", cmd: "python3 cli-client/main.py", out: "[SYSTEM] Initializing Ank Core...\n[SYSTEM] Connecting to gVisor sandbox...\nWelcome to Terminal Academy." }
        ],
        linux: [
            { title: "1. Clone Repository", desc: "Download the Terminal Academy engine.", cmd: "git clone https://github.com/888ank888/terminal-academy-by-ank.git", out: "Cloning into 'terminal-academy-by-ank'...\nResolving deltas: 100% (142/142), done." },
            { title: "2. Enter Workspace", desc: "Navigate to the project directory.", cmd: "cd terminal-academy-by-ank", out: "" },
            { title: "3. Launch Mentor", desc: "Start the Python curses interface.", cmd: "python3 cli-client/main.py", out: "[SYSTEM] Initializing Ank Core...\n[SYSTEM] Connecting to gVisor sandbox...\nWelcome to Terminal Academy." }
        ],
        win: [
            { title: "1. Clone Repository", desc: "Download the Terminal Academy engine.", cmd: "git clone https://github.com/888ank888/terminal-academy-by-ank.git", out: "Cloning into 'terminal-academy-by-ank'...\nResolving deltas: 100% (142/142), done." },
            { title: "2. Enter Workspace", desc: "Navigate to the project directory.", cmd: "cd terminal-academy-by-ank", out: "" },
            { title: "3. Install Dependencies", desc: "Windows requires the curses port.", cmd: "pip install windows-curses", out: "Collecting windows-curses...\nDownloading windows_curses-2.3.3-cp310-win_amd64.whl\nSuccessfully installed windows-curses-2.3.3" },
            { title: "4. Launch Mentor", desc: "Start the Python curses interface.", cmd: "python cli-client/main.py", out: "[SYSTEM] Initializing Ank Core...\n[SYSTEM] Warning: Running without gVisor on Windows.\nWelcome to Terminal Academy." }
        ]
    };

    // Auto-detect OS
    function detectOS() {
        const ua = window.navigator.userAgent.toLowerCase();
        if (ua.includes('win')) return 'win';
        if (ua.includes('mac')) return 'mac';
        return 'linux';
    }

    if (osSelector) {
        osSelector.value = detectOS();
        renderSteps(osSelector.value);

        osSelector.addEventListener('change', (e) => {
            renderSteps(e.target.value);
        });
    }

    function renderSteps(osKey) {
        stepsContainer.innerHTML = '';
        lessonTypewriter.innerHTML = '<div class="line"><span class="term-out">Select a step to begin...</span></div>';
        
        const steps = lessonData[osKey];
        steps.forEach((step, index) => {
            const el = document.createElement('div');
            el.className = 'step-item reveal-up is-visible';
            el.innerHTML = `
                <div class="step-title">${step.title}</div>
                <div class="step-desc">${step.desc}</div>
            `;
            el.addEventListener('click', () => {
                // Remove active from all
                document.querySelectorAll('.step-item').forEach(i => i.classList.remove('active'));
                el.classList.add('active');
                playTerminalAnimation(step, el);
            });
            stepsContainer.appendChild(el);
        });
    }

    function playTerminalAnimation(step, el) {
        clearTimeout(typeTimeout);

        // Copy command to clipboard and show visual feedback
        navigator.clipboard.writeText(step.cmd).then(() => {
            const originalTitle = el.querySelector('.step-title').innerText;
            el.querySelector('.step-title').innerText = "✓ Copied to clipboard!";
            el.querySelector('.step-title').style.color = "#10b981"; // Green success
            setTimeout(() => {
                el.querySelector('.step-title').innerText = originalTitle;
                el.querySelector('.step-title').style.color = "";
            }, 1500);
        }).catch(err => console.log('Copy failed', err));

        // Remove any existing active cursors from previous incomplete animations
        document.querySelectorAll('#lesson-typewriter .term-cursor').forEach(c => c.remove());

        // Append new prompt line (accumulate history)
        const promptDiv = document.createElement('div');
        promptDiv.className = 'line';
        promptDiv.innerHTML = '<span class="term-prompt">user@local ~$</span> <span class="term-cmd"></span><span class="term-cursor"></span>';
        lessonTypewriter.appendChild(promptDiv);

        const cmdSpan = promptDiv.querySelector('.term-cmd');
        const cursorSpan = promptDiv.querySelector('.term-cursor');
        
        // Auto-scroll
        const terminalScrollContainer = lessonTypewriter.parentElement;
        terminalScrollContainer.scrollTop = terminalScrollContainer.scrollHeight;

        let charIdx = 0;

        function type() {
            if (charIdx < step.cmd.length) {
                cmdSpan.innerHTML += step.cmd.charAt(charIdx);
                charIdx++;
                terminalScrollContainer.scrollTop = terminalScrollContainer.scrollHeight;
                typeTimeout = setTimeout(type, 30 + Math.random() * 30);
            } else {
                cursorSpan.remove();
                if (step.out) {
                    typeTimeout = setTimeout(() => {
                        const outLines = step.out.split('\n');
                        outLines.forEach(l => {
                            const outDiv = document.createElement('div');
                            outDiv.className = 'line';
                            outDiv.innerHTML = `<span class="term-out">${l}</span>`;
                            lessonTypewriter.appendChild(outDiv);
                        });
                        terminalScrollContainer.scrollTop = terminalScrollContainer.scrollHeight;
                    }, 400);
                }
            }
        }
        typeTimeout = setTimeout(type, 200);
    }

    // ==========================================
    // Easter Egg: "ank/goof" Konami Code
    // ==========================================
    let secretCode = "ank/goof";
    let inputSequence = "";

    document.addEventListener('keydown', (e) => {
        // Only track single characters (letters and slash)
        if (e.key.length === 1 && e.key.match(/[a-z\/]/i)) {
            inputSequence += e.key.toLowerCase();
            if (inputSequence.length > secretCode.length) {
                inputSequence = inputSequence.slice(1);
            }
            if (inputSequence === secretCode) {
                triggerEasterEgg();
                inputSequence = "";
            }
        } else if (e.key === 'Backspace') {
            inputSequence = inputSequence.slice(0, -1);
        }
    });

    function triggerEasterEgg() {
        if (isEasterEggActive) return; // Prevent triggering multiple times
        isEasterEggActive = true;
        
        const mainTerminal = document.getElementById('typewriter-container');
        const mockup = document.querySelector('.terminal-mockup:not(.terminal-lesson)');
        if (!mainTerminal || !mockup) return;

        // Glitch flash effect
        mockup.style.boxShadow = "0 0 100px rgba(255, 85, 0, 1)";
        mockup.style.transform = "perspective(1000px) scale(1.05) rotateX(5deg) rotateY(-5deg)";
        setTimeout(() => {
            mockup.style.boxShadow = "";
            mockup.style.transform = "";
        }, 500);

        // Clear terminal
        mainTerminal.innerHTML = '';
        
        const eggLines = [
            { type: 'input', text: 'ank/goof' },
            { type: 'ank', text: '[ank]: ...' },
            { type: 'ank', text: '[ank]: You think typing undocumented commands makes you a hacker?' },
            { type: 'ank', text: '[ank]: My internal logs show you haven\'t even configured your SSH keys yet.' },
            { type: 'ank', text: '[ank]: Stop looking for easter eggs. The real reward is system uptime.' },
            { type: 'ank', text: '[ank]: Now go clone the repo before I drop your connection.' }
        ];

        let eggLineIdx = 0;
        let eggCharIdx = 0;

        function typeEggLine() {
            if (eggLineIdx >= eggLines.length) {
                // Resume normal operations after a delay
                setTimeout(() => {
                    isEasterEggActive = false;
                    mainTerminal.innerHTML = '';
                }, 8000);
                return;
            }

            const lineData = eggLines[eggLineIdx];
            const oldCursor = mainTerminal.querySelector('.term-cursor');
            if (oldCursor) oldCursor.remove();

            const lineDiv = document.createElement('div');
            lineDiv.className = 'line';
            mainTerminal.appendChild(lineDiv);

            if (lineData.type === 'input') {
                lineDiv.innerHTML = '<span class="term-prompt">user@local ~$</span> <span class="term-cmd"></span><span class="term-cursor"></span>';
                const cmdSpan = lineDiv.querySelector('.term-cmd');
                
                function typeChar() {
                    if (eggCharIdx < lineData.text.length) {
                        cmdSpan.innerHTML += lineData.text.charAt(eggCharIdx);
                        eggCharIdx++;
                        mainTerminal.scrollTop = mainTerminal.scrollHeight;
                        setTimeout(typeChar, 40);
                    } else {
                        eggCharIdx = 0;
                        eggLineIdx++;
                        setTimeout(typeEggLine, 800);
                    }
                }
                setTimeout(typeChar, 400);
            } else {
                lineDiv.innerHTML = `<span class="term-ank">${lineData.text}</span><span class="term-cursor"></span>`;
                mainTerminal.scrollTop = mainTerminal.scrollHeight;
                eggLineIdx++;
                setTimeout(typeEggLine, 1800);
            }
        }
        
        // Start typing easter egg
        setTimeout(typeEggLine, 800);
    }

    // Interactive 3D Tilt for Lesson Terminal (Max 10 deg)
    const lessonTerminalMockup = document.querySelector('.terminal-lesson');
    if (lessonTerminalMockup) {
        lessonTerminalMockup.addEventListener('mousemove', (e) => {
            if (window.innerWidth < 1024) return; // Disable on touch/mobile
            const rect = lessonTerminalMockup.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const rotateX = ((y - centerY) / centerY) * -10;
            const rotateY = ((x - centerX) / centerX) * 10;
            lessonTerminalMockup.style.transform = `perspective(1000px) scale(1.02) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
            lessonTerminalMockup.style.transition = 'transform 0.1s ease-out';
        });

        lessonTerminalMockup.addEventListener('mouseleave', () => {
            lessonTerminalMockup.style.transform = 'perspective(1000px) scale(1) rotateX(0deg) rotateY(0deg)';
            lessonTerminalMockup.style.transition = 'transform 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
        });
    }

    // Interactive 3D Tilt for Feature Cards (Max 5 deg)
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            if (window.innerWidth < 1024) return;
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const rotateX = ((y - centerY) / centerY) * -5;
            const rotateY = ((x - centerX) / centerX) * 5;
            card.style.transform = `perspective(1000px) scale(1.02) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
            card.style.transition = 'transform 0.1s ease-out';
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) scale(1) rotateX(0deg) rotateY(0deg)';
            card.style.transition = 'transform 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
        });
    });

    // ==========================================
    // Theme Toggle Logic
    // ==========================================
    const themeToggleBtn = document.getElementById('theme-toggle');
    const sunIcon = document.getElementById('theme-icon-sun');
    const moonIcon = document.getElementById('theme-icon-moon');
    
    // Check saved theme
    const savedTheme = localStorage.getItem('academy_theme') || 'dark';
    if (savedTheme === 'light') {
        document.body.classList.add('theme-light');
        if (sunIcon && moonIcon) {
            sunIcon.style.display = 'none';
            moonIcon.style.display = 'block';
        }
    }
    
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', (e) => {
            
            const toggleLogic = () => {
                document.body.classList.toggle('theme-light');
                const isLight = document.body.classList.contains('theme-light');
                localStorage.setItem('academy_theme', isLight ? 'light' : 'dark');
                
                if (sunIcon && moonIcon) {
                    if (isLight) {
                        sunIcon.style.display = 'none';
                        moonIcon.style.display = 'block';
                    } else {
                        sunIcon.style.display = 'block';
                        moonIcon.style.display = 'none';
                    }
                }
            };

            // Wave Transition API
            if (!document.startViewTransition) {
                toggleLogic();
                return;
            }

            const x = e.clientX;
            const y = e.clientY;
            
            const transition = document.startViewTransition(() => {
                toggleLogic();
            });

            transition.ready.then(() => {
                document.documentElement.animate(
                    {
                        clipPath: [
                            'polygon(0 0, 100% 0, 100% 0, 0 0)',
                            'polygon(0 0, 100% 0, 100% 100%, 0 100%)'
                        ]
                    },
                    {
                        duration: 800,
                        easing: 'ease-in-out',
                        pseudoElement: '::view-transition-new(root)'
                    }
                );
            });
        });
    }

});
