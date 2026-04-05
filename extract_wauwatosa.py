import re, json

p = 'C:/Users/Mike/OneDrive/Documents/DATA/Developer/PizzaMan/toast_wauwtosa.html'
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

print(f'File size: {len(html)} chars')

# Find all window.__ state variables
state_vars = re.findall(r'window\.__(\w+)__\s*=', html)
print('State vars:', state_vars)

# Try all the OO_STATE
matches = re.findall(r'window\.__OO_STATE__\s*=\s*(\{[\s\S]{100,}?\});\s*(?:window|</script|$)', html)
if matches:
    blob = matches[0]
    print(f'OO_STATE blob len={len(blob)}')
    try:
        data = json.loads(blob)
        rq = data.get('ROOT_QUERY', {})
        for k, v in rq.items():
            if 'restaurant' in k.lower():
                loc = v.get('location', {}) if isinstance(v, dict) else {}
                name = v.get('name','') if isinstance(v, dict) else ''
                phone = loc.get('phone','') if isinstance(loc, dict) else ''
                addr = f"{loc.get('address1','')} {loc.get('city','')} {loc.get('state','')} {loc.get('zip','')}" if isinstance(loc, dict) else ''
                desc = v.get('description','') if isinstance(v, dict) else ''
                print(f'Restaurant: {name}')
                print(f'Phone: {phone}')
                print(f'Address: {addr}')
                print(f'Description: {desc}')
                sched = v.get('schedule', {}) if isinstance(v, dict) else {}
                if isinstance(sched, dict):
                    for upcoming in sched.get('upcomingSchedules', []):
                        behav = upcoming.get('behavior','')
                        print(f'\nSchedule ({behav}):')
                        for day in upcoming.get('dailySchedules', []):
                            date = day.get('date','')
                            periods = day.get('servicePeriods', [])
                            if periods:
                                for sp in periods:
                                    print(f'  {date}: {sp.get("startTime","")} - {sp.get("endTime","")}')
    except Exception as e:
        print('Error:', e)
        print(blob[:1000])
else:
    print('No OO_STATE - checking raw HTML')
    # Find restaurant data
    names = re.findall(r'"name"\s*:\s*"([^"]*Wauwatosa[^"]*)"', html)
    print('Wauwatosa mentions:', names)
    print(html[:2000])
