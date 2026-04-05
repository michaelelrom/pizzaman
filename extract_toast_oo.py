import re, json

p = 'C:/Users/Mike/OneDrive/Documents/DATA/Developer/PizzaMan/toast_oo.html'
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Get OO_STATE from toast page
matches = re.findall(r'window\.__OO_STATE__\s*=\s*(\{[\s\S]{100,}?\});\s*(?:window|</script|$)', html)
if matches:
    blob = matches[0]
    print(f'OO_STATE blob len={len(blob)}')
    try:
        data = json.loads(blob)
    except Exception as e:
        print('Parse error:', e)
        # Try to find the price data another way
        prices = re.findall(r'"price"\s*:\s*(\d+)', blob)
        print('Price values:', sorted(set([int(x) for x in prices if int(x) > 100]))[:30])
        prices2 = re.findall(r'"basePrice"\s*:\s*(\d+)', blob)
        print('BasePrice values:', sorted(set([int(x) for x in prices2 if int(x) > 100]))[:30])
        
        # Extract raw name+price combos
        name_price = re.findall(r'"name"\s*:\s*"([^"]{3,50})"(?:[^}]{0,500})"price"\s*:\s*(\d{3,6})', blob)
        print('\nName+Price pairs:')
        for n, pr in name_price[:30]:
            print(f'  ${int(pr)/100:.2f} | {n}')
        raise
    
    # Find priced items
    def find_priced(d, depth=0):
        if depth > 20:
            return
        if isinstance(d, dict):
            name = d.get('name','')
            for price_key in ['price', 'basePrice', 'unitPrice', 'itemPrice']:
                price = d.get(price_key, 0)
                if price and price > 0 and name:
                    desc = d.get('description','')
                    print(f'${price/100:.2f} | {name} | {desc[:100]}')
                    break
            for k, v in d.items():
                if isinstance(v, (dict, list)):
                    find_priced(v, depth+1)
        elif isinstance(d, list):
            for item in d:
                find_priced(item, depth+1)
    
    find_priced(data)
else:
    print('No OO_STATE found')
    # Check what's in the file
    print(html[5000:8000])
