# Terminal Academy Skill Tree: Networking & Security

Welcome to the Networking & Security branch. This domain transforms initiates into network operators, firewall architects, and penetration testers. The curriculum is entirely scenario-based—no multiple-choice theory, only broken configurations, locked-down servers, and hostile environments.

---

## Node 1: Network Interfaces & Link Management (`iproute2`)
**Dependencies**: None
**Focus**: Interface states, addressing, MAC manipulation.

**Incidents:**
1. **The Dead Link**: `eth1` is administratively down. Bring it up to restore the DB connection.
2. **Missing Identity**: The web server lost its IP. Assign static IP `192.168.10.55/24` to `eth0`.
3. **Ghost in the MAC**: Bypass a sticky MAC port-security lock by spoofing `eth2`'s MAC address.
4. **Subnet Squeeze**: Change the subnet mask on `eth0` from `/24` to `/26` without dropping the SSH session.
5. **The MTU Mismatch**: Jumbo frames are failing. Set `eth1` MTU to 9000 to fix the storage replication link.
6. **Promiscuous Mode**: A sniffer script is failing. Enable promiscuous mode on `eth0`.
7. **Phantom Interfaces**: Identify and delete a rogue dummy interface created by malware.
8. **VLAN Tagging Missing**: The switch is tagging VLAN 40. Create `eth0.40` and assign an IP.
9. **Duplicate IP Nightmare**: Use `arping` to prove another machine is stealing our IP, then assign a fallback IP.
10. **The Lost Gateway**: The default route was wiped. Add the gateway `10.0.0.1` back to `eth0`.
11. **Virtual Interfaces**: Create a virtual interface `eth0:1` for a secondary Nginx server block.
12. **Interface Renaming**: A custom udev rule renamed `eth0` to `ens33`. Revert it and restart networking.
13. **Link Aggregation**: Create a basic bonding interface (`bond0`) for `eth1` and `eth2`.
14. **Multicast Chaos**: Disable multicast on `eth0` to stop a flood of MDNS packets crashing the server.
15. **Boss Fight: The Silent Datacenter**: All interfaces wiped, random MTUs, overlapping subnets, and a broken bonding setup. Reconstruct the entire link layer to restore the web stack before the SLA breaches.

---

## Node 2: Basic Connectivity Diagnostics (`ping`, `traceroute`, `mtr`)
**Dependencies**: Node 1
**Focus**: ICMP, path MTU discovery, identifying drops.

**Incidents:**
1. **The Blind Ping**: `ping 8.8.8.8` fails but web browsing works. Diagnose and fix the local ICMP block.
2. **Trace the Drop**: Use `traceroute` to find which hop in a 10-router chain is dropping UDP packets.
3. **MTR Watcher**: Run `mtr` to capture intermittent packet loss (jitter) over a 5-minute window and log it.
4. **Path MTU Blackhole**: Large packets are dropping. Use `ping -M do -s` to find the exact MTU bottleneck.
5. **Source Routing**: Force `ping` to use `eth1` instead of `eth0` to test a backup ISP link.
6. **Broadcast Storm**: Identify devices responding to a broadcast ping on `192.168.1.255`.
7. **Traceroute Protocol Swap**: UDP traceroute is blocked. Switch to TCP SYN traceroute to bypass the firewall.
8. **TTL Exceeded**: Manually craft a ping with TTL=1 to prove the immediate gateway is misconfigured.
9. **ICMP Redirect Hijack**: Analyze a suspicious ICMP redirect telling the server to route through `10.0.0.99`.
10. **The Latency Spike**: Write a bash one-liner using `ping` to alert if latency exceeds 200ms.
11. **Flood Ping**: Use `ping -f` to stress-test a local switch port (requires root).
12. **IPv6 Void**: `ping6` fails. Enable IPv6 on the interface and test connectivity to `ff02::1`.
13. **Timestamp Requests**: Send ICMP timestamp requests to determine the uptime of a legacy switch.
14. **Record Route**: Use the IP Record Route option in ping to see the exact return path of packets.
15. **Boss Fight: The Labyrinth**: A complex network where ICMP is filtered differently at 5 hops. Use TCP/UDP traceroutes, custom MTUs, and source-interface bindings to map the network and find the hidden backup server.

---

## Node 3: Layer 2 & ARP Mysteries (`arp`, `bridge`, `ndp`)
**Dependencies**: Node 1
**Focus**: ARP tables, bridging, neighbor discovery.

