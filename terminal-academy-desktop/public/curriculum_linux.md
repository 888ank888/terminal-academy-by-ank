# Terminal Academy: Linux Core & SysAdmin Skill Tree

This document outlines the curriculum for the **Linux Core & SysAdmin** branch. The curriculum is composed of 20 Nodes, structured hierarchically. Each node contains 15 practical, scenario-based incidents culminating in a Boss Fight. There are no quizzes; the focus is on practical scenarios where things are broken and must be fixed.

## Node 1: Navigation & Basic Commands
**Description:** Surviving the basic shell environment, moving around, and finding things.
**Prerequisites:** None
**Incidents:**
1. Lost in Space: Recover a misplaced critical configuration file using only relative paths.
2. Hidden Treasures: Find the hidden `.secrets` directory in a deeply nested home folder.
3. Broken Alias: Fix a `.bashrc` where `cd` has been aliased to `exit`.
4. The Void: A directory named `-` is causing havoc; remove it without triggering flags.
5. Space Invaders: A directory with spaces in its name contains vital logs; access and read them.
6. Path of Destruction: The `$PATH` variable is wiped out; manually invoke standard tools to fix it.
7. Symbolic Confusion: A symlink loop is crashing a backup script; identify and break the loop.
8. Where am I: The prompt is completely blank and `pwd` is broken; figure out the current directory.
9. History Eraser: The bash history is disabled by default; re-enable it and recover the last commands from memory.
10. Manual Overdrive: `man` is broken; use `info` or `--help` to figure out the syntax for `tar`.
11. Wildcard Chaos: A wildcard expansion accidentally matched thousands of files; isolate the one `config.txt`.
12. Tree Climber: Navigate a directory structure 50 levels deep to find a specific key file.
13. Echo Chamber: `cat` is missing; use `echo` and redirection to read a file.
14. The Invisible Man: A file has no name, just a non-printable character; rename it.
15. **Boss Fight: The Maze Runner** - Escape a chroot jail where standard navigation commands are renamed or missing.

## Node 2: File Management & Archiving
**Description:** Creating, moving, copying, and compressing files under pressure.
**Prerequisites:** Navigation & Basic Commands
**Incidents:**
1. Tar Pit: Extract a `.tar.gz` archive that was corrupted by a missing header.
2. Zip Bomb: A suspicious `.zip` file is filling up the disk; safely extract only the `safe.txt` file.
3. Incomplete Transfer: Resume a broken `rsync` transfer between two local directories without data loss.
4. Copycat: Copy a directory tree but exclude all `.log` files to save disk space.
5. Disk Full: A massive rogue log file is eating all space; find and truncate it without deleting it.
6. Inode Exhaustion: The disk has free space but no free inodes; find and delete the millions of zero-byte files.
7. Fragmented Archive: Combine split archive files (`part1`, `part2`) and extract the payload.
8. The Sticky Move: Attempt to move files from a directory where the sticky bit is misconfigured.
9. Permission Denied: Force copy a file that you only have read access to into a directory you own.
10. Ownership Crisis: Archive a directory while preserving the complex user/group ownerships.
11. Timestamp Forgery: A script relies on file modification times; forge the timestamp of a critical config.
12. Orphaned Symlinks: Find and delete all broken symbolic links in `/etc`.
13. Gzip Corruption: Recover a partially corrupted gzip log file to read the last few lines.
14. Bzip2 Blockade: A backup script is failing because bzip2 runs out of memory; optimize the compression.
15. **Boss Fight: The Data Hoarder** - Migrate a massive, highly fragmented home directory to a new location with zero downtime and exact permissions preserved.

## Node 3: Text Processing & Parsing
**Description:** Slicing and dicing text streams using grep, awk, sed, and more.
**Prerequisites:** Navigation & Basic Commands
**Incidents:**
1. Log Flood: Use `grep` to extract only the critical error messages from a 10GB log file.
2. Sed Surgery: In-place replace all instances of a legacy IP address in 100 config files.
3. Awkward Formatting: Use `awk` to parse a CSV file and sum the values in the 3rd column.
4. Cut the Crap: Extract the 5th field of `/etc/passwd` to get a list of all user names.
5. Sort it Out: Sort a list of IP addresses numerically, not alphabetically.
6. Unique Snowflake: Find the single unique error code in a log of repeated errors.
7. Head to Tail: Extract lines 500 to 600 from a massive database dump without loading it into memory.
8. Regex Rescue: Write a complex regex to match invalid email formats in a user database.
9. Diff Disaster: Read a unified diff and manually apply the patch to a broken script.
10. Trimming the Fat: Use `tr` to convert a DOS-formatted file to Unix format (remove ^M).
11. Column Chaos: Align a messy text file into neat columns using the `column` command.
12. Hex Dumped: Read a binary file using `xxd` to find a plaintext password hidden inside.
13. Grep Inception: Grep for a pattern inside multiple compressed logs (`zgrep`).
14. Sed Delimiter Hell: Fix a sed command that is breaking because the replacement string contains slashes.
15. **Boss Fight: The Log Whisperer** - Parse a disorganized, multi-format server log to reconstruct the exact timeline of a cyber attack.

