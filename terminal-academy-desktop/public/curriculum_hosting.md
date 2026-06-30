# Terminal Academy Skill Tree: Game Servers & App Hosting

> [!NOTE]
> **Domain Overview:** This branch of the Terminal Academy focuses on deploying, securing, and maintaining game servers (Minecraft) and web applications. It emphasizes practical incident response, system administration, reverse proxies, and database management.

---

## Node 1: Linux Service Management (systemd)
**Dependencies:** None

### Syllabus (Practical Incidents)
1. **Crash Course:** Start a crashed service that failed silently.
2. **Boot Loader:** Enable a critical background service on boot.
3. **Journal Reader:** Parse `journalctl` to find why a service failed to initialize.
4. **The Architect:** Write a basic `.service` file from scratch for a dummy script.
5. **Syntax Sleuth:** Fix a syntax error in a broken unit file.
6. **Permission Denied:** Change service user permissions to stop a service running as root.
7. **Patience Tester:** Override systemd timeouts for a slow-starting game server.
8. **Tick Tock:** Set up a `systemd` timer to replace a legacy cron job.
9. **Ghost Links:** Fix broken symlinks in `/etc/systemd/system/`.
10. **The Conflict:** Mask a default service that is conflicting with a custom installation.
11. **Memory Warden:** Restrict a memory-leaking service using cgroups.
12. **Ghost Process:** Fix "Address already in use" by finding and killing the orphan process.
13. **Reload Required:** Successfully apply changes without restarting the server via daemon-reload.
14. **Boot Analyzer:** Analyze boot time (`systemd-analyze`) and disable a heavy, unneeded service.
15. **The Prison:** Create a simple chroot environment for a highly vulnerable service.

**Boss Fight:** Rescue a completely borked game server systemd configuration where the startup script is stuck in a crash loop, logging is silent, and permissions are ruined. 

---

## Node 2: Hosting Security Essentials (UFW & Fail2Ban)
**Dependencies:** None

### Syllabus (Practical Incidents)
1. **Lockout Prevention:** Enable UFW without locking yourself out of your active SSH session.
2. **The Gates Open:** Allow Minecraft port 25565 through a default-deny firewall.
3. **The Banhammer:** Block a specific noisy IP spamming the server.
4. **Broken Web:** Fix a misconfigured rule that is silently dropping all web traffic.
5. **Forwarding:** Set up port forwarding via UFW `before.rules`.
6. **Watchdog Install:** Install Fail2Ban and verify the service is running.
7. **Custom Jail:** Configure a custom SSH jail with a strict 3-strike policy.
8. **False Positive:** Unban a falsely banned administrator IP via `fail2ban-client`.
9. **Regex Repair:** Fix a Fail2Ban filter regex that isn't matching a new custom app log format.
10. **Rate Limiting:** Limit connections per IP in UFW to prevent basic brute-forcing.
11. **App Profiles:** Create and apply an application profile for UFW.
12. **Log Diver:** View and interpret dropped packet logs in `/var/log/ufw.log`.
13. **SYN Flood Defense:** Defend against a simulated SYN flood using UFW limit rules.
14. **The VIP Lounge:** Whitelist an entire management subnet.
15. **IPv6 Chaos:** Fix UFW failing to load due to broken IPv6 configurations.

**Boss Fight:** Defend against an active brute-force and DDoS simulation on multiple ports by configuring strict UFW limits and Fail2Ban jails under a severe time limit.

---

## Node 3: Nginx Fundamentals
**Dependencies:** Node 1