**Incidents:**
1. **The Stale Cache**: `192.168.1.10` changed its MAC, but your server still tries the old one. Flush the ARP cache.
2. **ARP Poisoning Victim**: Detect that the gateway's MAC in the ARP table has been replaced by an attacker.
3. **Static ARP Lock**: Hardcode the gateway's MAC address to prevent further ARP spoofing.
4. **Proxy ARP**: Enable proxy ARP on `eth0` so a hidden VM can communicate with the main network.
5. **Bridge Builder**: Create a Linux bridge `br0` and enslave `eth1` and `eth2` to it.
6. **Spanning Tree Storm**: Enable STP on `br0` to stop a broadcast loop crashing the local segment.
7. **FDB Inspection**: Read the Forwarding Database of `br0` to find which port a specific MAC is on.
8. **IPv6 Neighbor Discovery**: The IPv6 equivalent of ARP is broken. View and flush the NDP cache.
9. **Gratuitous ARP**: Send a gratuitous ARP to announce your server's new IP to the switch immediately.
10. **ARP Flux**: The server has IPs on two interfaces in the same subnet. Fix the `arp_announce` sysctls.
11. **Macvlan Madness**: Create a `macvlan` interface attached to `eth0` for a container.
12. **The Bridged Firewall**: Pass bridged traffic through iptables for inspection (br_netfilter).
13. **ARP Watcher**: Install and configure `arpwatch` to alert on new MAC addresses on the subnet.
14. **Multicast Snooping**: Disable IGMP snooping on the bridge to fix a broken discovery protocol.
15. **Boss Fight: The Poisoned Switch**: You are under active ARP spoofing. Hardcode critical MACs, isolate the attacker port using bridge FDB, and establish a stable macvlan connection for the production DB.

---

## Node 4: DNS & Name Resolution (`dig`, `resolvectl`, `/etc/hosts`)
**Dependencies**: Node 2
**Focus**: Resolution chains, DNS records, local overrides.

**Incidents:**
1. **The Poisoned Host**: Malware modified `/etc/hosts` to redirect `github.com` to `127.0.0.1`. Fix it.
2. **Resolv.conf Overwrite**: NetworkManager keeps overwriting `/etc/resolv.conf`. Lock it down to use `1.1.1.1`.
3. **NXDOMAIN Panic**: `dig` shows a domain exists, but ping says "Name or service not known". Fix `/etc/nsswitch.conf`.
4. **The Missing MX**: Use `dig` to find the mail servers for a domain to troubleshoot bouncing emails.
5. **Reverse DNS Mismatch**: Use `dig -x` to prove that an incoming SSH connection is spoofing its hostname.
6. **Zone Transfer**: Attempt an AXFR zone transfer on a misconfigured internal DNS server to map the network.
7. **DNS over TLS (DoT)**: Configure `systemd-resolved` to use strict DNS over TLS.
8. **Split-Horizon DNS**: Route DNS queries for `corp.local` to `10.0.0.5` and everything else to `8.8.8.8` via `resolvectl`.
9. **TXT Record Secrets**: Query the TXT records of `_acme-challenge.example.com` to debug a broken SSL cert.
10. **Custom DNS Port**: Query a DNS server running on non-standard port `5353`.
11. **DNS Cache Poisoning**: Flush the local `systemd-resolved` cache that is holding a bad A record.
12. **CNAME Chains**: Trace a CNAME record that redirects 5 times to find the final IP.
13. **DNS Leak**: Verify that VPN traffic is not leaking DNS queries to the local ISP.
14. **mDNS Resolution**: Resolve `printer.local` using `avahi-resolve` instead of standard DNS.
15. **Boss Fight: The Mirage**: The system is infected with DNS-hijacking malware, local caches are poisoned, and `nsswitch` is corrupted. Restore pristine resolution, secure the DNS path with DoT, and extract the attacker's C2 server from a hidden TXT record.

---

## Node 5: Packet Sniffing & PCAP Analysis (`tcpdump`, `tshark`)
**Dependencies**: Node 2
**Focus**: Wire-level analysis, packet filtering, extraction.

**Incidents:**
1. **The Noisy Wire**: Use `tcpdump` to capture only SSH traffic on `eth0` to verify connections.
2. **Hex Dumps**: Capture ICMP packets and print the hex/ASCII payload to read a hidden message.
3. **The Silent Drop**: Capture traffic between two IPs and prove the firewall is sending TCP RST packets.
4. **PCAP Extraction**: Save a capture to `evidence.pcap` for later analysis.
5. **Tshark Magic**: Use `tshark` to read a PCAP and extract only the HTTP Host headers.
6. **BPF Filters**: Write a BPF filter to capture only TCP packets with the SYN flag set (connection attempts).
7. **Cleartext Passwords**: Sniff an FTP connection and extract the plaintext username and password.
8. **DNS Interception**: Capture all DNS queries (port 53) and filter out the noise to find a malicious beacon.
9. **Jumbo Capture**: Adjust the `tcpdump` snaplen (`-s 0`) to capture entire 9000-byte packets without truncation.
10. **Ring Buffer Captures**: Run `tcpdump` continuously, rotating files every 50MB to catch an intermittent bug.
11. **VLAN Sniffing**: Capture traffic strictly on VLAN tag 20 using `tcpdump`.
12. **VoIP Debugging**: Extract SIP INVITE packets to figure out why phone calls aren't ringing.
13. **TLS Handshake**: Capture the Client Hello to verify if the server is negotiating TLS 1.2 or 1.3.
14. **MAC Address Filtering**: Capture all traffic originating from a specific rogue MAC address.
15. **Boss Fight: The Exfiltration**: A compromised server is leaking data. Use `tcpdump` and `tshark` to isolate the stealthy ICMP tunneling, extract the hex payloads from the PCAP, reconstruct the stolen file, and identify the destination.

