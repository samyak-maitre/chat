# 🚢 Ship Proxy System

This project implements a cost-cutting proxy system for cruise ships.  
It reuses a single persistent TCP connection to the offshore proxy server, ensuring only one TCP connection is billed by the satellite provider.

---

## 📂 Structure
ship-proxy-system/
├── client/ # Ship proxy (exposes :8080)
├── server/ # Offshore proxy (exposes :9999)


---

## 🔧 Build & Run with Docker

### 1. Build Images
```sh
docker build -t ship-proxy ./client
docker build -t offshore-proxy ./server
