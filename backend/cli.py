"""Your original script, upgraded: python cli.py +27821234567 [--map]"""
import argparse
import json

import folium

from app.service import InvalidNumber, analyze

p = argparse.ArgumentParser(description="Phone number intelligence")
p.add_argument("number")
p.add_argument("--region", help="default region for local numbers, e.g. ZA")
p.add_argument("--map", action="store_true", help="save mynumberlocation.html")
a = p.parse_args()
try:
    d = analyze(a.number, a.region)
except InvalidNumber as e:
    raise SystemExit(f"Invalid number: {e}")
print(json.dumps(d, indent=2))
if a.map and d["coordinates"]:
    c = d["coordinates"]
    m = folium.Map(location=[c["lat"], c["lng"]], zoom_start=9)
    folium.Marker([c["lat"], c["lng"]], popup=d["location"]).add_to(m)
    m.save("mynumberlocation.html")
