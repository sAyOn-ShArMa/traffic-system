# Smart Traffic Management System - Kathmandu Valley

A real-time traffic monitoring and emergency response system built with Django, featuring live vehicle tracking, accident detection, violation recording, congestion heatmaps, and multi-unit emergency dispatch across the Kathmandu road network.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.x-092E20?style=for-the-badge&logo=django&logoColor=white)
![Leaflet](https://img.shields.io/badge/Leaflet.js-1.9.4-199900?style=for-the-badge&logo=leaflet&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-Proprietary-red?style=for-the-badge)

---

## Features

### Live Vehicle Tracking
- 100 vehicles tracked in real-time across 16 Kathmandu road segments
- Speed-coded markers: Green (safe) / Yellow (moderate) / Red (overspeeding)
- Vehicle heading and position updated every 2 seconds

### Accident Detection & Location
- Automatic accident detection with GPS coordinates and road name
- 4 severity levels: Minor, Moderate, Severe, Fatal
- Pulsing animated markers sized by severity
- Danger zone circles around accident sites
- Injury count tracking
- Detailed accident descriptions

### Multi-Unit Emergency Dispatch
- 6 dispatch options per accident:
  - Ambulance
  - Police
  - Fire Truck
  - Traffic Police
  - Tow Truck
  - Rescue Team
- Multiple units can be dispatched simultaneously
- Status tracks all dispatched units
- One-click resolve removes accident from map and panel

### Traffic Violation Recording
- 4 violation types: Overspeeding, Wrong Lane, Red Light, No Helmet
- Fine amounts assigned per violation type
- Video evidence links
- GPS location and speed logged

### Congestion Heatmap
- Live heatmap generated from slow-moving vehicles (< 20 km/h)
- Color-graded: Green to Red intensity

### Traffic Signal Monitoring
- 10 traffic signals across major Kathmandu chowks
- Live Red / Yellow / Green state display on map

### Command Center Dashboard
- Dark-themed panel with live stats
- Accident and Violation tabs with live counts
- Layer toggle buttons (Vehicles, Accidents, Violations, Heatmap, Signals)
- Locate button flies to accident GPS location with highlight animation
- LIVE indicator with blinking dot

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python, Django 4.x |
| Frontend | HTML5, CSS3, JavaScript |
| Map | Leaflet.js 1.9.4, CARTO Dark Tiles |
| Heatmap | Leaflet.heat |
| Database | SQLite |
| Simulator | Python (requests, random, math) |

---

## Project Structure

```
traffic_system/
│
├── core/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── migrations/
│   │   └── __init__.py
│   └── static/
│       └── videos/
│           ├── overspeed_clip.mp4
│           └── wronglane_clip.mp4
│
├── traffic_system/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── templates/
│   └── map.html
│
├── vehicle_simulator.py
├── manage.py
└── README.md
```

---

## Database Models

| Model | Fields |
|-------|--------|
| **Vehicle** | vehicle_id, lat, lng, speed, heading, last_updated |
| **Accident** | vehicle, lat, lng, road_name, severity, description, injuries, time, status, resolved_at |
| **Violation** | vehicle, lat, lng, speed, lane, violation_type, video_clip, fine_amount, time |
| **TrafficSignal** | name, lat, lng, state, cycle_time |

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/stats/` | GET | Dashboard statistics |
| `/api/vehicles/` | GET | All vehicle positions and speeds |
| `/api/update/` | POST | Update vehicle position |
| `/api/accidents/` | GET | All accident records |
| `/api/violations/` | GET | All violation records |
| `/api/congestion/` | GET | Congestion heatmap data |
| `/api/signals/` | GET | Traffic signal states |
| `/api/dispatch/` | POST | Dispatch emergency unit to accident |
| `/api/resolve/` | POST | Resolve and remove accident |

---

## Installation & Setup

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/traffic-management-system.git
cd traffic-management-system
```

### Step 2: Install Dependencies

```bash
pip install django requests
```

### Step 3: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Create Admin User (Optional)

```bash
python manage.py createsuperuser
```

### Step 5: Start Django Server

```bash
python manage.py runserver
```

### Step 6: Start Vehicle Simulator (New Terminal)

```bash
python vehicle_simulator.py
```

### Step 7: Open Dashboard

```
http://127.0.0.1:8000/
```

Admin Panel:
```
http://127.0.0.1:8000/admin/
```

---

## Screenshots

### Dashboard Overview
- Dark-themed map with CARTO tiles
- 100 vehicles with color-coded speed markers
- Command panel with live stats, accident cards, and dispatch buttons

### Accident Tracking
- Pulsing severity-coded markers on map
- Danger zone circles sized by severity
- Locate button flies to exact GPS location
- Multi-unit dispatch with green confirmation

### Congestion Heatmap
- Color-graded overlay showing traffic bottlenecks
- Real-time updates based on vehicle speeds

---

## System Flowchart

```
System Startup
      │
      ▼
Simulator Launches (100 Vehicles, 16 Roads)
      │
      ▼
Vehicles Move in Real-Time
      │
      ▼
Events Auto-Generated (Accidents / Violations)
      │
      ▼
Data Sent to Django API
      │
      ▼
Stored in SQLite Database
      │
      ▼
Dashboard Fetches Every 2 Seconds
      │
      ▼
Operator Views Live Data
      │
      ├── Locate (Fly to GPS)
      ├── Dispatch (1-6 Units)
      └── Resolve (Remove from Map)
      │
      ▼
System Loops Continuously
```

---

## Configuration

| Setting | Default | File |
|---------|---------|------|
| Number of vehicles | 100 | `vehicle_simulator.py` |
| Refresh interval | 2 seconds | `templates/map.html` |
| Max pending accidents | 5 | `vehicle_simulator.py` |
| Max violations | 30 | `vehicle_simulator.py` |
| Accident probability | 5% per tick | `vehicle_simulator.py` |
| Violation probability | 8% per tick | `vehicle_simulator.py` |
| Map tile | CARTO Dark | `templates/map.html` |

---

## Developed By

**Radiants**

---

## License

Copyright (c) 2025 **Radiants**. All rights reserved.

This software and its associated documentation files (the "Software") are the proprietary property of **Radiants**. Unauthorized copying, modification, distribution, or use of this Software, in whole or in part, via any medium, is strictly prohibited without the prior written permission of **Radiants**.

The Software is provided "AS IS", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement.

For licensing inquiries, contact **Radiants**.
