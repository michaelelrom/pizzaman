import re, json

# Let's look at the main homepage JSON blob for all page sections content
p = 'C:/Users/Mike/.claude/projects/c--Users-Mike-OneDrive-Documents-DATA-Developer-PizzaMan/7029caca-a04d-4bbc-9355-1bdd966b6e50/tool-results/bd3yuhfxo.txt'
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

matches = re.findall(r'window\.__[A-Z_]+__\s*=\s*(\{[\s\S]{100,}?\});\s*(?:window|</script|$)', html)
blob = matches[0]
data = json.loads(blob)

# Get main restaurant
rest_key = None
for k in data.keys():
    if k.startswith('Restaurant:'):
        rest_key = k
        break

print(f'Restaurant key: {rest_key}')
rest = data[rest_key]
content = rest.get('content', {})
sections = content.get('sections', [])
print(f'Found {len(sections)} sections')

for i, section in enumerate(sections):
    typename = section.get('__typename','')
    sname = section.get('sectionName','')
    print(f'\n=== Section {i}: {typename} ({sname}) ===')
    
    # Cards
    cards = section.get('cards', [])
    for j, card in enumerate(cards):
        title = card.get('title','')
        body = card.get('body','')
        btn = card.get('button',{})
        btn_text = btn.get('text','') if isinstance(btn, dict) else ''
        btn_link = btn.get('link','') if isinstance(btn, dict) else ''
        print(f'  Card {j}: title={title[:200]} body={body[:200]} btn={btn_text}->{btn_link}')
    
    # Blocks
    blocks = section.get('blocks', [])
    for b in blocks:
        kind = b.get('kind','')
        contents = b.get('contents', {})
        if isinstance(contents, dict):
            alt = contents.get('altText','')
            link = contents.get('link','')
            text = ''
            # text content might be in children
            for key in ['text', 'richText', 'plainText']:
                t = contents.get(key,'')
                if t:
                    text = str(t)[:200]
            if alt or link or text:
                print(f'  Block ({kind}): alt={alt} link={link} text={text}')
    
    # Other fields
    for key in ['header', 'subheader', 'body', 'text', 'description', 'route', 'title']:
        val = section.get(key,'')
        if val:
            print(f'  {key}: {str(val)[:300]}')
