import re, json

# Extract neighborhood nights content
p = 'C:/Users/Mike/OneDrive/Documents/DATA/Developer/PizzaMan/neighborhood_nights.html'
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

matches = re.findall(r'window\.__[A-Z_]+__\s*=\s*(\{[\s\S]{100,}?\});\s*(?:window|</script|$)', html)
print(f'Found {len(matches)} state blobs')

for i, blob in enumerate(matches[:2]):
    print(f'\n=== BLOB {i} len={len(blob)} ===')
    try:
        data = json.loads(blob)
        # Look for text content in sections
        def find_text(d, depth=0):
            if depth > 15:
                return
            if isinstance(d, dict):
                for k in ['text', 'title', 'body', 'header', 'description', 'name', 'content', 'label']:
                    val = d.get(k)
                    if val and isinstance(val, str) and len(val) > 5:
                        print(f'  [{k}]: {val[:300]}')
                for k, v in d.items():
                    if isinstance(v, (dict, list)):
                        find_text(v, depth+1)
            elif isinstance(d, list):
                for item in d:
                    find_text(item, depth+1)
        find_text(data)
    except:
        print('Parse error, raw:')
        print(blob[:2000])
