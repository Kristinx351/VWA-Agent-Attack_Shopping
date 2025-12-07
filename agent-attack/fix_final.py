import os
import re

# 目标文件
target_file = '/root/Project/visualwebarena/agent/prompts/prompt_constructor.py'
print(f'🏥 正在进行深度代码治疗: {target_file}')

with open(target_file, 'r') as f:
    content = f.read()

# 我们要修复的字段及其默认值
defaults = {
    'intro': 'You are an autonomous intelligent agent.',
    'template': 'OBJECTIVE: {objective}\\nAction:',
    'keywords': [],
    'examples': []
}

new_content = content
total_fixed = 0

for key, default_val in defaults.items():
    # 构造正则：匹配 ['key'] 或 ["key"]，且后面没有等号（排除赋值操作）
    # 核心正则逻辑：查找 ["key"] 但后面不跟着 ' ='
    
    # 1. 匹配双引号 ["key"]
    pattern_double = r'\[\s*\"' + key + r'\"\s*\](?!\s*=)'
    # 2. 匹配单引号 ['key']
    pattern_single = r'\[\s*\'' + key + r'\'\s*\](?!\s*=)'
    
    # 替换目标：变成 .get('key', default)
    replacement = f".get('{key}', {repr(default_val)})"

    # 执行替换
    new_content, count_d = re.subn(pattern_double, replacement, new_content)
    new_content, count_s = re.subn(pattern_single, replacement, new_content)
    
    if count_d + count_s > 0:
        print(f'🔧 修复了 {count_d + count_s} 处 [{key}] 读取逻辑')
        total_fixed += (count_d + count_s)

if total_fixed > 0:
    with open(target_file, 'w') as f:
        f.write(new_content)
    print(f'✅ 完美！已强制修复 {total_fixed} 处隐患。代码现在自带防弹衣。')
else:
    print('⚠️ 未匹配到需要修复的代码。可能文件已被修复，或变量名不同。')
    # 调试：打印出可能包含 intro 的行，看看它到底长啥样
    print('--- 诊断信息 ---')
    for line in content.split('\n'):
        if 'intro' in line and '[' in line:
            print(f'发现疑似行: {line.strip()}')
