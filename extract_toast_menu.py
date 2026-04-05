import re, json

p = 'C:/Users/Mike/OneDrive/Documents/DATA/Developer/PizzaMan/toast_oo.html'
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

print(f'File size: {len(html)} chars')

# Find all window.__ state variables
state_vars = re.findall(r'window\.__(\w+)__\s*=', html)
print('State vars:', state_vars)

# Try to extract menu with prices from __NEXT_DATA__ or similar
next_data = re.findall(r'<script[^>]*id="__NEXT_DATA__"[^>]*>([\s\S]+?)</script>', html)
if next_data:
    print('\nFound __NEXT_DATA__, len:', len(next_data[0]))
    try:
        data = json.loads(next_data[0])
        print(json.dumps(data, indent=2)[:3000])
    except Exception as e:
        print('Parse error:', e)
        print(next_data[0][:500])

# Look for menu item names + prices in JSON
items_with_prices = re.findall(r'"name"\s*:\s*"([^"]{3,})"[^}]{0,300}"price"\s*:\s*(\d+)', html)
print('\nItems with prices (first 50):')
for name, price in items_with_prices[:50]:
    print(f'  ${int(price)/100:.2f} | {name}')