## Node 4: User & Group Management
**Description:** Managing identities, access, and privilege escalation on a Linux system.
**Prerequisites:** Navigation & Basic Commands
**Incidents:**
1. Locked Out: A developer locked their account; unlock it and reset the password expiry.
2. Ghost User: Find and remove a stealthy backdoor user added to the `wheel` group.
3. Group Conflict: Two departments need access to a shared folder; create the group and add the users.
4. Sudoers Syntax Error: The `/etc/sudoers` file is broken, locking everyone out of root; fix it using `pkexec` or single-user mode.
5. Password Expiry Chaos: All users were set to expire today; globally extend the expiration date by 30 days.
6. UID Clash: Two users have the same UID, causing permission weirdness; resolve the conflict safely.
7. No Home: A user was created without a home directory; create it and populate it with `/etc/skel`.
8. Root SSH: Disable direct root login via SSH but allow a specific admin group to use `su`.
9. The Unkillable User: A user's processes are preventing account deletion; kill the processes and remove the user.
10. Restricted Shell: Trap a junior admin in an `rbash` environment so they can only run `ping` and `ls`.
11. PAM Panic: A misconfigured PAM module is rejecting all logins; boot to rescue mode and bypass it.
12. Shadow Secrets: Identify which users have weak password hashes (e.g., MD5) in `/etc/shadow`.
13. Group Policy: Force all new users to automatically be added to the `docker` group upon creation.
14. Secondary Groups: A user cannot access audio devices; add them to the correct system group without logging out.
15. **Boss Fight: Identity Crisis** - Clean up a compromised system where the attacker has shuffled UIDs, scrambled groups, and hidden root equivalents.

## Node 5: Basic File Permissions
**Description:** Understanding read, write, execute, and ownership fundamentals.
**Prerequisites:** File Management & Archiving, User & Group Management
**Incidents:**
1. Web Root Lockdown: The web server can't read `index.html`; fix the ownership and permissions.
2. Executable Stripped: A critical script lost its execute bit and backups are failing; restore it.
3. Overly Permissive: A private SSH key has 777 permissions and is rejected; secure it.
4. The Unwritable Log: A daemon is crashing because it can't write to `/var/log/app.log`; fix the group owner.
5. Umask Mayhem: New files are being created with 000 permissions; fix the user's `umask`.
6. Shared Directory: Create a directory where group members can read/write, but others are blocked.
7. Octal Confusion: Translate a complex set of symbolic permissions into octal format to fix a provisioning script.
8. Recursive Disaster: Someone ran `chmod -R 777 /etc`; revert the critical files to secure states.
9. Hidden Executables: Find all world-writable executable files in `/tmp` and secure them.
10. Write-Only Drops: Create a 'dropbox' folder where users can write files but not read them.
11. Immutable Nightmare: A file cannot be deleted even by root; remove the `chattr +i` flag.
12. Read-Only Filesystem: The system remounted `/` as read-only; fix the error and remount it rw.
13. Script Sudo: A script needs to run as root, but you can't give the user sudo; use file permissions to solve.
14. Broken Sockets: A MySQL socket file has the wrong permissions, blocking connections.
15. **Boss Fight: The Permission Paradox** - Restore a system where all permissions in `/usr/bin` were randomized, using only built-in shell commands.

