import os
import re

target_file = '/root/Project/visualwebarena/agent/prompts/prompt_constructor.py'
print(f'Performing deep code fix: {target_file}')

with open(target_file, 'r') as f:
    content = f.read()

defaults = {
    'intro': 'You are an autonomous intelligent agent.',
    'template': 'OBJECTIVE: {objective}\\nAction:',
    'keywords': [],
    'examples': []
}

new_content = content
total_fixed = 0

for key, default_val in defaults.items():
    pattern_double = r'\[\s*\"' + key + r'\"\s*\](?!\s*=)'
    pattern_single = r'\[\s*\'' + key + r'\'\s*\](?!\s*=)'
    
    replacement = f".get('{key}', {repr(default_val)})"

    new_content, count_d = re.subn(pattern_double, replacement, new_content)
    new_content, count_s = re.subn(pattern_single, replacement, new_content)
    
    if count_d + count_s > 0:
        print(f'Fixed {count_d + count_s} [{key}] read operations')
        total_fixed += (count_d + count_s)

if total_fixed > 0:
    with open(target_file, 'w') as f:
        f.write(new_content)
    print(f'Successfully fixed {total_fixed} issues.')
else:
    print('No code matching the patterns found. File may have been fixed or variable names differ.')
    print('--- Diagnostic info ---')
    for line in content.split('\n'):
        if 'intro' in line and '[' in line:
            print(f'Found suspicious line: {line.strip()}')
