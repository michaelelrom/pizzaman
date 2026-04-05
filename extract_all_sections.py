import re, json

p = 'C:/Users/Mike/OneDrive/Documents/DATA/Developer/PizzaMan/neighborhood_nights.html'
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

matches = re.findall(r'window\.__[A-Z_]+__\s*=\s*(\{[\s\S]{100,}?\});\s*(?:window|</script|$)', html)
blob = matches[0]
data = json.loads(blob)

# Get the Restaurant content sections
rest_key = None
for k in data.keys():
    if k.startswith('Restaurant:'):
        rest_key = k
        break

if rest_key:
    rest = data[rest_key]
    content = rest.get('content', {})
    sections = content.get('sections', [])
    print(f'Found {len(sections)} sections')
    
    for i, section in enumerate(sections):
        typename = section.get('__typename','')
        sname = section.get('sectionName','')
        print(f'\n=== Section {i}: {typename} ({sname}) ===')
        
        # Cards section
        cards = section.get('cards', [])
        for card in cards:
            title = card.get('title','')
            body = card.get('body','')
            btn = card.get('button',{})
            btn_text = btn.get('text','') if isinstance(btn, dict) else ''
            btn_link = btn.get('link','') if isinstance(btn, dict) else ''
            img = card.get('image',{})
            alt = img.get('altText','') if isinstance(img, dict) else ''
            print(f'  Card title: {title}')
            print(f'  Card body: {body}')
            if btn_text:
                print(f'  Button: {btn_text} -> {btn_link}')
            if alt:
                print(f'  Image alt: {alt}')
        
        # Blocks in dynamic sections
        blocks = section.get('blocks', [])
        for b in blocks:
            kind = b.get('kind','')
            contents = b.get('contents', {})
            if isinstance(contents, dict):
                text_content = contents.get('text','')
                alt = contents.get('altText','')
                link = contents.get('link','')
                if text_content:
                    print(f'  Block ({kind}) text: {text_content}')
                if alt:
                    print(f'  Block ({kind}) altText: {alt}')
                if link:
                    print(f'  Block ({kind}) link: {link}')
        
        # Specials/hours sections
        for key in ['header','subheader','body','text','description']:
            val = section.get(key,'')
            if val:
                print(f'  {key}: {val[:400]}')