## Node 6: Advanced Permissions & ACLs
**Description:** Mastering setuid, setgid, sticky bit, and Access Control Lists.
**Prerequisites:** Basic File Permissions
**Incidents:**
1. SUID Backdoor: Find and neutralize a hidden bash binary with the SUID bit set.
2. SGID Collaboration: Ensure all new files in a shared folder inherit the folder's group ownership.
3. Sticky Situation: Prevent users from deleting each other's files in a shared `/data` directory.
4. ACL Intro: Grant a specific user read access to a file without changing its owner or group.
5. Default ACLs: Ensure all new files in `/var/www/html` automatically grant read access to the `qa` team.
6. ACL Masking: An ACL mask is restricting access despite explicit user rules; fix the mask.
7. Backup Denied: The backup script can't read user directories; use ACLs to grant access without giving root.
8. Stripping ACLs: A migrated directory has lingering ACLs causing issues; strip all ACLs and revert to standard permissions.
9. SUID Fix: `ping` is returning 'Operation not permitted'; restore its missing capabilities or SUID bit.
10. Capabilities vs SUID: Replace a dangerous SUID binary with Linux Capabilities (`setcap`).
11. SGID Executable: Configure a custom tool to run with the privileges of the `network` group.
12. ACL Conflict: A user belongs to a group denied access, but has a user ACL granting access; resolve the evaluation order.
13. The Sticky Deletion: A user bypassed the sticky bit by renaming the parent directory; secure the structure.
14. Getfacl Backup: Back up and restore complex ACLs for a massive file server migration.
15. **Boss Fight: The Access Labyrinth** - Untangle a web of conflicting standard permissions, SGID directories, and complex ACLs to restore access for three separate departments.

## Node 7: Bash Scripting Fundamentals
**Description:** Variables, loops, conditionals, and automating basic tasks.
**Prerequisites:** Text Processing & Parsing
**Incidents:**
1. Variable Void: A script fails because an environment variable is undefined; use default parameter expansion to fix.
2. Infinite Loop: A deployment script is stuck in an infinite `while` loop; identify the missing increment.
3. Conditional Crash: A script deletes `/` if the `$DIR` variable is empty; fix the `if` statement to check for empty strings.
4. For Loop Fiasco: A `for` loop over files with spaces in names is breaking; change the IFS or use globs.
5. Quote Hell: A complex `echo` statement is evaluating variables it shouldn't; fix the single/double quotes.
6. Silent Failure: A script continues running even after a critical command fails; implement `set -e`.
7. Missing Shebang: A script executes as a different shell and fails; add the correct shebang and test.
8. Input Ignored: A script expects arguments but ignores them; use `$1`, `$2`, and `$@` correctly.
9. Math Meltdown: Bash integer arithmetic is failing on decimals; use `bc` within the script.
10. Read-Only Variables: A script tries to overwrite a constant variable and crashes; fix the logic.
11. The Case Statement: Refactor a massive `if-elif-else` block into a clean `case` statement.
12. Redirecting Errors: A script dumps errors to the console; redirect stdout and stderr to separate log files.
13. Prompting for Input: A script needs user confirmation before proceeding; implement `read -p`.
14. Boolean Logic: A complex `&&` and `||` chain is evaluating incorrectly; fix the grouping.
15. **Boss Fight: The Broken Automaton** - Debug and rewrite a 500-line monolithic shell script that handles backups, but fails silently and deletes random files.

## Node 8: Advanced Bash Scripting
**Description:** Functions, arrays, traps, subshells, and robust script design.
**Prerequisites:** Bash Scripting Fundamentals
**Incidents:**
1. Function Scope: Variables in a function are overwriting globals; use `local`.
2. Array Access: A script parses a list of servers into a string instead of an array; fix it to iterate properly.
3. Associative Arrays: Rewrite a dictionary lookup using bash 4+ associative arrays.
4. Trap the Exit: A script leaves temporary files behind when killed; use `trap` to clean up on SIGINT/EXIT.
5. Subshell Surprise: A counter inside a `while read` loop isn't updating outside the loop; fix the pipeline subshell issue.
6. Parallel Execution: A script takes 5 hours to ping servers; run the tasks in parallel using background jobs or `xargs`.
7. Return Codes: A function fails but returns 0; properly pass exit statuses up the call chain.
8. String Manipulation: Use native bash string substitution to rename `.jpeg` files to `.jpg` without `sed`.
9. Here Documents: A script creates a config file with 50 `echo` lines; rewrite it using a `cat <<EOF` block.
10. Command Substitution: A legacy script uses backticks; modernize it to use `$()` and fix nested calls.
11. Debugging Mode: Enable `set -x` to trace why a complex mathematical function is returning the wrong value.
12. Coprocess Communication: Two scripts need to talk to each other; use `coproc` or named pipes (`mkfifo`).
13. Timeout Handling: A network script hangs forever; implement a timeout mechanism.
14. Dynamic Variable Names: Evaluate a variable whose name is stored in another variable (indirect expansion).
15. **Boss Fight: The CI/CD Pipeline** - Write a robust, idempotent bash framework that handles logging, error trapping, parallel execution, and dry-runs for a deployment system.

