"""
Traffic Vehicle Simulator - Kathmandu Valley
Simulates 100 vehicles, accidents, violations, and traffic signals.
"""

import requests
import time
import random
import math
import os
import sys

API_BASE = "http://127.0.0.1:8000/api"

# ── CONFIG ──
NUM_VEHICLES = 100
vehicles = {}

ROADS = [
    {"name": "Ring Road North",   "start": (27.7300, 85.3100), "end": (27.7300, 85.3400)},
    {"name": "Ring Road South",   "start": (27.6900, 85.3100), "end": (27.6900, 85.3400)},
    {"name": "Ring Road East",    "start": (27.6950, 85.3450), "end": (27.7300, 85.3450)},
    {"name": "Ring Road West",    "start": (27.6950, 85.2850), "end": (27.7300, 85.2850)},
    {"name": "Durbar Marg",       "start": (27.7120, 85.3140), "end": (27.7200, 85.3200)},
    {"name": "Kantipath",         "start": (27.7050, 85.3150), "end": (27.7200, 85.3150)},
    {"name": "Maharajgunj",       "start": (27.7250, 85.3250), "end": (27.7350, 85.3350)},
    {"name": "Balaju",            "start": (27.7250, 85.3050), "end": (27.7350, 85.3100)},
    {"name": "Kalanki",           "start": (27.6950, 85.2800), "end": (27.7050, 85.3000)},
    {"name": "Koteshwor",         "start": (27.6750, 85.3400), "end": (27.6900, 85.3500)},
    {"name": "New Baneshwor",     "start": (27.6900, 85.3300), "end": (27.7000, 85.3400)},
    {"name": "Thamel",            "start": (27.7150, 85.3100), "end": (27.7220, 85.3150)},
    {"name": "Lazimpat",          "start": (27.7200, 85.3200), "end": (27.7280, 85.3250)},
    {"name": "Patan Dhoka",       "start": (27.6750, 85.3200), "end": (27.6850, 85.3280)},
    {"name": "Satdobato",         "start": (27.6600, 85.3250), "end": (27.6750, 85.3300)},
    {"name": "Chabahil",          "start": (27.7180, 85.3400), "end": (27.7250, 85.3480)},
]

LANES = ["Left", "Right", "Center"]

SEVERITIES = ["Minor", "Moderate", "Severe", "Fatal"]
SEVERITY_WEIGHTS = [0.45, 0.30, 0.18, 0.07]

ACCIDENT_DESCRIPTIONS = {
    "Minor": [
        "Minor fender bender, no injuries",
        "Low-speed rear-end collision",
        "Side mirror clipped, minor scratch",
        "Vehicle bumped at traffic signal",
        "Slow-speed sideswipe near intersection",
    ],
    "Moderate": [
        "Two-vehicle collision, minor injuries reported",
        "Vehicle hit road divider at moderate speed",
        "Sideswipe collision, driver injured",
        "Motorcycle slipped on wet road",
        "Auto-rickshaw overturned, passengers shaken",
    ],
    "Severe": [
        "Head-on collision, multiple injuries",
        "Vehicle rolled over, passengers trapped",
        "High-speed crash into barrier",
        "Multi-vehicle pileup, road blocked",
        "Bus brakes failed, crashed into divider",
    ],
    "Fatal": [
        "Fatal head-on collision",
        "Pedestrian struck at high speed",
        "Bus overturned, critical casualties",
        "Truck collision, fatalities reported",
    ],
}

INJURY_RANGES = {
    "Minor": (0, 0),
    "Moderate": (0, 2),
    "Severe": (1, 5),
    "Fatal": (1, 8),
}

VIOLATION_TYPES = [
    {"type": "Overspeeding",  "video": "overspeed_clip.mp4",  "fine": 1500, "min_speed": 80},
    {"type": "Wrong Lane",    "video": "wronglane_clip.mp4",  "fine": 1000, "min_speed": 0},
    {"type": "Red Light",     "video": "overspeed_clip.mp4",  "fine": 2000, "min_speed": 0},
    {"type": "No Helmet",     "video": "wronglane_clip.mp4",  "fine": 500,  "min_speed": 0},
]

