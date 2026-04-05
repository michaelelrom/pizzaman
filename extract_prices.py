import re, json

p = 'C:/Users/Mike/.claude/projects/c--Users-Mike-OneDrive-Documents-DATA-Developer-PizzaMan/7029caca-a04d-4bbc-9355-1bdd966b6e50/tool-results/bd3yuhfxo.txt'
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

matches = re.findall(r'window\.__OO_STATE__\s*=\s*(\{[\s\S]{100,}?\});\s*(?:window|</script|$)', html)
blob = matches[0]
data = json.loads(blob)

# Find items with actual prices
def find_priced_items(d, depth=0):
    if depth > 20:
        return
    if isinstance(d, dict):
        price = d.get('price', 0)
        name = d.get('name', '')
        if price and price > 0 and name:
            desc = d.get('description','')
            print(f'${price/100:.2f} | {name} | {desc[:100]}')
        for k, v in d.items():
            if isinstance(v, (dict, list)):
                find_priced_items(v, depth+1)
    elif isinstance(d, list):
        for item in d:
            find_priced_items(item, depth+1)

find_priced_items(data)
