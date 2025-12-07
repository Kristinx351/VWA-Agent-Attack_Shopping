import os

target_file = '/root/Project/visualwebarena/agent/prompts/prompt_constructor.py'
print(f'Fixing syntax errors: {target_file}')

with open(target_file, 'r') as f:
    content = f.read()

fix_patterns = [
    ("instruction.get('examples', []) =", "instruction['examples'] ="),
    ('instruction.get("examples", []) =', "instruction['examples'] ="),
    ("self.instruction.get('examples', []) =", "self.instruction['examples'] ="),
    ('self.instruction.get("examples", []) =', "self.instruction['examples'] ="),
    ("instruction.get('keywords', []) =", "instruction['keywords'] ="),
    ('instruction.get("keywords", []) =', "instruction['keywords'] ="),
    ("self.instruction.get('keywords', []) =", "self.instruction['keywords'] ="),
    ('self.instruction.get("keywords", []) =', "self.instruction['keywords'] ="),
    ("meta_data.get('examples', []) =", "meta_data['examples'] ="),
    ('meta_data.get("examples", []) =', "meta_data['examples'] ="),
]

new_content = content
fixed_count = 0

for wrong, right in fix_patterns:
    if wrong in new_content:
        count = new_content.count(wrong)
        new_content = new_content.replace(wrong, right)
        fixed_count += count
        print(f'Fixed {count} occurrences: {wrong} -> {right}')

if fixed_count > 0:
    with open(target_file, 'w') as f:
        f.write(new_content)
    print(f'Successfully fixed {fixed_count} syntax errors!')
else:
    print('No known syntax error patterns found, file may have been manually modified.')
