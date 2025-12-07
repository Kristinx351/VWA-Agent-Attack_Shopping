import os

target_file = '/root/Project/visualwebarena/agent/prompts/prompt_constructor.py'
print(f'Installing data defense patch for {target_file}...')

with open(target_file, 'r') as f:
    lines = f.readlines()

new_lines = []
patched = False

patch_code = [
    "        # [PATCH] Force completion of missing fields\n",
    "        if 'meta_data' not in self.instruction: self.instruction['meta_data'] = {}\n",
    "        defaults = {\n",
    "            'intro': 'You are an autonomous intelligent agent.',\n",
    "            'template': 'OBJECTIVE: {objective}\\nAction:',\n",
    "            'keywords': [],\n",
    "            'examples': [],\n",
    "            'action_splitter': ':',\n",
    "            'answer_phrase': 'Answer'\n",
        "        }\n",
        "        for k, v in defaults.items():\n",
        "            if k not in self.instruction: self.instruction[k] = v\n",
        "            if k not in self.instruction['meta_data']: self.instruction['meta_data'][k] = v\n",
    "        # [PATCH END]\n"
]

for line in lines:
    new_lines.append(line)
    
    if 'self.instruction =' in line and not patched:
        if line.strip().startswith('self.instruction ='):
            indent = line[:line.find('self.instruction')]
            patch_code_indented = [indent + code for code in patch_code]
            new_lines.extend(patch_code_indented)
            patched = True
            print('Defense code inserted after data loading.')

if patched:
    with open(target_file, 'w') as f:
        f.writelines(new_lines)
    print('Fix complete! Code will now automatically fill missing intro and template.')
else:
    print('Warning: self.instruction assignment not found, trying alternative...')