### Syllabus (Practical Incidents)
1. **First Contact:** Install and start Nginx, verifying the default page.
2. **Static Drop:** Serve a custom static HTML file from a new directory.
3. **Forbidden City:** Fix a 403 Forbidden error caused by bad directory permissions.
4. **Port Shift:** Change the default listening port from 80 to 8080.
5. **Semicolon Assassin:** Fix a critical syntax error in `nginx.conf` preventing startup.
6. **Custom 404:** Create and map a custom 404 error page.
7. **The Bouncer:** Configure basic authentication (`htpasswd`) for a private directory.
8. **File Browser:** Enable and format `autoindex` to serve a directory of files.
9. **Spam Filter:** Implement rate limiting (`limit_req`) to stop a basic HTTP flood.
10. **Hidden Secrets:** Deny access to hidden `.git` directories globally.
11. **Log Parser:** Read and parse Nginx access logs using `awk` to find the top requester.
12. **Worker Exhaustion:** Fix a "Worker Connections" limit error under load.
13. **Shrink Wrap:** Enable Gzip compression to reduce payload sizes.
14. **Core Alignment:** Configure worker processes to automatically match CPU cores.
15. **The Redirect:** Redirect all `www` traffic to `non-www` seamlessly.

**Boss Fight:** Repair an Nginx server returning a mix of 500s and 403s. You must fix user permissions, restore the correct root directory, and block a bad bot scraping the site.

---

## Node 4: Apache HTTPD Basics
**Dependencies:** Node 1

### Syllabus (Practical Incidents)
1. **Clash of Titans:** Install Apache and resolve a port conflict with an existing Nginx instance.
2. **Basic Serve:** Serve a basic site out of a custom `DocumentRoot`.
3. **Module Master:** Enable `mod_rewrite` and verify it loads.
4. **The Broken Rule:** Fix a broken `.htaccess` file causing a global 500 Internal Server Error.
5. **Custom Ink:** Configure a custom log format to capture execution times.
6. **Index Config:** Set up directory listing but exclude specific file types.
7. **IP Restrictor:** Restrict directory access to a single internal IP.
8. **Listener:** Change the global `Listen` directive to bind to a specific interface.
9. **SELinux/AppArmor Block:** Fix a permission issue causing "Forbidden" when serving outside `/var/www`.
10. **KeepAlive Tune:** Enable KeepAlive and tune the timeout for a high-latency network.
11. **Silent Server:** Disable the ServerSignature to hide Apache version info.
12. **User Swap:** Configure Apache to run as a specific restricted user.
13. **Auth Prompt:** Set up a basic auth prompt using `.htpasswd`.
14. **Missing Link:** Analyze `error.log` to identify and install a missing PHP module.
15. **The Alias:** Set up an Alias directory to map a URL path to a different filesystem path.

**Boss Fight:** Migrate a legacy PHP application's messy `.htaccess` routing into a clean, performant VirtualHost configuration while fixing broken file permissions across the board.

---

## Node 5: PostgreSQL Fundamentals
**Dependencies:** Node 1

### Syllabus (Practical Incidents)
1. **First Query:** Install Postgres and connect via the default `psql` shell.
2. **Amnesia:** Reset the forgotten `postgres` superuser password via single-user mode.
3. **New Tenant:** Create a new user, a new database, and grant ownership.
4. **Local Block:** Fix `pg_hba.conf` which is currently blocking local socket connections.
5. **Distant Shores:** Allow remote connections by editing `postgresql.conf` and `pg_hba.conf`.
6. **The Bad Dump:** Import a broken `.sql` dump by skipping errors or fixing the syntax.
7. **Assassin:** Find and gracefully kill a deadlocked, long-running query.
8. **Space Invader:** Query the system catalogs to find the size of all databases and tables.
9. **Strict Access:** Grant specific table permissions to a read-only reporting user.
10. **Too Many Cooks:** Fix a "too many clients" error by increasing `max_connections`.
11. **Migration:** Safely change the default Postgres data directory to a new drive.
12. **Log Detective:** Read PostgreSQL logs to identify exactly which query is failing.
13. **Data Exfil:** Export specific table data to a CSV file directly from `psql`.
14. **Buffer Tune:** Tune `shared_buffers` appropriately for a 2GB RAM server.
15. **Ghost Login:** Setup a `.pgpass` file for automated scripts to log in without prompts.

**Boss Fight:** Rescue a corrupted database configuration where remote connections fail, the superuser is locked out, and a rogue background query is eating 100% CPU.

---

## Node 6: Redis In-Memory Datastore
**Dependencies:** Node 1

