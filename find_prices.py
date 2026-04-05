import re, json

p = 'C:/Users/Mike/.claude/projects/c--Users-Mike-OneDrive-Documents-DATA-Developer-PizzaMan/7029caca-a04d-4bbc-9355-1bdd966b6e50/tool-results/bd3yuhfxo.txt'
with open(p, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Search for price patterns in the raw blob
# Look for "basePrice" or "price" with numeric values
price_patterns = re.findall(r'"(?:basePrice|price|cost|amount)"\s*:\s*(\d+(?:\.\d+)?)', html)
print('Price values found:', sorted(set([float(x) for x in price_patterns if float(x) > 0]))[:50])

# Look for currency formatted strings
dollar_amounts = re.findall(r'\\$(\d+(?:\.\d+)?)', html)
print('Dollar amounts in strings:', sorted(set(dollar_amounts)))

# Look for menu item with priceCents or similar
cents = re.findall(r'"(?:priceCents|basePrice|unitPrice|price)"\s*:\s*(\d{3,6})', html)
cents_vals = sorted(set([int(x) for x in cents if int(x) > 0]))
print('Price cents values:', [f'${x/100:.2f}' for x in cents_vals[:30]])

# Also check for the modifier groups (pizza toppings/sizes)
mods = re.findall(r'"(?:modifier|option|topping|size|crust)"[^{]{0,20}\{[^}]{0,200}', html)
print('\nModifier entries (first 10):')
for m in mods[:10]:
    print(' ', m[:150])
