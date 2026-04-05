import re, json

p = 'C:/Users/Mike/OneDrive/Documents/DATA/Developer/PizzaMan/toast_oo.html'
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

matches = re.findall(r'window\.__OO_STATE__\s*=\s*(\{[\s\S]{100,}?\});\s*(?:window|</script|$)', html)
blob = matches[0]
data = json.loads(blob)

# Find modifier groups (pizza toppings, etc.)
def find_modifiers(d, depth=0):
    if depth > 20:
        return
    if isinstance(d, dict):
        # Modifier group typically has "name" and "modifiers" or "options"
        name = d.get('name','')
        mods = d.get('modifiers', d.get('options', []))
        if name and mods and isinstance(mods, list) and len(mods) > 0:
            print(f'\nMODIFIER GROUP: {name}')
            for m in mods:
                if isinstance(m, dict):
                    mname = m.get('name','')
                    mprices = m.get('prices', [])
                    price_str = ' / '.join([f'${p}' for p in mprices]) if mprices else ''
                    print(f'  - {mname} {price_str}')
        for k, v in d.items():
            if isinstance(v, (dict, list)):
                find_modifiers(v, depth+1)
    elif isinstance(d, list):
        for item in d:
            find_modifiers(item, depth+1)

find_modifiers(data)