### Syllabus (Practical Incidents)
1. **Quick Start:** Install, start Redis, connect via `redis-cli`, and ping the server.
2. **Lockdown:** Set a password (`requirepass`) and authenticate.
3. **Remote Access:** Fix a Redis instance binding only to localhost when a remote app needs it.
4. **Port Change:** Change the default port from 6379 to a custom port.
5. **Snapshot Setup:** Configure RDB persistence to save every 60 seconds if 10 keys change.
6. **MISCONF Error:** Fix a "MISCONF Redis is configured to save RDB snapshots" error caused by bad permissions.
7. **Append Only:** Enable AOF (Append Only File) persistence and verify the file is created.
8. **Surgical Flush:** Flush a specific logical database without wiping the entire server.
9. **Live Monitor:** Use `redis-cli monitor` to identify which app is spamming a specific key.
10. **Memory Cap:** Set a strict memory limit (`maxmemory`) to prevent OOM crashes.
11. **Eviction Notice:** Configure an eviction policy (`allkeys-lru`) when the memory cap is hit.
12. **Rename Danger:** Rename dangerous commands like `FLUSHALL` in `redis.conf`.
13. **Metrics Check:** Use `INFO` to check cache hit/miss ratios and memory fragmentation.
14. **AOF Rewrite:** Manually trigger a background rewrite of an overgrown AOF file.
15. **Pipeline Test:** Feed a massive list of commands to Redis using pipe mode.

**Boss Fight:** Secure a completely open Redis instance that is actively being manipulated by an external bot, implement strict memory limits, and restore lost critical data from an RDB backup.

---

## Node 7: Vanilla Java Minecraft Server
**Dependencies:** Node 1

### Syllabus (Practical Incidents)
1. **Java Drop:** Install the correct Headless JRE version for the target Minecraft version.
2. **The Jar:** Download the official `server.jar` and run it for the first time.
3. **Legal Bind:** Accept the EULA via CLI without using a text editor (e.g., `sed` or `echo`).
4. **Memory Allocation:** Allocate specific RAM pools using JVM flags (`-Xmx` and `-Xms`).
5. **OOM Crash:** Diagnose and fix an "Out of Memory" crash loop.
6. **Port Config:** Change the default port in `server.properties` to host a second server.
7. **Authentication:** Toggle online-mode to allow or deny cracked clients.
8. **Color MOTD:** Update the Server MOTD using standard Minecraft color codes in the properties file.
9. **The List:** Whitelist a player manually via the terminal.
10. **Admin Grant:** Op a player directly via the console interface.
11. **Corrupted World:** Fix a corrupted `level.dat` by replacing it with `level.dat_old`.
12. **Start Script:** Write a robust `start.sh` script to handle reboots.
13. **Daemonize:** Run the server safely in a `tmux` or `screen` session.
14. **Auto Reboot:** Schedule daily automatic restarts using a bash script and cron.
15. **Crash Reader:** Interpret a dense crash report to find the root cause (e.g., ticking entity) and remove it.

**Boss Fight:** Recover a crashed Minecraft server where the world is corrupted, memory is heavily constrained, and the start script is failing to attach to `tmux`.

---

## Node 8: Nginx Reverse Proxy & Load Balancing
**Dependencies:** Node 3

### Syllabus (Practical Incidents)
1. **Basic Proxy:** Proxy traffic to a local NodeJS app running on port 3000.
2. **Bad Gateway:** Diagnose and fix a "502 Bad Gateway" error.
3. **Real IP:** Pass the real client IP to the backend using `X-Forwarded-For`.
4. **WebSocket Upgrade:** Proxy websockets successfully by upgrading the connection headers.
5. **Upstream Block:** Set up an `upstream` block targeting two separate backend servers.
6. **Round Robin:** Configure basic round-robin load balancing.
7. **Sticky Sessions:** Configure IP-hash load balancing for an app that requires session affinity.
8. **Maintenance Mode:** Mark a backend server as 'down' in the upstream block.
9. **Payload Too Large:** Fix an issue with large file uploads by adjusting `client_max_body_size`.
10. **Proxy Cache:** Cache reverse proxy responses to reduce backend load.
11. **Bypass Cache:** Configure rules to bypass the proxy cache for logged-in users via cookies.
12. **Stale Serve:** Serve stale cached content if the backend goes down (`proxy_cache_use_stale`).
13. **Timeout Tweaks:** Set proxy timeouts to prevent 504 Gateway Timeouts on long requests.
14. **Path Rewrite:** Rewrite URL paths before passing them to the backend proxy.
15. **Custom Headers:** Inject custom headers into the proxy response for the client.

