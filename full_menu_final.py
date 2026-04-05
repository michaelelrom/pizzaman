import re, json

p = 'C:/Users/Mike/OneDrive/Documents/DATA/Developer/PizzaMan/toast_oo.html'
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

matches = re.findall(r'window\.__OO_STATE__\s*=\s*(\{[\s\S]{100,}?\});\s*(?:window|</script|$)', html)
blob = matches[0]
data = json.loads(blob)

# Resolve refs
def resolve(obj, store):
    if isinstance(obj, dict):
        if '__ref' in obj:
            key = obj['__ref']
            if key in store:
                return resolve(store[key], store)
            return obj
        return {k: resolve(v, store) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [resolve(item, store) for item in obj]
    return obj

# Get all menu groups
rq = data['ROOT_QUERY']
paginated = None
for k, v in rq.items():
    if 'paginatedMenuItems' in k:
        paginated = resolve(v, data)
        break

if paginated:
    groupings = paginated.get('groupings', [])
    print('=== MENU STRUCTURE ===')
    for g in groupings:
        print(f'\n== {g["name"]} ({g.get("itemCount",0)} items) ==')
        for child in g.get('children', []):
            print(f'  - {child["name"]} ({child.get("itemCount",0)} items)')

# Now get all Menu objects and their items
print('\n\n=== FULL MENU WITH PRICES ===')
for key in data.keys():
    if key.startswith('Menu:'):
        menu = data[key]
        menu_name = menu.get('name','')
        if not menu_name:
            continue
        print(f'\n=== {menu_name} ===')
        groups = menu.get('groups', [])
        for group_ref in groups:
            group = resolve(group_ref, data)
            group_name = group.get('name','')
            print(f'\n  -- {group_name} --')
            items = group.get('items', [])
            for item_ref in items:
                item = resolve(item_ref, data)
                if isinstance(item, dict):
                    iname = item.get('name','')
                    iprices = item.get('prices',[])
                    idesc = item.get('description','')
                    price_str = '/'.join([f'${p}' for p in iprices]) if iprices else ''
                    print(f'    {iname} {price_str}')
                    if idesc:
                        print(f'      {idesc}')
