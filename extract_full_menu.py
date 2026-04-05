import re, json

p = 'C:/Users/Mike/OneDrive/Documents/DATA/Developer/PizzaMan/toast_oo.html'
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

matches = re.findall(r'window\.__OO_STATE__\s*=\s*(\{[\s\S]{100,}?\});\s*(?:window|</script|$)', html)
blob = matches[0]
data = json.loads(blob)

def extract_menu(d, current_group='', depth=0):
    if depth > 20:
        return
    if isinstance(d, dict):
        name = d.get('name','')
        prices = d.get('prices', [])
        desc = d.get('description','')
        
        # Check if this is a menu group
        if name and 'items' in d and isinstance(d.get('items'), list):
            print(f'\n--- {name} ---')
        
        # Check if this is a menu item (has prices list)
        if name and prices and isinstance(prices, list) and len(prices) > 0:
            price_str = ' / '.join([f'${p:.2f}' if isinstance(p, float) else f'${p}' for p in prices])
            print(f'  {name} | {price_str}')
            if desc:
                print(f'    DESC: {desc}')
        
        for k, v in d.items():
            if isinstance(v, (dict, list)):
                extract_menu(v, current_group, depth+1)
    elif isinstance(d, list):
        for item in d:
            extract_menu(item, current_group, depth+1)

extract_menu(data)