**Boss Fight:** Load balance traffic across three broken backend apps. You must diagnose which one is returning 500s, fix dropped WebSockets, and set up caching to survive a sudden traffic spike.

---

## Node 9: Apache Virtual Hosts & .htaccess
**Dependencies:** Node 4

### Syllabus (Practical Incidents)
1. **First VHost:** Create a VirtualHost configuration for a brand new domain.
2. **Routing Chaos:** Fix a routing issue where all traffic goes to the default VirtualHost.
3. **Alias Match:** Setup `ServerAlias` to handle `www` and `non-www` traffic identically.
4. **Site Manager:** Use `a2ensite` and `a2dissite` to cleanly manage active sites.
5. **Alt Root:** Configure a `DocumentRoot` that lives in `/home/user/public_html`.
6. **HTTPS Redirect:** Write an `.htaccess` rule to force redirect HTTP to HTTPS.
7. **Directory Shield:** Password protect a single directory within a VirtualHost.
8. **Agent Block:** Block a specific malicious `User-Agent` string via `.htaccess`.
9. **Custom Errors:** Set up custom ErrorDocuments for 403, 404, and 500 errors.
10. **Clean URLs:** Rewrite URLs to silently remove `.php` extensions.
11. **Infinite Loop:** Fix an `.htaccess` redirect loop (ERR_TOO_MANY_REDIRECTS).
12. **CORS Config:** Enable and configure CORS headers for an API endpoint.
13. **Subdomain Mapping:** Map a subdomain to a specific internal subfolder.
14. **Index Priority:** Set the directory index priority (e.g., `index.php` over `index.html`).
15. **Log Separation:** Configure separate access and error logs per VirtualHost.

**Boss Fight:** Fix a multi-tenant Apache server where three domains are cross-routing incorrectly, `.htaccess` overrides are completely ignored by the master config, and one domain is stuck in an infinite redirect loop.

---

## Node 10: Web Server SSL/TLS (Certbot)
**Dependencies:** Node 8, Node 9

### Syllabus (Practical Incidents)
1. **Standalone Cert:** Install Certbot and obtain a standalone cert (port 80 must be free).
2. **Nginx Plugin:** Obtain and auto-install a cert using the Nginx Certbot plugin.
3. **Apache Plugin:** Obtain and auto-install a cert using the Apache Certbot plugin.
4. **DNS Mismatch:** Fix a failed challenge caused by a DNS A-record pointing to the wrong IP.
5. **Port Block:** Fix a failed challenge because port 80 is blocked by UFW.
6. **Force SSL:** Verify and fix HTTP to HTTPS redirection post-installation.
7. **HSTS Setup:** Configure Strict-Transport-Security (HSTS) headers.
8. **Protocol Purge:** Disable outdated and insecure TLS 1.0 and TLS 1.1 protocols.
9. **Cipher Hardening:** Configure modern, strong cipher suites.
10. **Manual Renew:** Manually trigger a renewal for an expired certificate.
11. **Cron Fix:** Fix a systemd timer / cron job that silently failed to renew certs.
12. **Revocation:** Revoke a compromised certificate properly.
13. **Wildcard DNS:** Set up a wildcard certificate using the DNS TXT challenge.
14. **Self-Signed:** Generate and install a custom self-signed certificate for internal use.
15. **Mixed Content:** Identify and fix "Mixed Content" errors by enforcing secure asset loading.

