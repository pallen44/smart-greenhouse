# 🌿 Mini Smart Greenhouse + Digital Twin

A hands-on **personal engineering project** combining hardware, software, and plants.  
Built to learn, grow, and eventually scale into a fully self-sustaining greenhouse system.

---

## 🧭 Overview
The **Mini Smart Greenhouse** is a Raspberry Pi + ESP32-based system that automates watering, lighting, and climate control — all while mirroring real-world conditions in a digital twin simulation.

It starts as a small indoor greenhouse for herbs like basil and mint — but is designed to scale toward a future backyard greenhouse powered by renewable inputs and predictive automation.

---

## 🚀 Core Goals
- 🌱 Grow herbs and vegetables automatically.  
- 🧠 Learn IoT, data logging, and environmental control.  
- 💻 Build a **digital twin** to simulate temperature, humidity, and soil dynamics.  
- ⚡ Design for **scalability** — from desktop tent → full greenhouse.  
- 🌞 Move toward sustainability (solar, water recycling, nutrient dosing).

---

## 🧰 Tech Stack

| Layer | Tools & Components | Purpose |
|-------|--------------------|----------|
| **Hardware** | ESP32 · Raspberry Pi 3B+ · SHT31 · Capacitive soil probes · LED light · Pump · Fan | Sense & control environment |
| **Software** | ESPHome / MicroPython · Python · Docker | Firmware, control logic, simulation |
| **Services** | Mosquitto (MQTT) · InfluxDB · Grafana | Communication, data storage & visualization |
| **Frontend (Planned)** | React + Three.js (Digital Twin UI) | Interactive 3D greenhouse view |

---

## 🪜 Project Versions & Roadmap

### **v1 — Bench Prototype (MVP)**
> Focus: get sensors talking, visualize real data.
- [x] Raspberry Pi setup (Docker + MQTT + Grafana)  
- [x] ESP32 flashed & publishing data  
- [ ] Air Temp / RH / Soil Moisture telemetry  
- [ ] Simple auto-watering rule  
- [ ] Grafana dashboard online  

### **v2 — Full Mini-Greenhouse Automation**
> Focus: closed-loop control and digital twin foundation.
- [ ] Install all sensors + drip system in greenhouse  
- [ ] Add fan / humidifier control  
- [ ] Build Python control service (PID + rules)  
- [ ] Log data to InfluxDB automatically  
- [ ] Create Digital Twin v1 (Python simulation)

### **v3 — Visualization & Prediction**
> Focus: show it all visually and start simulating future states.
- [ ] Web dashboard or React + Three.js frontend  
- [ ] Sync live MQTT → 3D model (digital twin UI)  
- [ ] Compare predicted vs actual environment  
- [ ] Implement data-driven watering optimization

### **v4 — Self-Sustaining Expansion**
> Focus: scale up + sustainability.
- [ ] Add solar / battery monitoring  
- [ ] Add nutrient control + CO₂ sensor  
- [ ] Multiple zones / micro-controllers  
- [ ] Outdoor greenhouse integration  

---

## 📈 Current Status
| Component | Progress |
|------------|-----------|
| Raspberry Pi Server | 🟩 Configured |
| ESP32 Node | 🟨 Setting up |
| Sensors | 🟨 Ordering / Testing |
| Greenhouse Enclosure | 🟩 Selected |
| Control Logic | ⬜ Planned |
| Digital Twin | ⬜ Planned |

---

## 💡 Future Ideas
- Camera + image-based plant growth detection  
- Predictive watering via AI model  
- Home Assistant integration  
- Sustainability dashboard (energy / water usage)  
- Publish open-source guide once mature  

---

## 👤 Author
**Parker Allen**  
📍 Computer Science + Math student, UNL  
🎯 Interests: IoT · Automation · Sustainability · Digital Twins  
💬 _“Blending code, data, and design to grow something real.”_

---

### 🪴 License
This project is for personal and educational use.  
Feel free to fork, remix, or build your own version — just link back here!

---


## 📂 Repository Structure