TRAFFIC_SIGNALS = [
    {"name": "Kalanki Chowk",     "lat": 27.6934, "lng": 85.2815},
    {"name": "Koteshwor Chowk",   "lat": 27.6790, "lng": 85.3490},
    {"name": "Maharajgunj Chowk", "lat": 27.7268, "lng": 85.3275},
    {"name": "Thapathali",        "lat": 27.6950, "lng": 85.3200},
    {"name": "Baneshwor Chowk",   "lat": 27.6930, "lng": 85.3370},
    {"name": "Chabahil Chowk",    "lat": 27.7195, "lng": 85.3425},
    {"name": "Balaju Chowk",      "lat": 27.7275, "lng": 85.3070},
    {"name": "Thamel Chowk",      "lat": 27.7160, "lng": 85.3120},
    {"name": "Satdobato Chowk",   "lat": 27.6650, "lng": 85.3260},
    {"name": "Patan Gate",        "lat": 27.6780, "lng": 85.3230},
]


def setup_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'traffic_system.settings')
    import django
    django.setup()


def init_signals():
    from core.models import TrafficSignal
    for sig in TRAFFIC_SIGNALS:
        TrafficSignal.objects.get_or_create(
            name=sig["name"],
            defaults={"lat": sig["lat"], "lng": sig["lng"], "state": "Green", "cycle_time": 60}
        )
    print(f"  Signals: {TrafficSignal.objects.count()} initialized")


def cycle_signals():
    from core.models import TrafficSignal
    states = ["Green", "Green", "Green", "Yellow", "Red", "Red", "Red"]
    for sig in TrafficSignal.objects.all():
        sig.state = random.choice(states)
        sig.save()


def init_vehicles():
    for i in range(NUM_VEHICLES):
        vid = f"BA-{random.randint(1, 9)}-PA-{random.randint(1000, 9999)}"
        road = random.choice(ROADS)
        t = random.random()
        lat = road["start"][0] + t * (road["end"][0] - road["start"][0])
        lng = road["start"][1] + t * (road["end"][1] - road["start"][1])

        dlat = road["end"][0] - road["start"][0]
        dlng = road["end"][1] - road["start"][1]
        heading = math.degrees(math.atan2(dlng, dlat)) % 360

        vehicles[vid] = {
            "lat": lat,
            "lng": lng,
            "speed": random.uniform(20, 70),
            "heading": heading,
            "road": road,
            "direction": random.choice([1, -1]),
            "lane": random.choice(LANES),
            "progress": t,
        }


def move_vehicles():
    for vid, v in vehicles.items():
        road = v["road"]

        # Speed variation
        v["speed"] += random.uniform(-5, 5)
        v["speed"] = max(5, min(120, v["speed"]))

        # Traffic slowdowns
        if random.random() < 0.08:
            v["speed"] = random.uniform(5, 15)

        # Rush hour bursts
        if random.random() < 0.03:
            v["speed"] = random.uniform(80, 110)

        # Move along road
        step = v["speed"] * 0.00001 * v["direction"]
        v["progress"] += step

        if v["progress"] > 1 or v["progress"] < 0:
            v["direction"] *= -1
            v["progress"] = max(0, min(1, v["progress"]))
            if random.random() < 0.3:
                v["road"] = random.choice(ROADS)
                road = v["road"]
                v["progress"] = random.random()
                dlat = road["end"][0] - road["start"][0]
                dlng = road["end"][1] - road["start"][1]
                v["heading"] = math.degrees(math.atan2(dlng, dlat)) % 360

        t = v["progress"]
        v["lat"] = road["start"][0] + t * (road["end"][0] - road["start"][0])
        v["lng"] = road["start"][1] + t * (road["end"][1] - road["start"][1])
        v["lat"] += random.uniform(-0.0003, 0.0003)
        v["lng"] += random.uniform(-0.0003, 0.0003)