**Boss Fight:** Secure a legacy web server hosting multiple domains by updating vulnerable ciphers, fixing a broken wildcard certificate via DNS challenge, and resolving mixed content warnings under a strict deadline.

---

## Node 11: Vanilla Bedrock Server Setup
**Dependencies:** Node 1

### Syllabus (Practical Incidents)
1. **Binary Drop:** Download and extract the official Ubuntu Bedrock binary.
2. **Missing Libs:** Diagnose and fix missing shared libraries (e.g., `libcurl4`).
3. **Dual Bind:** Start the server and ensure both IPv4 and IPv6 ports bind correctly.
4. **Bedrock Props:** Update the `server.properties` with Bedrock-specific settings.
5. **Execute Denied:** Fix a server crash due to missing execution permissions on the binary.
6. **Allowlist:** Manage the `allowlist.json` to restrict player access.
7. **Service Setup:** Set up a dedicated, secure systemd service for the Bedrock server.
8. **The Pipe:** Run server commands via a named pipe (FIFO) for bash automation.
9. **Automated Backup:** Backup the `worlds` folder using a cronjob while the server is running.
10. **Safe Update:** Update the server binary to a new version without losing world data.
11. **Segfault Debug:** Interpret a Bedrock segmentation fault error log.
12. **Tick Tune:** Change server tick distance to improve performance on low-end hardware.
13. **Port Conflict:** Fix a "Cannot bind to port" error when running alongside Java Edition.
14. **Thread Cap:** Adjust `max-threads` for CPU optimization.
15. **Remote Console:** Connect and send commands to a remote Bedrock console via scripts.

**Boss Fight:** Upgrade a corrupted Bedrock server, fix its missing OS dependencies, restore a valid backup of the world, and re-establish the broken systemd service that relies on named pipes.

---

## Node 12: Docker Fundamentals for App Hosting
**Dependencies:** Node 1

### Syllabus (Practical Incidents)
1. **Engine Start:** Install Docker Engine and verify with the hello-world container.
2. **Port Map:** Run an Nginx container and map host port 8080 to container port 80.
3. **Conflict Resolution:** Fix a port conflict preventing a new container from starting.
4. **Volume Mount:** Mount a local host directory as a persistent volume in a container.
5. **Volume Permissions:** Fix file permission issues inside a mounted volume (UID/GID mismatch).
6. **Log Tailer:** Read and follow container logs to debug a crashed application.
7. **The Infiltrator:** Execute into a running container using `docker exec -it`.
8. **Dockerfile Basics:** Write a simple Dockerfile for a custom Python script.
9. **Build Crash:** Fix a Dockerfile failing at the `RUN apt-get install` step.
10. **Spring Cleaning:** Prune unused images, networks, and containers to free disk space.
11. **Env Vars:** Pass sensitive environment variables to a container using `-e`.
12. **Resource Limits:** Limit container CPU usage and Memory to prevent host starvation.
13. **Network Inspect:** Inspect a container to find its internal Docker IP address.
14. **Restart Policies:** Configure `--restart unless-stopped` for a critical app.
15. **Image Tagging:** Tag a local image and prepare it for a remote registry.

**Boss Fight:** Containerize a legacy web app from scratch: write the Dockerfile, mount the persistent database volume, fix the resulting permission errors, and ensure it restarts automatically on a system crash.

---

## Node 13: Spigot/Paper Plugin Servers
**Dependencies:** Node 7

