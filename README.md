# NetBot - Computer Network Assistant

A chatbot for computer networks: OSI/TCP-IP, IP addressing and subnetting, TCP/UDP, routing and switching,
DNS/DHCP/HTTP/TLS, security, Wi-Fi/LAN and troubleshooting. Streaming AI replies, topic suggestions,
a built-in **subnet calculator**, and an **offline mode** that works with no API key.

## Run it

- **Windows:** double-click `Start NetBot.bat`
- **Mac / Linux:** `./start.sh`  (or `python3 server.py`)

Opens at http://127.0.0.1:8000. Needs Python 3.8+ and nothing else (no pip install).

## AI key (optional)

Copy `.env.example` to `.env` and set `AI_API_KEY=...`. xAI Grok (`xai-...`) and Groq (`gsk_...`, free tier) are
detected from the key. Without a key, NetBot answers core topics from built-in notes and calculates any CIDR you type.

## Settings (.env)

`AI_MODEL` overrides the model, `PORT` changes the port, `AI_PROVIDER=xai|groq` forces a provider.
The key stays in `.env`, is used only by `server.py`, and the server listens on 127.0.0.1 only. Never share `.env`.