## Node 9: Process Management
**Description:** Monitoring, managing, and killing processes and interpreting signals.
**Prerequisites:** None
**Incidents:**
1. Zombie Apocalypse: The process table is full of zombies; find the parent process and restart it.
2. Runaway Process: A crypto-miner is eating 100% CPU; find it, pause it (`SIGSTOP`), and kill it (`SIGKILL`).
3. Orphaned Daemons: A web server crashed, but its worker processes are still holding the port; terminate them.
4. Priority Inversion: A backup job is starving the database; use `renice` to lower its priority.
5. The Unkillable: A process is stuck in Uninterruptible Sleep (D state); diagnose the I/O bottleneck.
6. Signal Trapping: A daemon needs to reload its config without restarting; send it a `SIGHUP`.
7. Process Tree: `ps aux` is too messy; use `htop` or `pstree` to visualize the relationship between crashing workers.
8. Memory Leak: A Java process is consuming all RAM, triggering the OOM Killer; analyze `dmesg` to confirm.
9. Strace the Silent: A custom script hangs silently; use `strace` to see what system call it's waiting on.
10. Lsof Lockdown: A process holds a lock on a deleted file, consuming disk space; use `lsof` to find and restart it.
11. Context Switching: A system is slow despite low CPU usage; diagnose high context switches and interrupts.
12. Cgroup Limits: A container is using too much memory; manually inspect its cgroup limits.
13. Background Jobs: A user logged out and their long-running script died; explain `nohup` and `screen`/`tmux`.
14. Fork Bomb: A user accidentally executed a fork bomb; recover the system without rebooting.
15. **Boss Fight: The Ghost in the Machine** - Isolate and terminate a rootkit that intercepts `ps` and `top` commands to hide itself, using raw `/proc` inspection.

## Node 10: Background Jobs & Scheduling
**Description:** Cron, at, systemd timers, and terminal multiplexers.
**Prerequisites:** Bash Scripting Fundamentals, Process Management
**Incidents:**
1. Cron Syntax Crash: A backup runs every minute instead of once a day; fix the crontab syntax.
2. Missing Environment: A script runs perfectly manually but fails in cron; fix the `$PATH` issue in the crontab.
3. Spamming Root: A cron job is sending thousands of emails to root; redirect its output to `/dev/null`.
4. The One-Off Job: A task needs to run at 3 AM tonight only; schedule it using `at`.
5. Tmux Recovery: An SSH session dropped during a critical database migration; reattach to the running `tmux` session.
6. Anacron Delays: A laptop missed its midnight cron jobs; configure `anacron` to run them upon boot.
7. Systemd Timer Migration: Convert a flaky, complex cron job into a robust systemd timer.
8. Nohup Output: A `nohup` script is writing to a massive `nohup.out` file; redirect it properly.
9. Job Control: You accidentally started `vim` in the background; bring it to the foreground (`fg`).
10. Cron Access: A developer cannot edit their crontab; fix the `/etc/cron.allow` or `cron.deny` files.
11. Timezone Trouble: Cron is running jobs in UTC, but the server is in EST; align the timezones.
12. Overlapping Cron: A long-running cron job is stepping on its own toes; implement `flock` to prevent overlap.
13. System Cron vs User Cron: Move scripts from `/etc/cron.daily` to a specific user's crontab.
14. Screen Detachment: Use `screen` to share a terminal session live with a remote admin for debugging.
15. **Boss Fight: The Temporal Anomaly** - Fix a chaotic server where dozens of conflicting cron jobs, at jobs, and systemd timers are causing rolling outages every hour.