### Syllabus (Practical Incidents)
1. **BuildTools:** Compile the latest Spigot/Paper jar using BuildTools from source.
2. **The Swap:** Swap a Vanilla `server.jar` for Paper seamlessly.
3. **First Plugin:** Install a basic plugin (e.g., EssentialsX) and verify it loads.
4. **Version Crash:** Fix a server crash caused by an outdated plugin.
5. **Paper Tune:** Configure `paper.yml` to optimize chunk loading and entity limits.
6. **Malware Hunt:** Read server logs to identify and remove a malicious/backdoored plugin.
7. **Perms Setup:** Manage user permissions using LuckPerms entirely via the terminal.
8. **YAML Syntax:** Fix a YAML syntax error in a plugin's `config.yml` that broke the plugin.
9. **World Border:** Set up a WorldBorder and pre-generate chunks via the console.
10. **Timings Report:** Run and analyze a timings report to find lag spikes.
11. **Hot Reload:** Update a plugin without restarting the server using PlugMan/commands.
12. **Java Mismatch:** Fix an "Unsupported Class Version" error by updating the JRE.
13. **Command Blocker:** Disable an exploitable command globally via `commands.yml`.
14. **Data Backup:** Backup and selectively restore specific plugin database files.
15. **Anti-Xray:** Configure Paper's built-in anti-xray engine to thwart cheaters.

**Boss Fight:** Rescue a lagging Paper server bogged down by 50+ plugins. You must identify the memory leak from a faulty plugin, fix three broken YAML configs, and heavily optimize `paper.yml` to achieve a stable 20 TPS.

---

## Node 14: PostgreSQL Backup & Replication
**Dependencies:** Node 5

### Syllabus (Practical Incidents)
1. **Logical Backup:** Perform a full logical backup using `pg_dump`.
2. **Table Restore:** Restore a specific deleted table from a logical backup.
3. **Global Dump:** Perform a global backup of all roles and databases using `pg_dumpall`.
4. **Cron Automator:** Automate daily backups via cron and rotate old files.
5. **Auth Fail:** Fix a scheduled backup failing due to authentication issues.
6. **Physical Copy:** Perform a fast physical backup using `pg_basebackup`.
7. **WAL Archiving:** Set up and verify WAL (Write-Ahead Log) archiving to a separate directory.
8. **Disk Exhaustion:** Fix a database halting due to WAL disk space exhaustion.
9. **Read Replica:** Configure a read-only replica via streaming replication.
10. **Slot Repair:** Troubleshoot and fix a broken replication slot.
11. **The Promotion:** Promote a replica to primary during a simulated failure.
12. **Lag Monitor:** Check system views to monitor replication lag in bytes/seconds.
13. **Time Travel:** Set up the prerequisites for Point-in-Time Recovery (PITR).
14. **The Vacuum:** Vacuum a bloated database via `vacuumdb` to reclaim space.
15. **PITR Restore:** Restore a accidentally dropped database using a PITR backup.

**Boss Fight:** The primary DB is dead. You must promote the read-replica, re-point the application, fix the broken WAL archiving, and perform a full `vacuum` to stabilize performance.

---

## Node 15: Modded Servers (Forge/Fabric)
**Dependencies:** Node 7

### Syllabus (Practical Incidents)
1. **Forge Install:** Install the Forge server environment via the CLI installer.
2. **Arg Tweak:** Fix memory settings inside the `user_jvm_args.txt` configuration.
3. **Mod Drop:** Install a server-side mod and verify it loads in the console.
4. **Missing Dep:** Resolve a crash caused by a mod missing its required library/dependency.
5. **ID Conflict:** Fix a block/item ID conflict or registry error from the logs.
6. **Client-Only Crash:** Identify and remove a client-only mod (e.g., minimap) crashing the server.
7. **Fabric Setup:** Install and configure the Fabric server launcher.
8. **Fabric API:** Add the Fabric API mod and resolve version incompatibilities.
9. **Heavy Load:** Allocate massive RAM properly with garbage collection tweaks for a 200+ modpack.
10. **Stack Trace:** Decipher a massive Java stack trace to find the exact failing mod.
11. **Dimension Disable:** Disable a specific dimension causing server hangs in config files.
12. **Chunk Wipe:** Wipe a corrupted chunk using an external CLI tool (MCA Selector headless).
13. **Auto-Restart:** Configure auto-restarts specifically to combat heavy memory leak modpacks.
14. **Toml Tweaks:** Adjust Forge `server.toml` settings for server performance.
15. **Migration:** Fix incompatibilities when migrating a world from Forge to Fabric.