---

## Node 6: Basic Routing & Gateways (`ip route`)
**Dependencies**: Node 1
**Focus**: Routing tables, default gateways, static routes.

**Incidents:**
1. **No Route to Host**: The server can't reach the internet. Add a default gateway to `10.0.0.1`.
2. **The Missing Subnet**: Add a static route to reach the `172.16.0.0/16` subnet via router `10.0.0.254`.
3. **Metric Wars**: You have two default routes. Change the metric of the backup route to 200 so it isn't preferred.
4. **Blackhole Routing**: Null-route (`blackhole`) an attacking IP `198.51.100.4` to drop its traffic instantly.
5. **Local Routing Table**: Inspect the `local` routing table to understand why an IP is looping back.
6. **Temporary Route**: Add a route that will survive a network restart by modifying the OS netplan/interfaces file.
7. **Gateway Ping Loss**: Route ping responses through a specific interface to bypass asymmetric routing drops.
8. **Host-Specific Route**: Route traffic for a single IP `8.8.8.8` through a VPN tunnel interface `tun0`.
9. **Routing Cache Flush**: Flush the routing cache after changing the default gateway to force immediate adoption.
10. **Probing Routes**: Use `ip route get 8.8.4.4` to ask the kernel exactly which path a packet will take.
11. **ECMP Routing**: Setup Equal-Cost Multi-Path routing to load balance traffic across two gateways.
12. **Scope Link**: Add a route with `scope link` to communicate with a host directly on the segment.
13. **Reject Routes**: Add a `unreachable` route to send ICMP administratively prohibited messages to a subnet.
14. **Broadcast Routing**: Fix a misconfigured broadcast address in the routing table.
15. **Boss Fight: The Asymmetric Nightmare**: Two ISPs, three subnets, packets going out one interface and returning on another (causing firewall drops). Rebuild the routing table, fix the metrics, and ensure strict symmetric paths.

---

## Node 7: Advanced Policy Routing (`ip rule`, `vrf`)
**Dependencies**: Node 6
**Focus**: Multiple routing tables, source-based routing, VRFs.

**Incidents:**
1. **Source Routing**: Traffic from `eth1` (10.0.1.5) must use gateway `10.0.1.1`, not the main default gateway. Create a custom routing table.
2. **The `ip rule` Fix**: Add an `ip rule` to direct traffic from `10.0.1.5` to use your new custom table.
3. **Fwmark Routing**: Route traffic marked by iptables (mark `0x1`) to a VPN interface.
4. **Multiple Defaults**: Configure default gateways for two separate ISP links simultaneously without conflict.
5. **VRF Creation**: Create a Virtual Routing and Forwarding (VRF) instance named `mgmt_vrf`.
6. **Enslaving Interfaces**: Move `eth0` into `mgmt_vrf` to isolate management traffic from production.
7. **Pinging across VRFs**: Execute a ping from inside `mgmt_vrf` to test connectivity.
8. **Rule Priorities**: Adjust the `ip rule` priorities so the VPN routing table is evaluated before the main table.
9. **Type of Service (ToS)**: Route VoIP traffic (matching specific ToS bits) via a dedicated low-latency link.
10. **Bypassing the VPN**: Add an `ip rule` to force traffic destined for `192.168.1.0/24` to bypass the VPN table.
11. **Orphaned Rules**: Clean up stale `ip rule` entries left behind by a crashed VPN client.
12. **Namespaces Basics**: Create a Linux network namespace `test_ns` and move a veth interface into it.
13. **Routing in Namespaces**: Configure a default route inside the isolated `test_ns` namespace.
14. **Cross-Namespace Communication**: Route traffic between the global namespace and `test_ns`.
15. **Boss Fight: The Split-Brain Router**: The system acts as a router for 3 overlapping subnets and 2 VPNs. Use VRFs and Policy Routing to completely isolate the networks, route marked web traffic through the VPN, and leave SSH untouched.

---

## Node 8: Port Scanning & Service Discovery (`nmap` basics)
**Dependencies**: Node 2
**Focus**: Host discovery, TCP/UDP scanning, version detection.

**Incidents:**
1. **The Silent Ping**: Hosts are ignoring ICMP. Use `nmap -Pn` to discover live hosts on `192.168.1.0/24`.
2. **Stealth Scan**: Perform a TCP SYN scan (`-sS`) on a target to avoid completing the full 3-way handshake.
3. **UDP Mystery**: A DNS server is suspected on `10.0.0.50`. Perform a UDP scan (`-sU`) on port 53.
4. **Version Detection**: Port 80 is open, but is it Apache or Nginx? Run a version detection scan (`-sV`).
5. **OS Fingerprinting**: Use OS detection (`-O`) to figure out if the target is Linux or Windows.
6. **Fast Scanning**: Scan the top 100 ports quickly (`-F`) to get an initial lay of the land.
7. **Specific Port Targeting**: Scan only ports 80, 443, and 8080-8090 on a target.
8. **Output Formatting**: Save scan results in grepable format (`-oG`) and extract all open ports using `awk`.
9. **Timing Templates**: The firewall is dropping your aggressive scans. Slow it down with `-T2`.
10. **Packet Tracing**: Use `--packet-trace` to see exactly what nmap is sending and receiving.
11. **Source Port Spoofing**: Bypass a stateless firewall by forcing nmap to use source port 53 (`-g 53`).
12. **Fragmenting Packets**: Fragment nmap packets (`-f`) to evade a basic intrusion detection system.
13. **Decoy Scanning**: Hide your true IP by scanning with decoys (`-D 10.0.0.1,10.0.0.2,ME`).
14. **List Scan**: Perform a reverse-DNS resolution list scan (`-sL`) without actually sending packets to the hosts.
15. **Boss Fight: The Ghost Subnet**: A highly defended subnet drops ICMP, heavily rate-limits TCP, and runs services on non-standard ports. Map out all 5 live hosts, their OS, and services using stealth, fragmentation, timing controls, and decoy scans.