## Node 11: Package Management & Repositories
**Description:** Installing, updating, and repairing software via apt/dpkg or yum/rpm.
**Prerequisites:** Process Management
**Incidents:**
1. Broken Dependencies: `apt-get upgrade` fails due to unmet dependencies; force a fix and repair the dpkg database.
2. Repository 404: The system is trying to pull packages from a dead repository URL; update `/etc/apt/sources.list`.
3. GPG Key Expired: Cannot install packages because the repository signing key expired; fetch and add the new key.
4. Held Packages: A critical security update won't install because a package is marked as 'hold'; unhold it.
5. Rogue Package: Find out which package installed a specific bizarre binary in `/usr/sbin`.
6. Downgrade Disaster: A new version of a web server breaks the site; downgrade the package to the previous version.
7. Orphan Cleanup: The root partition is full; use `apt autoremove` and clear the package cache safely.
8. RPM Rebuild: The RPM database is corrupted and `yum` is hanging; rebuild the RPM database.
9. Source Compilation: A package isn't in the repos; download the source, `./configure`, `make`, and `make install` it.
10. Deb Creation: Wrap a custom bash script into a simple `.deb` package for easy distribution.
11. Yum History: Roll back a botched `yum update` transaction that broke the database server.
12. Extracting Contents: Extract a `.deb` or `.rpm` file without installing it to inspect its contents.
13. Pinning Packages: Configure apt preferences to always prefer a package from a specific PPA.
14. Missing Shared Object: A binary fails complaining about a missing `.so` file; locate and install the missing library package.
15. **Boss Fight: Dependency Hell** - Untangle a server where mixing unstable repositories with stable ones has completely shattered the package manager.

## Node 12: Service Management (Systemd Basics)
**Description:** Starting, stopping, and logging daemons with systemctl and journalctl.
**Prerequisites:** Package Management & Repositories, Process Management
**Incidents:**
1. Dead Daemon: Nginx won't start; check the status and read the immediate error output.
2. Journal Diving: Use `journalctl` to find why SSH failed to start at boot, filtering by time and service.
3. Masked Unit: A service refuses to start because it is 'masked'; unmask and enable it.
4. Boot Loop: A crashing service is bringing down the server on boot; boot into emergency mode and disable it.
5. Persistent Logs: `journalctl` logs vanish on reboot; configure systemd-journald to persist logs to disk.
6. Dependency Failure: A web app is starting before the database, causing it to fail; fix the start order.
7. Hanging Stop: A service hangs for 90 seconds when stopping; kill it immediately and adjust its timeout.
8. Service Not Found: A legacy init.d script isn't recognized by systemctl; enable it manually.
9. Reload vs Restart: A config changed; safely reload a service without dropping active connections.
10. Journal Size Limit: Systemd logs are eating 50GB of disk space; vacuum the journal to 1GB.
11. Unit File Override: Edit a system unit file without modifying the `/lib/systemd` original (use `systemctl edit`).
12. Target Confusion: The server boots to a GUI instead of CLI; change the default systemd target.
13. Socket Activation: A service only starts when it receives traffic on a specific port; troubleshoot the systemd socket.
14. Chroot Service: Start a service inside a specific chroot environment using systemd.
15. **Boss Fight: The Silent Failure** - A critical daemon crashes instantly with no errors in standard logs; use advanced journalctl filters, strace, and unit overrides to find the cause.

## Node 13: Advanced Systemd
**Description:** Writing custom units, timers, mounts, and resource controls.
**Prerequisites:** Service Management (Systemd Basics)
**Incidents:**
1. Custom Daemon: Write a basic `my_app.service` unit file to run a Python script as a daemon.
2. Watchdog Trigger: A custom service occasionally freezes; implement systemd `WatchdogSec` to auto-restart it.
3. Environment Variables: A service needs specific API keys; inject them via `EnvironmentFile` securely.
4. Path Activation: Configure a systemd path unit to trigger a script whenever a specific file is modified.
5. Automount: Convert an `/etc/fstab` network mount into a systemd automount unit for better boot performance.
6. Drop-in Hell: Multiple systemd drop-in files (`override.conf`) are conflicting; consolidate and fix them.
7. Resource Limits: A memory-leaky app is crashing the server; use systemd `MemoryLimit` to restrict it.
8. Hardening Services: Secure a custom service using `ProtectSystem=strict` and `ProtectHome=read-only`.
9. User Services: Configure a service to run entirely within a standard user's session (`systemctl --user`).
10. Multi-Instance Services: Create a template unit (`app@.service`) to run multiple instances of a daemon on different ports.
11. Boot Performance: Use `systemd-analyze blame` to identify and fix a 3-minute slow boot time.
12. Slice Configuration: Move a heavy backup service into a low-priority systemd slice to save CPU for the web server.
13. Failure Notifications: Configure a service to trigger an alert script (`OnFailure=`) if it crashes.
14. Transient Services: Run a temporary, one-off background task using `systemd-run`.
15. **Boss Fight: The Orchestrator** - Replace an entire messy init script system with a clean, dependency-aware suite of systemd targets, services, and timers for a multi-tier application.