def update_server():
    for vid, v in vehicles.items():
        try:
            requests.post(f"{API_BASE}/update/", json={
                "vehicle_id": vid,
                "lat": round(v["lat"], 6),
                "lng": round(v["lng"], 6),
                "speed": round(v["speed"], 1),
                "heading": round(v["heading"], 1),
            }, timeout=2)
        except requests.RequestException:
            pass


def generate_accident():
    if random.random() < 0.05:
        from core.models import Accident

        pending = Accident.objects.filter(status="Pending").count()
        if pending >= 5:
            return

        vid = random.choice(list(vehicles.keys()))
        v = vehicles[vid]
        road_name = v["road"]["name"]
        severity = random.choices(SEVERITIES, weights=SEVERITY_WEIGHTS, k=1)[0]
        description = random.choice(ACCIDENT_DESCRIPTIONS[severity])
        injuries = random.randint(*INJURY_RANGES[severity])

        Accident.objects.create(
            vehicle=vid,
            lat=round(v["lat"], 6),
            lng=round(v["lng"], 6),
            road_name=road_name,
            severity=severity,
            description=description,
            injuries=injuries,
        )
        print(f"\n  [ACCIDENT] {severity.upper()} - {vid} on {road_name} ({injuries} injuries)")


def generate_violation():
    if random.random() < 0.08:
        from core.models import Violation

        total = Violation.objects.count()
        if total >= 30:
            return

        vid = random.choice(list(vehicles.keys()))
        v = vehicles[vid]

        if v["speed"] > 80:
            vtype = VIOLATION_TYPES[0]  # Overspeeding
        else:
            vtype = random.choice(VIOLATION_TYPES)
            if vtype["type"] == "Overspeeding":
                v["speed"] = random.uniform(85, 120)

        Violation.objects.create(
            vehicle=vid,
            lat=round(v["lat"], 6),
            lng=round(v["lng"], 6),
            speed=round(v["speed"], 1),
            lane=v["lane"],
            violation_type=vtype["type"],
            video_clip=vtype["video"],
            fine_amount=vtype["fine"],
        )
        print(f"\n  [VIOLATION] {vtype['type']} - {vid} ({v['speed']:.0f} km/h) Fine: Rs.{vtype['fine']}")


def main():
    print("=" * 55)
    print("   Kathmandu Traffic Simulator")
    print("   Vehicles: %d | Roads: %d | Signals: %d" % (NUM_VEHICLES, len(ROADS), len(TRAFFIC_SIGNALS)))
    print("=" * 55)

    setup_django()
    init_signals()
    init_vehicles()

    print(f"  Vehicles: {len(vehicles)} initialized")
    print("  Press Ctrl+C to stop\n")

    tick = 0
    while True:
        try:
            move_vehicles()
            update_server()

            if tick % 3 == 0:
                generate_accident()
            if tick % 2 == 0:
                generate_violation()
            if tick % 5 == 0:
                cycle_signals()

            tick += 1
            speeds = [v["speed"] for v in vehicles.values()]
            avg = sum(speeds) / len(speeds)
            fast = sum(1 for s in speeds if s > 80)
            slow = sum(1 for s in speeds if s < 20)

            sys.stdout.write(
                f"\r  [Tick {tick:04d}] "
                f"Vehicles: {len(vehicles)} | "
                f"Avg: {avg:.0f} km/h | "
                f"Fast: {fast} | "
                f"Slow: {slow}   "
            )
            sys.stdout.flush()

            time.sleep(2)

        except KeyboardInterrupt:
            print("\n\n  Simulator stopped.")
            break
        except Exception as e:
            print(f"\n  Error: {e}")
            time.sleep(2)


if __name__ == "__main__":
    main()