---

## Node 9: Advanced Nmap & Vulnerability Scanning (NSE)
**Dependencies**: Node 8
**Focus**: Nmap Scripting Engine, vulnerability detection, advanced evasion.

**Incidents:**
1. **Default Scripts**: Run the default set of safe scripts (`-sC`) against a web server to find basic info.
2. **SMB Enumeration**: Run the `smb-os-discovery` script to extract the exact Windows build number.
3. **Vulnerability Scanning**: Use `vuln` script category to check an older server for known CVEs (like Heartbleed or MS17-010).
4. **HTTP Title Grabber**: Use `http-title` to quickly see what websites are hosted on 50 different IPs.
5. **Directory Brute Forcing**: Use `http-enum` to find hidden `/admin` directories on a target.
6. **Banner Grabbing**: Use a raw connect scan with `banner` script to grab raw service banners.
7. **SSL Cipher Check**: Check an HTTPS server for weak ciphers using `ssl-enum-ciphers`.
8. **FTP Anonymous Login**: Verify if an FTP server allows anonymous login using `ftp-anon`.
9. **MySQL Empty Password**: Use `mysql-empty-password` to find an insecure database instance.
10. **Script Arguments**: Pass credentials to an NSE script using `--script-args user=admin,pass=admin`.
11. **Custom Scripting**: Write a 5-line Lua NSE script to connect to a port and send a custom "HELLO" string.
12. **Firewall Rule Evasion**: Use `--badsum` to see if a firewall is blindly forwarding packets with bad checksums.
13. **Idle Zombie Scan**: Perform a completely stealthy Idle scan (`-sI`) by bouncing off a zombie printer.
14. **NSE Script Update**: Update the nmap script database (`--script-updatedb`).
15. **Boss Fight: The DMZ Audit**: You are given a subnet of 20 IPs. You must identify all web servers, check them for SSL vulnerabilities, find the one FTP server allowing anonymous access, and map the internal network trust relationships—all without tripping the aggressive IPS.

---

## Node 10: Local Host Firewalls (`ufw`, `firewalld`)
**Dependencies**: Node 2
**Focus**: Simple host-level protection, zones, basic policies.

**Incidents:**
1. **Lockdown**: Enable `ufw` and set the default incoming policy to deny, but don't lock yourself out of SSH!
2. **Allowing Services**: Open port 443/tcp for a new HTTPS server using `ufw`.
3. **IP Whitelisting**: Allow all traffic from the backup server IP `10.0.0.50` in `ufw`.
4. **Rate Limiting**: Use `ufw limit ssh` to protect against brute-force attacks.
5. **Deleting Rules**: Find the numbered rule for port 8080 and delete it.
6. **Firewalld Zones**: Move `eth0` into the `public` zone in `firewalld`.
7. **Rich Rules**: Add a firewalld rich rule to reject traffic from `192.168.1.100` with an ICMP admin-prohibited message.
8. **Service Definitions**: Allow the `http` and `https` predefined services in firewalld permanently.
9. **Panic Mode**: Turn on firewalld panic mode to instantly drop all packets during an active attack.
10. **Port Forwarding (firewalld)**: Forward incoming port 8888 to port 80 internally.
11. **Logging Drops**: Enable ufw logging at the `medium` level to see dropped packet details in syslog.
12. **UFW Application Profiles**: Allow Nginx Full profile instead of specifying ports manually.
13. **Masquerading**: Enable masquerading in firewalld's external zone for NAT.
14. **Direct Rules**: Insert a raw iptables rule via firewalld's direct interface to bypass standard zones.
15. **Boss Fight: The Lockdown Drill**: A server is completely open. Using UFW or Firewalld, implement a strict default-deny policy, whitelist 3 specific management IPs, rate-limit SSH, allow web traffic, and forward a custom port—all while maintaining your own SSH connection.

---

## Node 11: Iptables Fundamentals (`filter` table)
**Dependencies**: Node 10
**Focus**: Chains, targets, stateless vs stateful filtering.