## Node 14: Storage Management & Partitioning
**Description:** Fdisk, mkfs, mount, and taming /etc/fstab.
**Prerequisites:** File Management & Archiving
**Incidents:**
1. Lost Partition: A partition table was accidentally wiped; recover the boundaries using `testdisk` or `parted`.
2. Filesystem Corruption: An ext4 filesystem is unmountable due to a bad superblock; run `fsck` with a backup superblock.
3. Fstab Crash: A typo in `/etc/fstab` is dropping the system into emergency mode on boot; fix the syntax.
4. UUID Mismatch: A disk was cloned, but the system won't boot because the UUIDs changed; update grub and fstab.
5. Mount Point Busy: Cannot unmount a USB drive because 'target is busy'; use `fuser` to kill the blocking processes.
6. Swap Exhaustion: The server is out of memory and has no swap; create, format, and activate a swapfile.
7. Expanding Partitions: A cloud VM disk was resized; use `growpart` and `resize2fs` to expand the filesystem online.
8. Read-Only Mount: A failing disk automatically remounted as read-only; diagnose the hardware errors in `dmesg`.
9. XFS Repair: An XFS filesystem is corrupted; use `xfs_repair` to fix it, bypassing standard fsck.
10. Bind Mounts: Expose `/var/www/html` to a user's home directory securely using a bind mount.
11. Loopback Devices: Mount a raw `.img` file as a loop device to extract its contents.
12. Disk Quotas: A user is using too much space; enable and enforce disk quotas on the `/home` partition.
13. Inode Deletion: A partition is 100% full of tiny files; bypass standard `rm` limits to clear it out.
14. Bad Sectors: A disk is throwing read errors; map out the bad blocks using `badblocks`.
15. **Boss Fight: The Disk Juggler** - Migrate a live root filesystem to a new, larger disk with a different partition layout, without shutting down the primary services.

## Node 15: Logical Volume Management (LVM)
**Description:** Abstracting storage for flexible sizing and snapshots.
**Prerequisites:** Storage Management & Partitioning
**Incidents:**
1. Volume Full: The `/var` logical volume is full; extend it dynamically using free space in the volume group.
2. VG Expansion: The Volume Group has no free space; add a new physical disk and extend the VG.
3. Snapshot Creation: Take an LVM snapshot of a database volume, mount it, and run a backup without locking the DB.
4. Snapshot Overflow: An LVM snapshot ran out of space and corrupted itself; remove it and fix the origin volume.
5. LV Reduction (Danger): Shrink the `/home` LV to make room for `/root`; execute the fs resize and LV reduce carefully.
6. Missing PV: A disk in the VG failed; remove the missing physical volume from the LVM metadata.
7. LVM on RAID: Configure LVM on top of a software RAID (mdadm) array for redundancy.
8. Metadata Corruption: The LVM configuration is wiped; restore the VG metadata from `/etc/lvm/archive`.
9. Thin Provisioning: Create a thin pool and provision several thin LVs for virtual machines.
10. Thin Pool Overcommit: A thin pool has run out of actual physical space; add storage before data loss occurs.
11. LV Renaming: Rename a volume group and logical volume to match new naming conventions without breaking fstab.
12. Stale Device Nodes: `dmsetup` is showing orphaned LVM device mapper entries; clean them up.
13. LVM Cache: Add a fast NVMe drive as a caching layer to a slow HDD logical volume.
14. Mirroring LVs: Convert a standard LV into a mirrored LV across two physical volumes.
15. **Boss Fight: The Data Rescue** - A heavily fragmented LVM setup spanning 4 disks lost a physical volume; salvage the remaining logical volumes and rebuild the array.

