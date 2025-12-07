import os

target_file = '/root/Project/visualwebarena/agent/prompts/prompt_constructor.py'
print(f'Fixing syntax errors: {target_file}')

with open(target_file, 'r') as f:
    content = f.read()

replacements = [
    ("instruction.get('examples', []) =", "instruction['examples'] ="),
    ('instruction.get("examples", []) =', "instruction['examples'] ="),
    ("instruction.get('keywords', []) =", "instruction['keywords'] ="),
    ('instruction.get("keywords", []) =', "instruction['keywords'] ="),
    ("meta_data.get('examples', []) =", "meta_data['examples'] ="),
    ('meta_data.get("examples", []) =', "meta_data['examples'] ="),
]

new_content = content
count = 0

for old, new in replacements:
    if old in new_content:
        new_content = new_content.replace(old, new)
        count += 1
        print(f'Fixed: {old} -> {new}')

if count > 0:
    with open(target_file, 'w') as f:
        f.write(new_content)
    print(f'Successfully fixed {count} syntax errors!')
else:
    print('No syntax errors found, file may have been manually modified or content does not match.')