**Incidents:**
1. **The Default Drop**: Change the default policy of the `INPUT` chain to `DROP` (careful with SSH!).
2. **Stateful Acceptance**: Add a rule to allow `ESTABLISHED` and `RELATED` connections so return traffic works.
3. **The Loopback Exception**: Traffic to `127.0.0.1` is blocked. Append a rule to allow all traffic on the `lo` interface.
4. **Inserting Rules**: A DROP rule is at position 1. Insert an ACCEPT rule for SSH at position 1 to override it.
5. **ICMP Rate Limiting**: Allow ICMP echo requests, but limit them to 1 per second using the `limit` module.
6. **Port Ranges**: Allow incoming TCP traffic on ports 6000 through 6010 using `--dport`.
7. **Multiport**: Allow ports 80, 443, and 8080 in a single rule using the `multiport` module.
8. **Logging Packets**: Add a rule to `LOG` dropped packets with the prefix "IPTABLES-DROP: " before they hit the final DROP rule.
9. **MAC Filtering**: Drop traffic from a specific MAC address regardless of its IP.
10. **String Matching**: Drop unencrypted HTTP packets that contain the string "cmd.exe" using the `string` module.
11. **Reject vs Drop**: Reject incoming Telnet (port 23) with a `tcp-reset` instead of silently dropping it.
12. **Custom Chains**: Create a custom chain named `LOG_AND_DROP`, link it, and send bad traffic there.
13. **Flushing Rules**: Flush all rules in the `filter` table and delete custom chains to start fresh.
14. **Saving & Restoring**: Save the current iptables configuration to a file and restore it to ensure persistence.
15. **Boss Fight: The Bastion Host**: Manually construct an iptables firewall script from scratch. It must statefully allow outgoing traffic, accept SSH only from a specific subnet, rate-limit pings, drop port scanners, and log all violations, surviving a reboot.

---

## Node 12: Advanced Iptables (`nat`, `mangle`, `raw`)
**Dependencies**: Node 11
**Focus**: PREROUTING, POSTROUTING, SNAT/DNAT, packet alteration.

**Incidents:**
1. **Source NAT (Masquerade)**: The internal network (`10.0.0.0/24`) needs internet. Enable `MASQUERADE` on `POSTROUTING` for `eth0`.
2. **Static SNAT**: Change the source IP of outgoing packets to a specific public IP instead of masquerading.
3. **Port Forwarding (DNAT)**: Forward incoming traffic on port 80 to an internal backend server `10.0.0.5:8080` using `PREROUTING`.
4. **Local Port Redirect**: Redirect incoming traffic on port 443 to a local service running on port 8443 (`REDIRECT` target).
5. **The Forwarding Catch**: A DNAT rule is active, but traffic is dropped. Add the required `FORWARD` chain rule in the filter table to permit the NATted traffic.
6. **Mangle TTL**: Change the TTL of all outgoing packets to 128 (Windows default) to obscure the OS type using the `mangle` table.
7. **Marking Packets**: Use the `mangle` table to set a firewall mark (`--set-mark 1`) on SSH packets for policy routing.
8. **TCP MSS Clamping**: Fix stalled PPPoE/VPN connections by clamping the MSS to PMTU in the `mangle` table.
9. **Raw Table Bypassing**: Use the `raw` table and the `NOTRACK` target to exempt heavy DNS traffic from connection tracking overhead.
10. **Load Balancing**: Use the `statistic` module in `PREROUTING` to round-robin incoming web traffic between two internal IPs.
11. **Geo-IP Blocking (Concept)**: Block traffic from a large list of CIDRs efficiently using `ipset` combined with iptables.
12. **Time-Based Rules**: Allow access to the backup port only between 02:00 and 04:00 using the `time` module.
13. **Recent Module**: Implement port knocking: require a ping with a specific payload size before opening SSH using the `recent` module.
14. **Tracing Packets**: Use the `TRACE` target in the `raw` table to debug exactly which chains and rules a packet hits.
15. **Boss Fight: The Invisible Proxy**: Build a transparent intercepting proxy. Route all outgoing HTTP/HTTPS traffic from a guest subnet through a local scanning service on port 3128 using DNAT, ensure return traffic works, clamp MSS for the VPN uplink, and implement port knocking for administrative access.

---

## Node 13: SSH Fundamentals & Hardening (`sshd_config`, `ssh-keygen`)
**Dependencies**: Node 2
**Focus**: Asymmetric keys, agent forwarding, secure configurations.

