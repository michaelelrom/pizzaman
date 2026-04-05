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
sections = content.get('sections', [])

for i, section in enumerate(sections):
    typename = section.get('__typename','')
    sname = section.get('sectionName','')
    print(f'\n=== Section {i}: {typename} ({sname}) ===')
    # Full dump of this section
    print(json.dumps(section, indent=2)[:3000])
