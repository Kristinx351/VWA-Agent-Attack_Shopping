import os

target_file = '/root/Project/visualwebarena/agent/prompts/prompt_constructor.py'
print(f'🏥 正在修复语法错误: {target_file}')

with open(target_file, 'r') as f:
    content = f.read()

# 定义要修复的错误模式 -> 正确模式
# 我们要把被改坏的赋值语句左边改回来
fix_patterns = [
    # 修复 examples 的赋值
    ("instruction.get('examples', []) =", "instruction['examples'] ="),
    ('instruction.get("examples", []) =', "instruction['examples'] ="),
    ("self.instruction.get('examples', []) =", "self.instruction['examples'] ="),
    ('self.instruction.get("examples", []) =', "self.instruction['examples'] ="),
    
    # 修复 keywords 的赋值
    ("instruction.get('keywords', []) =", "instruction['keywords'] ="),
    ('instruction.get("keywords", []) =', "instruction['keywords'] ="),
    ("self.instruction.get('keywords', []) =", "self.instruction['keywords'] ="),
    ('self.instruction.get("keywords", []) =', "self.instruction['keywords'] ="),

    # 修复可能误伤的 meta_data 赋值
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
        print(f'🔧 修复了 {count} 处: {wrong} -> {right}')

if fixed_count > 0:
    with open(target_file, 'w') as f:
        f.write(new_content)
    print(f'✅ 成功修复了 {fixed_count} 处语法错误！')
else:
    print('⚠️ 未发现已知的语法错误模式，可能是文件内容已经被手动修改过。')