**Incidents:**
1. **The Password Purge**: Disable password authentication in `sshd_config` and require SSH keys.
2. **Key Generation**: Generate an Ed25519 SSH keypair and copy it to a target server using `ssh-copy-id`.
3. **Root Lockdown**: Disable `PermitRootLogin` completely to prevent direct root access.
4. **Custom Port**: Move SSH from port 22 to port 2222 and update the firewall.
5. **Agent Forwarding**: Configure `ssh-agent` and use `-A` to jump through a bastion host without leaving private keys on the bastion.
6. **Config Files**: Create an `~/.ssh/config` file to map `Host db` to `10.0.0.50`, user `admin`, port `2222`, and a specific identity file.
7. **Authorized_Keys Restrictions**: Restrict an SSH key in `authorized_keys` so it can only execute a specific backup script (`command="..."`).
8. **Connection Multiplexing**: Enable `ControlMaster` in ssh config to reuse a single TCP connection for multiple SSH sessions.
9. **Keepalive**: SSH connections drop after 5 minutes of inactivity. Fix it using `ServerAliveInterval`.
10. **Cipher Hardening**: Restrict `sshd` to only use modern ciphers (e.g., `chacha20-poly1305`) and disable CBC ciphers.
11. **User Allowlist**: Restrict SSH access to only the `admin` and `deploy` users via `AllowUsers`.
12. **Host Key Checking**: Fix the "REMOTE HOST IDENTIFICATION HAS CHANGED" error after a server rebuild by clearing the `known_hosts` entry.
13. **SSH Certificate Authority**: (Basic) Sign a user key with an SSH CA key so they can log into any server trusting the CA.
14. **Banner Warning**: Add a legal warning banner before login using the `Banner` directive.
15. **Boss Fight: The Impenetrable Bastion**: Secure a bastion host. Enforce Ed25519 keys, disable root, change the port, restrict an automated backup key to a single command, set aggressive timeouts, and configure a local `~/.ssh/config` for seamless multiplexed jumps to the internal network.

---

## Node 14: SSH Tunnels & Pivoting (Local, Remote, Dynamic)
**Dependencies**: Node 13
**Focus**: Port forwarding, SOCKS proxies, reverse shells via SSH.

**Incidents:**
1. **Local Port Forwarding (`-L`)**: Access an internal database on `10.0.0.5:3306` by forwarding your local port 3306 through the bastion host.
2. **Remote Port Forwarding (`-R`)**: Expose your local development server (port 8080) to the internet by forwarding it to port 80 on a public VPS.
3. **Dynamic Port Forwarding (`-D`)**: Create a SOCKS5 proxy on local port 9050 using SSH to securely browse the web through a remote server.
4. **GatewayPorts**: A remote forward `-R` only binds to `127.0.0.1` on the VPS. Enable `GatewayPorts` in `sshd_config` so external users can external users access it.
5. **Jump Hosts (`-J`)**: Use the `-J` flag to tunnel through `bastion1` and `bastion2` to reach the final secure database.
6. **Background Tunnels (`-fN`)**: Start an SSH tunnel in the background without executing a remote shell.
7. **Reverse SSH Shell**: Use a reverse SSH tunnel to gain access to a machine behind a strict NAT router.
8. **Tunneling RDP/VNC**: Forward an RDP session (port 3389) securely over SSH to manage a Windows server.
9. **ProxyCommand Legacy**: Use `ProxyCommand` and `netcat` to jump through a host (the old way, before `-J`).
10. **Chaining Local Forwards**: Chain two `-L` commands across two different SSH sessions to reach a deeply nested service.
11. **VPN over SSH (`-w`)**: Create a true layer 3 VPN tunnel using SSH `tun` devices.
12. **SOCKS Proxy with Browser**: Configure curl or Firefox to use the SOCKS proxy created by `-D`.
13. **SSH Multiplexer Reverse**: Create a reverse tunnel using an already established multiplexed control socket.
14. **Restricting Tunnels**: Hard-code `PermitOpen` in `sshd_config` to ensure users can only forward ports to specific internal IPs.
15. **Boss Fight: The Deep Pivot**: You are on a compromised web server. A critical database is on an isolated network reachable only via a secondary internal jump box. Establish a dynamic SOCKS proxy through a chain of two SSH tunnels, configure proxychains, and extract the flag from the database—all without writing any keys to disk.

---

## Node 15: Netcat, Socat & Data Relays
**Dependencies**: Node 14
**Focus**: Raw TCP/UDP connections, reverse shells, advanced relays.

**Incidents:**
1. **The Netcat Listener**: Start a basic TCP listener on port 4444 and pipe a text file to anyone who connects.
2. **File Transfer**: Transfer a 1GB binary file over the network using `nc` without using SCP/FTP.
3. **Port Scanning with Netcat**: Use `nc -zv` to scan ports 20-30 on a target when nmap is not installed.
4. **Basic Reverse Shell**: Execute a bash reverse shell (`nc -e` or `bash -i >& /dev/tcp/...`) back to your listener.
5. **Bind Shell**: Bind a bash shell to port 8888 on a compromised machine so you can connect to it anytime.
6. **Socat Bidirectional Relay**: Use `socat` to forward local port 8080 to remote port 80 on another server.
7. **Socat Encrypted Shell**: Upgrade a plaintext netcat shell to an encrypted OpenSSL shell using `socat`.
8. **Upgrading the TTY**: Use Python `pty` module and stty raw to upgrade a dumb netcat reverse shell into a fully interactive TTY (with tab completion).
9. **UDP Relaying**: Use `socat` to listen on UDP port 53 and forward it to a TCP port 53 backend.
10. **SOCKS Proxy via Socat**: Create a basic SOCKS proxy using socat to pivot into a network.
11. **Serial Port over IP**: Expose a local serial device `/dev/ttyUSB0` over a TCP socket using socat.
12. **Forking Listeners**: Make a `socat` listener fork child processes so it can handle multiple simultaneous connections.
13. **HTTP Request Manually**: Use raw `nc` to manually type an HTTP GET request and retrieve a webpage.
14. **Proxychains Basics**: Configure `proxychains.conf` to route `nc` traffic through an existing SOCKS proxy.
15. **Boss Fight: The Shell Game**: You need a stable, encrypted, fully interactive shell on a target that drops all outbound traffic except DNS. Use `socat` to create an encrypted bind shell, port forward it through a compromised intermediate host using raw relays, connect to it, and upgrade it to a full TTY.