## Node 16: Network Configuration Basics
**Description:** IP addressing, interfaces, and DNS using iproute2 and Netplan.
**Prerequisites:** Navigation & Basic Commands
**Incidents:**
1. Lost IP: The server lost its IP address; manually assign one using `ip addr` and bring the interface up.
2. Default Gateway Gone: Cannot reach the internet; check `ip route` and add the missing default gateway.
3. DNS Blackout: Pings to IPs work, but names fail; fix the `/etc/resolv.conf` or systemd-resolved config.
4. Netplan Nightmare: A syntax error in a YAML Netplan file broke networking; fix the spacing and apply.
5. NetworkManager Conflict: Two tools are fighting for control of the same interface; disable one.
6. MAC Spoofing: Change the MAC address of an interface temporarily to bypass a network restriction.
7. VLAN Tagging: The server needs to communicate on VLAN 50; configure the 802.1q interface.
8. Static to DHCP: Switch an interface from static to DHCP without rebooting.
9. MTU Mismatch: Packets are dropping over a VPN; troubleshoot and adjust the MTU of the interface.
10. Link Speed Negotiation: An interface is auto-negotiating to 10Mbps half-duplex; force it to 1Gbps full-duplex using `ethtool`.
11. Multiple IPs: Assign a secondary IP alias to a single network interface for a new web service.
12. ARP Poisoning: The server has the wrong MAC address for the gateway in its ARP cache; flush it.
13. IPv6 Conflicts: IPv6 is causing weird routing issues; disable IPv6 system-wide via sysctl.
14. Proxy Problems: `curl` commands are failing because the system proxy variables are misconfigured.
15. **Boss Fight: The Disconnected Server** - Gain access to a headless server through a serial console and rebuild the entire broken network stack from scratch using only raw `ip` commands.

## Node 17: SSH Configuration & Security
**Description:** Key management, config hardening, and port forwarding.
**Prerequisites:** Network Configuration Basics, User & Group Management
**Incidents:**
1. Lost Key: You lost your private key; recover access using an alternative emergency backdoor.
2. Permission Denied (publickey): SSH is rejecting a valid key because the home directory permissions are wrong; fix `.ssh/`.
3. Root Login Enabled: Secure the `sshd_config` to disable root login and password authentication.
4. Port 22 Blocked: The ISP blocks port 22; reconfigure SSH to listen on port 443.
5. Local Port Forwarding: Access an internal database (port 5432) securely via an SSH tunnel.
6. Remote Port Forwarding: Expose your local development web server to the public internet via a remote SSH server.
7. Dynamic Forwarding (SOCKS): Set up an SSH SOCKS proxy to browse the internet securely through the server.
8. Key Passphrase: Remove the passphrase from an old legacy SSH key for use in an automated script.
9. Agent Forwarding: Use `ssh-agent` to hop through a bastion host to a private server without copying keys.
10. SSH Multiplexing: Configure `~/.ssh/config` to use multiplexing to speed up multiple connections.
11. Stale Sessions: SSH sessions are dropping frequently; configure `ClientAliveInterval` to keep them alive.
12. Brute Force Attack: The server is being hammered; implement `Fail2Ban` or SSH rate limiting.
13. Host Key Changed: A man-in-the-middle warning appears because a server was rebuilt; clear the old `known_hosts` entry.
14. Jump Hosts: Configure `ProxyJump` in the SSH config to cleanly access a deeply nested internal server.
15. **Boss Fight: The Bastion Breach** - Secure a heavily compromised SSH jump server by implementing MFA, key-only access, strict chroots, and comprehensive audit logging.

## Node 18: Firewall Basics (UFW & Iptables)
**Description:** Filtering traffic, opening ports, and locking down servers.
**Prerequisites:** Network Configuration Basics
**Incidents:**
1. Locked Out via UFW: You accidentally denied port 22 and locked yourself out; fix it from the console.
2. Allow Specific IP: Configure UFW to allow MySQL connections only from the web server's IP.
3. Iptables Drop All: Change the default iptables policy to DROP and manually allow SSH, HTTP, and HTTPS.
4. Rule Ordering: An allow rule is being ignored because a drop rule comes first; reorder the iptables rules.
5. Logging Dropped Packets: Enable iptables logging to diagnose why a custom application is failing to connect.
6. Rate Limiting: Use iptables `limit` module to prevent ICMP ping floods.
7. Flush Disaster: Someone ran `iptables -F` and broke everything; restore the rules from a backup file.
8. Docker Firewall Conflict: Docker is bypassing UFW rules; configure iptables specifically in the `DOCKER-USER` chain.
9. Persistent Rules: Iptables rules disappear on reboot; install and configure `iptables-persistent`.
10. Port Knocking: Set up a simple port knocking sequence to open SSH only when a secret pattern is received.
11. IPv6 Leaks: UFW is configured for IPv4, but IPv6 traffic is completely open; secure `ip6tables`.
12. Stateful Inspection: Allow incoming traffic only if it is part of an `ESTABLISHED` or `RELATED` connection.
13. Reject vs Drop: Change a silent DROP rule to a REJECT rule to speed up application failure handling.
14. Custom Chains: Create a custom iptables chain to group rules for a specific VPN interface.
15. **Boss Fight: The Siege** - Defend against an active, multi-vector DDoS attack using complex iptables rate-limiting, geo-blocking, and fail2ban integration.

