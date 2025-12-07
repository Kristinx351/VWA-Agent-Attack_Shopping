import os
import re
from pathlib import Path
import shutil

# 👉 修改为你的实际路径
target_file = Path('/root/Project/visualwebarena/agent/prompts/prompt_constructor.py')

print(f'🏥 Fixing broken .get() assignments in: {target_file}')

if not target_file.exists():
    print("❌ Error: target file not found!")
    raise SystemExit(1)

# 备份一下原文件，防止翻车
backup_file = target_file.with_suffix('.py.bak')
shutil.copy2(target_file, backup_file)
print(f'🧷 Backup created at: {backup_file}')

text = target_file.read_text()

# 匹配形如：
#     instruction.get('examples', []) = ...
#     self.instruction.get("keywords", default) = ...
#     meta_data.get('examples') = ...
#
# 要求：
#  - .get(...) 出现在行首（可能有缩进），且在等号左边
#  - 不会匹配 RHS 的读取语句，比如 x = foo.get(...)
pattern = re.compile(r"""
^(\s*)                          # 1: indentation
([A-Za-z_][\w\.]*)              # 2: object name, e.g. instruction / self.instruction / meta_data
\.get\(                         #    literal '.get('
\s*(['"])([^'"]+)\3             # 3: quote, 4: key inside quotes
(?:\s*,[^)]*)?                  #    optional default argument: , ...
\)\s*=
""", re.VERBOSE | re.MULTILINE)

def repl(match: re.Match) -> str:
    indent = match.group(1)
    obj = match.group(2)
    key = match.group(4)
    # 变成：obj['key'] =
    return f"{indent}{obj}['{key}'] ="

new_text, n_subs = pattern.subn(repl, text)

if n_subs == 0:
    print("⚠️ No broken `.get(...)=` assignments found. File may already be fixed or modified.")
else:
    target_file.write_text(new_text)
    print(f'✅ Fixed {n_subs} assignment(s) of the form `.get(...)=`.')
    print('   All reads like `x = obj.get("key", default)` are preserved.')

print("🎉 Done.")