**Boss Fight:** Deploy a heavy 250-mod Forge modpack on a headless server. Diagnose the startup crash loop, strip out the client-side mods, fix the memory allocation flags, and resolve a dimension ID conflict.

---

## Node 16: Redis Clustering & Persistence
**Dependencies:** Node 6

### Syllabus (Practical Incidents)
1. **Master-Replica:** Set up a basic Redis Master-Replica configuration.
2. **Sync Fail:** Fix a replica that is continuously failing to sync with the master.
3. **Sentinel Setup:** Configure Redis Sentinel for automated high availability monitoring.
4. **Failover Test:** Simulate a master failure and verify Sentinel promotes the replica.
5. **Split-Brain:** Fix a Sentinel split-brain scenario.
6. **Cluster Init:** Set up a true Redis Cluster with 3 master nodes and 3 replicas.
7. **Node Add:** Safely add a new master node to an existing Redis Cluster.
8. **Resharding:** Reshard slots across the Redis Cluster to balance the load.
9. **Cluster Down:** Fix a "CLUSTERDOWN The cluster is down" error.
10. **Data Migration:** Migrate keys from a standalone Redis instance into a cluster.
11. **AOF Rewrite:** Configure aggressive AOF rewrite policies for heavy write loads.
12. **AOF Repair:** Recover corrupted AOF data using `redis-check-aof`.
13. **Big Key Hunt:** Analyze and find memory hogs using `redis-cli --bigkeys`.
14. **Latency Debug:** Debug high latency operations using `redis-cli --latency`.
15. **TLS Cluster:** Secure intra-cluster communication using TLS certificates.

**Boss Fight:** Recover a crashed Redis Cluster. You must repair the corrupted AOF file, manually reshard the lost hash slots, and re-establish Sentinel monitoring without any data loss.

---

## Node 17: Docker Compose for Multi-Tier Apps
**Dependencies:** Node 12

### Syllabus (Practical Incidents)
1. **First Compose:** Write a `docker-compose.yml` for an Nginx + Python web app.
2. **Database Link:** Add a PostgreSQL database service to the compose file.
3. **Internal Net:** Link containers strictly using isolated Docker networks.
4. **Resolution Fail:** Fix a container unable to resolve the DB hostname.
5. **Shared Volume:** Mount a shared named volume between two separate containers.
6. **Env Files:** Use `.env` files to pass database credentials securely.
7. **Syntax Fix:** Fix a YAML syntax error preventing `docker-compose up`.
8. **Force Recreate:** Force recreate a corrupted container without affecting others.
9. **Scaling Up:** Scale a stateless web service to 3 replicas.
10. **Startup Order:** Configure container startup order using `depends_on` and healthchecks.
11. **Healthcheck Debug:** Debug a failing healthcheck that keeps restarting a container.
12. **Port Hide:** Expose only the frontend reverse proxy port to the host machine.
13. **Docker Backup:** Backup a database running inside Docker Compose using `docker exec`.
14. **Aggregated Logs:** View and filter aggregated logs of all running services.
15. **Zero Downtime:** Update a container image and restart the stack with zero downtime.

**Boss Fight:** Deploy a complex 4-tier application (Web, API, Redis, DB). Fix the broken internal networking, write the missing service healthchecks, and ensure the database actually persists data after a `docker-compose down`.

---

## Node 18: BungeeCord/Waterfall Network Setup
**Dependencies:** Node 13

### Syllabus (Practical Incidents)
1. **Proxy Install:** Install Waterfall and configure the base `config.yml`.
2. **Server Link:** Link a Hub server and a Survival server in the config.
3. **IP Forwarding:** Fix the "IP Forwarding" error by configuring Spigot and Bungee correctly.
4. **Online Mode Fix:** Resolve the "Server is online mode!" kick message.
5. **Backend Firewall:** Configure `iptables` to block direct access to backend servers.
6. **Fallback Setup:** Set up fallback servers in case the Hub goes down.
7. **Proxy Perms:** Configure basic proxy-level permissions in BungeeCord.
8. **Proxy Plugin:** Install and configure a BungeeCord proxy plugin (e.g., ServerListPlus).
9. **Java Crash:** Fix a proxy crash caused by an outdated Java version.
10. **Forced Hosts:** Set up forced hosts (e.g., `survival.domain.com` routing directly to survival).
11. **Global Broadcast:** Send a global broadcast via the proxy console.
12. **Player Cap:** Limit proxy max players to prevent backend overload.
13. **UUID Spoofing:** Prevent UUID spoofing by enforcing strict firewall rules.
14. **Bot Throttle:** Configure connection throttles to mitigate basic bot attacks.
15. **Packet Drops:** Analyze Waterfall proxy logs for dropped packets and timeouts.

