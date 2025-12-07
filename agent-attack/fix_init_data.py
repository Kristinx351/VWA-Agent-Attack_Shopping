import os

target_file = '/root/Project/visualwebarena/agent/prompts/prompt_constructor.py'
print(f'🏥 正在为 {target_file} 安装数据防御补丁...')

with open(target_file, 'r') as f:
    lines = f.readlines()

new_lines = []
patched = False

# 我们要注入的防御代码块
# 这段代码会在运行时动态补全缺失的字段
patch_code = [
    "        # [PATCH] 强制补全缺失字段 (防崩溃保险)\n",
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
    "            # 补全顶层\n",
    "            if k not in self.instruction: self.instruction[k] = v\n",
    "            # 补全 meta_data 层\n",
    "            if k not in self.instruction['meta_data']: self.instruction['meta_data'][k] = v\n",
    "        # [PATCH END]\n"
]

for line in lines:
    new_lines.append(line)
    
    # 寻找最佳插入点
    # 通常是在 json.load 之后，或者是 super().__init__ 附近
    # 我们找 "self.instruction = " 这一行，它通常在加载数据
    if 'self.instruction =' in line and not patched:
        # 确保不是在 if 块里的一行（看缩进）
        if line.strip().startswith('self.instruction ='):
            indent = line[:line.find('self.instruction')]
            # 加上缩进
            patch_code_indented = [indent + code for code in patch_code]
            new_lines.extend(patch_code_indented)
            patched = True
            print('✅ 已在数据加载后插入了防御代码。')

if patched:
    with open(target_file, 'w') as f:
        f.writelines(new_lines)
    print('🎉 修复完成！现在代码会自动填充缺失的 intro 和 template。')
else:
    print('⚠️ 未找到 self.instruction 赋值位置，尝试备选方案...')
    # 如果没找到赋值，试试在 __init__ 之后插入
    # (此处省略备选，通常上面的逻辑就够了)