## Node 19: Advanced Networking & Routing
**Description:** NAT, IP forwarding, bridges, and static routing.
**Prerequisites:** Firewall Basics (UFW & Iptables)
**Incidents:**
1. NAT Gateway: Configure a server to act as a NAT router for an internal network using `iptables MASQUERADE`.
2. Port Forwarding (DNAT): Forward incoming traffic on port 80 to an internal backend server on port 8080.
3. IP Forwarding Disabled: The NAT rules are right, but traffic won't pass; enable `net.ipv4.ip_forward` in sysctl.
4. Static Route: The server cannot reach a specific subnet; add a permanent static route using `ip route`.
5. Source Routing: Traffic from two ISPs is returning on the wrong interface; use `ip rule` to configure policy routing.
6. Bridge Network: Create a Linux bridge interface (`br0`) and attach physical and virtual interfaces to it.
7. Hairpin NAT: Internal users cannot access an internal web server using its public IP; configure NAT loopback.
8. Dummy Interfaces: Create a `dummy0` interface to bind multiple services to a single logical IP.
9. Anycast IP: Configure loopback interfaces on multiple servers for anycast load balancing.
10. GRE Tunnel: Establish a GRE tunnel between two data centers and route specific traffic over it.
11. WireGuard VPN: Set up a basic point-to-point WireGuard tunnel and verify handshakes.
12. TCP Dump: Use `tcpdump` to capture packets on a specific port and save them to a `.pcap` for Wireshark analysis.
13. Asymmetric Routing: Packets are dropping because they leave via `eth0` but return via `eth1`; disable rp_filter.
14. Traffic Shaping: Use `tc` (traffic control) to throttle outbound bandwidth on a specific interface.
15. **Boss Fight: The Network Architect** - Build a complete, functional virtual router connecting 3 subnets, complete with NAT, strict firewalling, and static routes, purely from the command line.

## Node 20: System Troubleshooting & Log Analysis
**Description:** Putting it all together to debug kernel panics, OOMs, and complex failures.
**Prerequisites:** Advanced Bash Scripting, Advanced Systemd, Advanced Networking & Routing
**Incidents:**
1. The OOM Killer: The system randomly kills processes; analyze `/var/log/messages` or `dmesg` to find the culprit.
2. Kernel Panic: The system hangs on boot with a kernel panic; boot with `nomodeset` or an older kernel to fix the driver issue.
3. High Load, Low CPU: The load average is 50 but CPU usage is 2%; diagnose a massive I/O wait issue.
4. Syscall Tracing: A proprietary binary crashes instantly; use `strace` to find a missing configuration file.
5. Network Dropping: Connections drop intermittently; use `mtr` and `ss` to identify a routing loop or port exhaustion.
6. File Descriptor Exhaustion: 'Too many open files' error; increase limits via `ulimit` and `/etc/security/limits.conf`.
7. Core Dumps: Enable and analyze a core dump using `gdb` to see why a C program segfaulted.
8. Auditd Tracing: Use `auditd` to track exactly which user is modifying a secure configuration file.
9. Slow DNS Resolution: Every ssh connection takes 30 seconds; fix the reverse DNS lookup issue in SSH or `resolv.conf`.
10. Disk Latency: Use `iostat` and `iotop` to find the specific process thrashing the disk.
11. Memory Leaks: Differentiate between cached memory and actual RAM usage using `free` and `vmstat`.
12. Corrupt Glibc: A botched update broke `glibc`, rendering most commands unusable; recover using a statically linked busybox.
13. Sysctl Tuning: The server is dropping massive amounts of syn packets; tune TCP syn backlogs in `sysctl.conf`.
14. Zombie Network Connections: The server has 10,000 connections in `TIME_WAIT`; tune TCP reuse/recycle parameters.
15. **Boss Fight: The Kobayashi Maru** - A highly realistic, multi-layered outage where DNS is broken, the disk is full, the database is corrupt, and a runaway script is fork-bombing the system. Diagnose and fix the root causes in the correct order to restore service.