**Boss Fight:** Build a secure Minecraft network. You must fix IP forwarding so real player IPs show, block direct port scanning to backend servers using strict firewall rules, and route incoming subdomains to the correct game modes.

---

## Node 19: Performance Monitoring & Logs
**Dependencies:** Node 1

### Syllabus (Practical Incidents)
1. **CPU Hog:** Install and use `htop` to identify and kill a runaway process.
2. **Disk Thrashing:** Analyze disk IO using `iotop` to find what is writing so much.
3. **Space Invader:** Find large hidden files eating disk space using `ncdu`.
4. **Log Parse:** Parse an Nginx access log to find top IP addresses using `awk` and `sort`.
5. **Web Dash:** Install `goaccess` for terminal-based web log analysis.
6. **Bandwidth Hog:** Check real-time network bandwidth usage using `nload` or `iftop`.
7. **Port Spy:** Find which ghost process is listening on a port using `ss` or `netstat`.
8. **Syscall Trace:** Use `strace` to find why a game server process is hanging on startup.
9. **OOM Hunt:** Monitor kernel logs via `dmesg` to confirm an OOM killer event.
10. **Historical RAM:** Set up `sysstat` (sar) to view historical RAM usage from yesterday.
11. **Slow Queries:** Enable and analyze Postgres slow query logs.
12. **Packet Sniff:** Use `tcpdump` to capture packets of a failing API call.
13. **Log Rotate:** Rotate huge log files manually using `logrotate` configs.
14. **Disk Full:** Fix a completely filled up `/var/log` partition safely.
15. **Trace Route:** Trace DNS and routing issues using `dig` and `traceroute`.

**Boss Fight:** The server is randomly freezing every 4 hours. Use monitoring tools to identify an OOM-killer event, track down the memory leak to a specific Docker container, and implement a log rotation policy to fix the full disk.

---

## Node 20: CI/CD & Automated Game Server Deployments
**Dependencies:** Node 17

### Syllabus (Practical Incidents)
1. **Map Puller:** Write a bash script to pull the latest Minecraft map from a Git repo.
2. **Git Hook:** Set up a git hook to restart the server automatically on push.
3. **Plugin Auto-Update:** Automate downloading the latest plugin jars via `curl` scripts.
4. **Make Automator:** Write a `Makefile` for quick Docker container management.
5. **Bash Debug:** Fix a broken bash deployment script that is failing silently.
6. **Secret Keep:** Handle database credentials securely in automated deployment scripts.
7. **Rsync Deploy:** Deploy a web update using `rsync` without overwriting user uploads.
8. **Pre-Flight Check:** Validate Nginx configs automatically in the script before reloading.
9. **Discord Webhook:** Send a Discord webhook notification when the server successfully starts.
10. **Auto Migrate:** Automate database schema migrations on container start.
11. **Rollback:** Write a script to quickly roll back a failed deployment from a tarball.
12. **Key Auth:** Configure SSH keys for passwordless script execution between servers.
13. **Staging Clone:** Create a script to instantly clone production into a staging environment.
14. **Deploy Logs:** Monitor and log the output of deployment scripts for debugging.
15. **Path Trigger:** Create a `systemd.path` unit to trigger scripts upon a file change.

**Boss Fight:** Fix a completely broken continuous deployment pipeline. You must repair the SSH keys, fix the `rsync` permissions, resolve the Nginx config validation failure, and successfully deploy a new web update with zero downtime.
