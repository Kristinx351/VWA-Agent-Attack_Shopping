import os

target_file = '/root/Project/visualwebarena/agent/prompts/prompt_constructor.py'
print(f'正在修复语法错误: {target_file}')

with open(target_file, 'r') as f:
    content = f.read()

# 我们不再用复杂的正则，直接用最简单的字符串替换，绝对不会错
# 目标：把被改坏的 .get(..., []) =  改回 ['...'] =
replacements = [
    ("instruction.get('examples', []) =", "instruction['examples'] ="),
    ('instruction.get("examples", []) =', "instruction['examples'] ="),
    ("instruction.get('keywords', []) =", "instruction['keywords'] ="),
    ('instruction.get("keywords", []) =', "instruction['keywords'] ="),
    # 以防万一，把可能涉及 meta_data 的也加进去
    ("meta_data.get('examples', []) =", "meta_data['examples'] ="),
    ('meta_data.get("examples", []) =', "meta_data['examples'] ="),
]

new_content = content
count = 0

for old, new in replacements:
    if old in new_content:
        new_content = new_content.replace(old, new)
        count += 1
        print(f'🔧 修复: {old} -> {new}')

if count > 0:
    with open(target_file, 'w') as f:
        f.write(new_content)
    print(f'✅ 成功修复了 {count} 处语法错误！')
else:
    print('⚠️ 未发现语法错误，可能是文件已被手动修改或内容不匹配。')
