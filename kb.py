"""Built-in offline knowledge base for NetBot (used when no API key is set)."""
import re

KB = [
 (("osi", "layers of", "seven layer", "7 layer"),
  "**The OSI model** has 7 layers, top to bottom:\n\n1. **Application**: user-facing protocols (HTTP, DNS, SMTP)\n2. **Presentation**: encoding, compression, encryption (TLS is often placed here)\n3. **Session**: opens, manages and closes sessions\n4. **Transport**: end-to-end delivery, ports (TCP, UDP)\n5. **Network**: logical addressing and routing (IP, ICMP). Data unit: packet\n6. **Data Link**: framing and MAC addressing on one link (Ethernet, Wi-Fi). Data unit: frame\n7. **Physical**: bits on the wire, signals, cables\n\nMemory aid, top to bottom: *All People Seem To Need Data Processing*."),
 (("tcp/ip", "tcp ip model", "internet model", "osi vs tcp", "compare osi"),
  "**The TCP/IP model** has 4 layers: **Application** (HTTP, DNS, SMTP), **Transport** (TCP, UDP), **Internet** (IP, ICMP, ARP-adjacent) and **Link** (Ethernet, Wi-Fi). It maps to OSI as: Application = OSI 5-7, Transport = 4, Internet = 3, Link = 1-2. OSI is the teaching reference; TCP/IP is what the Internet actually runs."),
 (("tcp vs udp", "udp vs tcp", "difference between tcp and udp", "tcp and udp"),
  "**TCP vs UDP**\n\n- **TCP**: connection-oriented, reliable, ordered, flow and congestion control, 3-way handshake. Used by HTTP(S), SSH, SMTP, FTP.\n- **UDP**: connectionless, no delivery guarantee, no ordering, tiny header (8 bytes). Used by DNS, DHCP, VoIP, video streaming, games, QUIC.\n\nUse TCP when every byte must arrive correctly; use UDP when speed matters more than perfection."),
 (("three way", "3 way", "3-way", "handshake", "syn"),
  "**TCP 3-way handshake**\n\n1. Client sends **SYN** (seq = x)\n2. Server replies **SYN-ACK** (seq = y, ack = x+1)\n3. Client sends **ACK** (ack = y+1)\n\nAfter this the connection is ESTABLISHED. Closing uses FIN/ACK in each direction (4 steps)."),
 (("tcp",),
  "**TCP (Transmission Control Protocol)** gives reliable, ordered, byte-stream delivery over IP. It uses sequence numbers and acknowledgements, retransmits lost segments, controls flow with a receive window and controls congestion (slow start, congestion avoidance, fast retransmit). Connections start with a 3-way handshake."),
 (("udp",),
  "**UDP (User Datagram Protocol)** is a minimal, connectionless transport: 8-byte header (source port, destination port, length, checksum), no handshake, no retransmission, no ordering. Fast and light, so it suits DNS, DHCP, VoIP, streaming and games."),
 (("subnet", "cidr", "vlsm", "netmask", "subnet mask"),
  "**Subnetting basics**\n\nA CIDR prefix like `/26` means the first 26 bits are the network part, so 6 bits are left for hosts.\n\n- Usable hosts = 2^(host bits) - 2\n- Block size = 256 - last mask octet (for /26 the mask is 255.255.255.192, block = 64)\n- Network address = all host bits 0; broadcast = all host bits 1\n\nExample: `192.168.1.100/26` has network 192.168.1.64, broadcast 192.168.1.127, hosts .65 to .126 (62 hosts).\n\nTry the **Subnet calculator** or type any CIDR such as `10.0.0.0/22` and I will compute it."),
 (("ipv6",),
  "**IPv6** uses 128-bit addresses written in 8 groups of hex (`2001:db8::1`; `::` replaces one run of zeros). No broadcast (uses multicast), built-in SLAAC auto-configuration, no NAT needed, simpler fixed 40-byte header. A typical LAN uses a /64 prefix."),
 (("ipv4", "ip address", "ip class", "private ip", "private address"),
  "**IPv4** addresses are 32 bits (`192.168.1.10`). Classes: A 1-126 (/8), B 128-191 (/16), C 192-223 (/24), D 224-239 multicast, E reserved. **Private ranges** (RFC 1918): `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`. `127.0.0.0/8` is loopback and `169.254.0.0/16` is link-local (APIPA)."),
 (("dns", "domain name"),
  "**DNS** translates names to IP addresses. A lookup goes: your stub resolver -> recursive resolver (cache) -> root server -> TLD server (.com) -> authoritative server, then the answer is cached for its TTL. Common records: **A** (IPv4), **AAAA** (IPv6), **CNAME** (alias), **MX** (mail), **NS** (name server), **TXT**. Uses UDP/TCP port 53."),
 (("dhcp",),
  "**DHCP** hands out IP configuration automatically using four steps, **DORA**: *Discover* (client broadcast), *Offer* (server), *Request* (client), *Acknowledge* (server). It supplies IP, mask, gateway and DNS. Uses UDP ports 67 (server) and 68 (client)."),
 (("nat", "pat", "network address translation"),
  "**NAT** rewrites addresses so many private hosts share one public IP. **PAT** (NAT overload) also rewrites the source port, so the router tracks each flow in a translation table. It saves IPv4 addresses but breaks end-to-end addressing, which IPv6 restores."),
 (("arp",),
  "**ARP** maps an IPv4 address to a MAC address on the local link. The host broadcasts *who has 192.168.1.1?*, the owner replies with its MAC (unicast), and the result is cached. ARP only works inside one broadcast domain."),
 (("router", "routing", "ospf", "rip", "bgp", "routing table"),
  "**Routing** moves packets between networks using a routing table and *longest prefix match*. **Static** routes are set by hand; **dynamic** protocols learn them: **RIP** (distance vector, hop count, max 15), **OSPF** (link state, Dijkstra, cost from bandwidth, interior), **BGP** (path vector, between autonomous systems, runs the Internet)."),
 (("switch", "hub", "mac address", "vlan"),
  "**Hub vs switch vs router**: a hub repeats bits to every port (L1); a switch learns MAC addresses and forwards frames only to the right port (L2); a router forwards packets between networks by IP (L3). A **VLAN** splits one switch into separate broadcast domains; trunk links carry several VLANs using 802.1Q tags."),
 (("http", "https", "web request", "rest"),
  "**HTTP** is the web's request/response protocol (port 80). Methods: GET, POST, PUT, DELETE. Status codes: 2xx success, 3xx redirect, 4xx client error (404), 5xx server error (500). **HTTPS** is HTTP inside TLS (port 443) for encryption and server authentication."),
 (("tls", "ssl", "encryption", "certificate"),
  "**TLS** secures a connection: the client and server agree on a cipher, the server proves its identity with a certificate signed by a trusted CA, they derive a shared session key (asymmetric crypto), then all data is encrypted with fast symmetric crypto. HTTPS = HTTP over TLS."),
 (("firewall", "security", "attack", "ddos", "vpn"),
  "**Network security basics**: a **firewall** filters traffic by rules (IP, port, protocol, state). A **VPN** builds an encrypted tunnel across an untrusted network. Common attacks: DDoS (flood), ARP spoofing, DNS poisoning, man-in-the-middle, port scanning. Defences: encryption (TLS), segmentation (VLANs), least-privilege rules, patching, IDS/IPS."),
 (("wifi", "wi-fi", "wireless", "802.11"),
  "**Wi-Fi (IEEE 802.11)** uses CSMA/CA (avoid collisions, since radios cannot listen while sending). Bands: 2.4 GHz (longer range, crowded), 5 GHz and 6 GHz (faster). Security: prefer WPA3 or WPA2-AES; WEP is broken."),
 (("ping", "icmp", "traceroute", "tracert"),
  "**ICMP** carries control messages. `ping` sends Echo Request and waits for Echo Reply to test reachability and round-trip time. `traceroute` (`tracert` on Windows) sends packets with TTL 1, 2, 3... and reads the *Time Exceeded* replies to list each hop."),
 (("port", "ports"),
  "**Common ports**: 20/21 FTP, 22 SSH, 23 Telnet, 25 SMTP, 53 DNS, 67/68 DHCP, 80 HTTP, 110 POP3, 143 IMAP, 443 HTTPS, 3389 RDP. Well-known: 0-1023, registered: 1024-49151, dynamic: 49152-65535."),
 (("ethernet", "csma", "frame", "mac"),
  "**Ethernet** frames carry destination MAC, source MAC, type, payload (46-1500 bytes) and a CRC. Classic Ethernet used **CSMA/CD** (listen, send, detect collision, back off); modern full-duplex switched Ethernet has no collisions."),
 (("bandwidth", "latency", "throughput", "delay"),
  "**Bandwidth** is link capacity (bits/s). **Throughput** is what you actually achieve. **Latency** = transmission delay (L/R) + propagation delay (d/s) + queuing + processing. Example: 1500 bytes over 10 Mbps = 12,000 / 10,000,000 = 1.2 ms transmission delay."),
 (("topology", "star", "bus", "ring", "mesh"),
  "**Topologies**: *bus* (one shared cable, cheap, single point of failure), *star* (all nodes to a central switch, the modern LAN), *ring* (each node to two neighbours), *mesh* (many links, very resilient, costly), *tree* (hierarchy of stars)."),
]

HELP = ("I am running in **offline mode** (no AI key set), so I can answer core networking topics from my built-in notes: "
        "OSI/TCP-IP, TCP vs UDP, handshake, subnetting, IPv4/IPv6, DNS, DHCP, NAT, ARP, routing, switching/VLAN, HTTP/TLS, "
        "ports, Wi-Fi, ICMP, security, latency. You can also type a CIDR like `192.168.10.0/26` and I will calculate it.\n\n"
        "Add an API key in `.env` for free-form answers to any question.")


def offline_answer(text):
    low = " " + re.sub(r"[^a-z0-9/.\- ]", " ", text.lower()) + " "
    best, score = None, 0
    for keys, ans in KB:
        s = sum(len(k) for k in keys if (" " + k + " ") in low or (len(k) > 4 and k in low))
        if s > score:
            best, score = ans, s
    return best or HELP