---

## Node 16: VPNs & Secure Overlays (WireGuard)
**Dependencies**: Node 12
**Focus**: Cryptokey routing, WireGuard configuration, site-to-site.

**Incidents:**
1. **Key Generation**: Generate WireGuard private and public keys (`wg genkey`).
2. **Basic Interface**: Create a WireGuard interface (`wg0`), assign it an IP, and bring it up.
3. **Peer Configuration**: Add a peer to `wg0` specifying their public key and allowed IPs.
4. **Endpoint Update**: Set the remote endpoint IP and port for a peer to establish the tunnel.
5. **Routing All Traffic**: Configure `AllowedIPs = 0.0.0.0/0` on a client to route all internet traffic through the VPN.
6. **Persistent Keepalive**: Fix an issue where the tunnel drops when idle by setting `PersistentKeepalive = 25`.
7. **Wg-Quick**: Write a `wg0.conf` file and bring it up using `wg-quick`.
8. **Pre-shared Keys (PSK)**: Add a Post-Quantum resistant Pre-shared Key to an existing WireGuard tunnel for extra security.
9. **Firewall Rules in Config**: Add `PostUp` and `PostDown` iptables masquerade rules in the WireGuard config.
10. **Site-to-Site Routing**: Connect two subnets by configuring `AllowedIPs` on both routers to include the opposite subnet.
11. **MTU Tuning**: Packets are fragmenting over the tunnel. Calculate and set the correct MTU for `wg0`.
12. **Debugging Handshakes**: A tunnel is down. Use `tcpdump` and `wg show` to prove that the initiator's handshake is not getting a response.
13. **Dynamic IP Endpoints**: Use a dynamic DNS script to update the WireGuard endpoint when the ISP IP changes.
14. **Routing Loops**: Fix a routing loop caused when a WireGuard endpoint is routed *into* the WireGuard tunnel itself.
15. **Boss Fight: The Secure Mesh**: Connect 3 servers in a full-mesh WireGuard topology. Server A must route all internet traffic through Server B, while Server C only routes internal subnet traffic. Fix the overlapping IP conflicts, adjust MTUs for a strict ISP, and write the iptables rules to permit the traffic.

---

## Node 17: Traffic Shaping & Manipulation (`tc`, `netem`)
**Dependencies**: Node 6
**Focus**: Quality of Service (QoS), artificial latency, bandwidth limiting.

**Incidents:**
1. **Bandwidth Throttling**: Use `tc` (Traffic Control) with a TBF qdisc to limit `eth0` outbound speed to 10mbit.
2. **Artificial Latency**: Use `netem` to add 150ms of delay to an interface to simulate a satellite link.
3. **Packet Loss Simulation**: Configure `netem` to randomly drop 5% of packets to test application resilience.
4. **Packet Corruption & Reordering**: Introduce 2% packet corruption and reorder 1% of packets to break a poorly written UDP protocol.
5. **Removing Qdiscs**: Remove all traffic control rules from `eth0` to restore normal performance.
6. **HTB Class Basics**: Create a Hierarchical Token Bucket (HTB) root and two classes (high priority, low priority).
7. **Filtering Traffic to Classes**: Use `tc filter` to send SSH traffic to the high-priority class and HTTP to the low-priority class.
8. **Burst Rates**: Configure a burst rate in TBF to allow short spikes of 20mbit before throttling down to 5mbit.
9. **Ingress Policing**: Limit *incoming* bandwidth on an interface (harder than outbound shaping) using an ingress qdisc.
10. **Fq_Codel**: Replace the default pfifo_fast qdisc with `fq_codel` to solve bufferbloat on a router interface.
11. **Marking for TC**: Use iptables to mark packets, and use `tc filter fw` to assign those marked packets to specific bandwidth queues.
12. **Simulating Jitter**: Add 100ms delay with a 20ms jitter (variation) using `netem`.
13. **Duplicating Packets**: Use `netem` to duplicate 5% of packets to test duplicate-handling logic.
14. **Monitoring Queues**: Use `tc -s qdisc show dev eth0` to monitor dropped packets and queue lengths in real-time.
15. **Boss Fight: The Congested Pipe**: A video streaming service is choking out SSH access. Implement a complex HTB queueing discipline that guarantees 1mbit to SSH, caps video streaming at 50mbit, and applies `fq_codel` to prevent bufferbloat, all while simulating 50ms of realistic WAN latency.

---

## Node 18: Basic Protocol Exploitation & Brute-Forcing
**Dependencies**: Node 9
**Focus**: Dictionary attacks, Hydra, common misconfigurations.

