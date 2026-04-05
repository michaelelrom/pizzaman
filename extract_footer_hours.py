import re, json

p = 'C:/Users/Mike/.claude/projects/c--Users-Mike-OneDrive-Documents-DATA-Developer-PizzaMan/7029caca-a04d-4bbc-9355-1bdd966b6e50/tool-results/bd3yuhfxo.txt'
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

matches = re.findall(r'window\.__[A-Z_]+__\s*=\s*(\{[\s\S]{100,}?\});\s*(?:window|</script|$)', html)
blob = matches[0]
data = json.loads(blob)

rest_key = [k for k in data.keys() if k.startswith('Restaurant:')][0]
rest = data[rest_key]
content = rest.get('content', {})

# Footer
footer = content.get('footerConfig', {})
print('=== FOOTER CONFIG ===')
print(json.dumps(footer, indent=2))

# Nav config
nav = content.get('navConfig', {})
print('\n=== NAV CONFIG ===')
print(json.dumps(nav, indent=2)[:2000])

# Spotlight banner
spotlight = content.get('spotlightBanner', {})
print('\n=== SPOTLIGHT BANNER ===')
print(json.dumps(spotlight, indent=2))

# Location schedule (from RestaurantLocation)
loc_key = [k for k in data.keys() if k.startswith('RestaurantLocation:')][0]
loc = data[loc_key]
print('\n=== LOCATION SCHEDULE ===')
print(f'Name: {loc.get("name")}')
print(f'Address: {loc.get("address1")}, {loc.get("city")}, {loc.get("state")} {loc.get("zipcode")}')
print(f'Phone: {loc.get("phoneNumber")}')
print(f'Lat/Lng: {loc.get("lat")}, {loc.get("long")}')
print(f'Social URLs: {loc.get("meta", {}).get("urls", [])}')
print('\nSchedule:')
for sched in loc.get('schedule', []):
    days = sched.get('days', [])
    for interval in sched.get('intervals', []):
        start = interval.get('startTime','')
        end = interval.get('endTime','')
        print(f'  {", ".join(days)}: {start} - {end}')
