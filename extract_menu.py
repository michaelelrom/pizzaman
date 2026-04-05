import re, json

p = 'C:/Users/Mike/.claude/projects/c--Users-Mike-OneDrive-Documents-DATA-Developer-PizzaMan/7029caca-a04d-4bbc-9355-1bdd966b6e50/tool-results/bd3yuhfxo.txt'
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

matches = re.findall(r'window\.__OO_STATE__\s*=\s*(\{[\s\S]{100,}?\});\s*(?:window|</script|$)', html)
blob = matches[0]
data = json.loads(blob)

def extract_menu(d, path='', depth=0):
    if depth > 15:
        return
    if isinstance(d, dict):
        if 'name' in d and ('price' in d or 'calories' in d or 'itemGroupGuid' in d):
            name = d.get('name','')
            price = d.get('price', '')
            desc = d.get('description', '')
            calories = d.get('calories', '')
            print(f'ITEM | {name} | price={price} | cal={calories} | desc={desc[:120] if desc else ""}')
        if 'name' in d and 'items' in d and isinstance(d['items'], list):
            print(f'\nGROUP: {d["name"]}')
        for k, v in d.items():
            if isinstance(v, (dict, list)):
                extract_menu(v, path+'.'+k, depth+1)
    elif isinstance(d, list):
        for item in d:
            extract_menu(item, path, depth+1)

extract_menu(data)