**Incidents:**
1. **SSH Brute Force**: Use `hydra` with a small wordlist to crack a weak SSH password on a target.
2. **FTP Dictionary Attack**: Crack an FTP login using `medusa` or `hydra`.
3. **Web Form Login Bypass**: Use `hydra` to brute-force a basic HTTP POST login form on a web application.
4. **SNMP Community Strings**: Use `onesixtyone` or nmap to guess the SNMP community string (e.g., "public").
5. **SMB Null Session**: Connect to an SMB share using `smbclient` with a null session (no password) to enumerate users.
6. **RDP Brute Force**: Target a Windows machine's RDP port using `ncrack`.
7. **Database Cracking**: Brute-force a PostgreSQL or MySQL login.
8. **Wordlist Mutation**: Use `hashcat` rules or `john` to mutate a basic wordlist (e.g., add "123" to the end of words) before brute-forcing.
9. **Rate Limit Evasion**: Slow down `hydra` or use proxychains to rotate IPs and evade fail2ban during a dictionary attack.
10. **Redis Unauthenticated Access**: Connect to an exposed Redis instance using `redis-cli` and extract the keys.
11. **NFS Showmount**: Use `showmount -e` to find exposed NFS shares and mount them locally.
12. **RSync Module Enumeration**: Enumerate and sync an unprotected `rsync` module to read sensitive files.
13. **Telnet Hijack**: Find an open telnet port and log in using default IoT credentials (admin/admin).
14. **VNC No Authentication**: Connect to a VNC server that has authentication disabled.
15. **Boss Fight: The Weak Link**: You are given a target IP with 5 open ports. Identify the services, find the open NFS share to read a custom wordlist, use that wordlist to brute-force the HTTP admin panel, extract the DB password from the web config, and finally log into the database to retrieve the flag.

---

## Node 19: Intrusion Detection & Response (IDS/IPS, `fail2ban`)
**Dependencies**: Node 5, Node 11
**Focus**: Snort/Suricata rules, log parsing, automated bans.

**Incidents:**
1. **Fail2ban Setup**: Install `fail2ban` and enable the `sshd` jail to block IPs after 3 failed logins.
2. **Unbanning IPs**: A legitimate admin locked themselves out. Use `fail2ban-client` to unban their IP.
3. **Custom Fail2ban Filter**: Write a custom regex filter for `fail2ban` to catch failed logins in a custom Node.js app log.
4. **Suricata Basic Run**: Start `suricata` on an interface and review the `fast.log` for alerts.
5. **Writing an IDS Rule**: Write a custom Suricata rule to alert on any plaintext HTTP traffic containing the word "password".
6. **Detecting Port Scans**: Configure Suricata or Snort to detect and log an aggressive Nmap SYN scan.
7. **Log Rotation**: Configure `logrotate` for `/var/log/suricata` to prevent disk exhaustion.
8. **Zeek (Bro) Scripting**: Run `zeek` on a PCAP and extract the `http.log` to see all requested URLs.
9. **Malware Signature**: Write an IDS rule to detect a specific Hex pattern associated with a known C2 beacon.
10. **IPS Mode**: Configure Suricata in inline IPS mode (using NFQUEUE) to proactively drop malicious packets.
11. **Fail2ban Recidive**: Configure the `recidive` jail in fail2ban to permanently ban IPs that repeatedly get banned and unbanned.
12. **Auditd File Monitoring**: Use `auditd` to trigger an alert if `/etc/shadow` is read by a non-root user.
13. **Syslog Centralization**: Configure `rsyslog` to forward authentication logs to a central server.
14. **Detecting ICMP Tunnels**: Write a rule to detect unusually large ICMP echo requests indicating a ping tunnel.
15. **Boss Fight: The Red Team Assault**: You are defending a server. A red team script is launching dictionary attacks, SQL injections, and port scans. You must deploy Fail2ban with custom jails, write Suricata rules to drop the SQLi payloads in IPS mode, and maintain 100% uptime for legitimate traffic.

---

## Node 20: Capstone - The Red/Blue Chimera
**Dependencies**: All previous Nodes
**Focus**: Comprehensive mastery of networking, pivoting, defense, and exploitation.

**Incidents:**
1-14: *Preparation phases—mapping an unknown architecture, establishing persistence, bypassing initial firewalls, securing local infrastructure, compiling static binaries for pivoting, setting up VPN infrastructure.*

15. **Boss Fight: Operation Chimera**: 
You are dropped into a compromised DMZ host with no root access.
*Phase 1 (Red)*: Privilege escalate locally, map the internal corporate network without nmap (using raw bash/nc), pivot through a dual-homed server using an SSH dynamic proxy, and steal the Domain Controller's hashes.
*Phase 2 (Blue)*: The real attackers realize you are there and begin wiping the network. You must instantly pivot to defense—deploy iptables rules to sever the attacker's C2 connections, sinkhole their DNS requests using policy routing, restore the corrupted routing tables on the core router, and establish a secure WireGuard tunnel to the incident response team to exfiltrate the captured malware. 
Failure means the simulated data center is wiped. Success makes you a Master of the Terminal Academy Networking Branch.
