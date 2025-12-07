import os
import ast

# 目标目录：所有 prompt 相关逻辑基本都在这里
TARGET_DIR = os.path.join(os.getcwd(), "agent", "prompts")

# 哪些 key 需要从 dict['k'] -> dict.get('k', default)?
KEY_DEFAULTS = {
    "intro": "",
    "template": "",
    "keywords": [],   # keywords 通常是 list
    # 你如果后面遇到 KeyError('examples')，可以把 "examples": [] 也加进来
}

class GetTransformer(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        self.replaced = 0

    def visit_Subscript(self, node):
        # 先递归处理子节点
        self.generic_visit(node)

        # 只处理“读取”的下标访问（Load），不处理赋值左侧（Store）
        if not isinstance(node.ctx, ast.Load):
            return node

        # 只处理简单的常量下标：dict['intro']
        key = None
        # Python 3.9+ 下，简单下标是 Constant
        if isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, str):
            key = node.slice.value
        else:
            return node

        if key not in KEY_DEFAULTS:
            return node

        default_value = KEY_DEFAULTS[key]

        # 构造 dict.get('key', default) 调用
        new_node = ast.Call(
            func=ast.Attribute(
                value=node.value,
                attr="get",
                ctx=ast.Load(),
            ),
            args=[
                ast.Constant(key),
                self._to_ast_const(default_value),
            ],
            keywords=[],
        )

        self.replaced += 1
        return ast.copy_location(new_node, node)

    def _to_ast_const(self, value):
        # 支持 str / list 这两种 default
        if isinstance(value, str):
            return ast.Constant(value)
        if isinstance(value, list):
            return ast.List(elts=[], ctx=ast.Load())
        # fallback
        return ast.Constant(value)


def process_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        print(f"❌ 跳过 {path}，语法错误：{e}")
        return 0

    transformer = GetTransformer()
    new_tree = transformer.visit(tree)
    ast.fix_missing_locations(new_tree)

    if transformer.replaced > 0:
        new_code = ast.unparse(new_tree)
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_code)
        print(f"✅ {path}: 替换了 {transformer.replaced} 处 dict['intro/template/keywords'] 读取为 .get()")
    else:
        print(f"ℹ️ {path}: 没有需要替换的地方")

    return transformer.replaced


def main():
    if not os.path.isdir(TARGET_DIR):
        print(f"❌ 找不到目标目录: {TARGET_DIR}")
        return

    total = 0
    print(f"🔍 扫描并修复目录: {TARGET_DIR}")
    for root, dirs, files in os.walk(TARGET_DIR):
        for name in files:
            if not name.endswith(".py"):
                continue
            path = os.path.join(root, name)
            total += process_file(path)

    print(f"\n🎯 总共替换了 {total} 处读取 'intro'/'template'/'keywords' 的表达式为 .get(...)")
    print("（只改读取，不改赋值左侧，所以不会再出现 .get(...) = ... 的 SyntaxError）")


if __name__ == "__main__":
    main()
