import re, json

p = 'C:/Users/Mike/OneDrive/Documents/DATA/Developer/PizzaMan/toast_oo.html'
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Look for price anywhere in the raw HTML
# Search for numeric values that look like menu prices (5-30 dollar range = 500-3000 cents)
price_contexts = re.findall(r'(?:price|Price|amount|Amount|cost|Cost)["\s:]{1,10}(\d{3,5})', html)
print('Price-like values:', sorted(set([int(x) for x in price_contexts]))[:40])

# Look for $ amounts in text
dollar_text = re.findall(r'\\$(\d+(?:\.\d{2})?)', html)
print('Dollar text amounts:', sorted(set(dollar_text)))

# Search for "priceCents"
cents = re.findall(r'priceCents["\s:]{1,5}(\d+)', html)
print('priceCents:', sorted(set([int(x) for x in cents]))[:30])

# Look at a chunk of the OO_STATE to see structure around menu items
idx = html.find('"Pizza Man Special"')
if idx >= 0:
    print('\nContext around "Pizza Man Special":')
    print(html[idx-50:idx+500])
