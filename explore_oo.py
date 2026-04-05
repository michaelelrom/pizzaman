import re, json

p = 'C:/Users/Mike/OneDrive/Documents/DATA/Developer/PizzaMan/toast_oo.html'
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

matches = re.findall(r'window\.__OO_STATE__\s*=\s*(\{[\s\S]{100,}?\});\s*(?:window|</script|$)', html)
blob = matches[0]
data = json.loads(blob)

# Print ALL top-level keys in the OO state
print('Top-level keys:', list(data.keys())[:20])

# Look at the ROOT_QUERY structure
rq = data.get('ROOT_QUERY', {})
print('\nROOT_QUERY keys (first 10):')
for k in list(rq.keys())[:10]:
    print(f'  {k}')

# Find the menu data key
for k in rq.keys():
    if 'menu' in k.lower() or 'group' in k.lower():
        print(f'\nMENU/GROUP key: {k}')
        val = rq[k]
        if isinstance(val, dict):
            print(json.dumps(val, indent=2)[:1000])

# Look for all unique __typename values
typenames = re.findall(r'"__typename"\s*:\s*"([^"]+)"', blob)
print('\nAll typenames:', sorted(set(typenames)))
