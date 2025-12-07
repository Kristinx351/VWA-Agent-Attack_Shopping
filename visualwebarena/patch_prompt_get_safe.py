import os
import ast

TARGET_DIR = os.path.join(os.getcwd(), "agent", "prompts")

KEY_DEFAULTS = {
    "intro": "",
    "template": "",
    "keywords": [],
}

class GetTransformer(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        self.replaced = 0

    def visit_Subscript(self, node):
        self.generic_visit(node)

        if not isinstance(node.ctx, ast.Load):
            return node

        key = None
        if isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, str):
            key = node.slice.value
        else:
            return node

        if key not in KEY_DEFAULTS:
            return node

        default_value = KEY_DEFAULTS[key]

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
        if isinstance(value, str):
            return ast.Constant(value)
        if isinstance(value, list):
            return ast.List(elts=[], ctx=ast.Load())
        return ast.Constant(value)


def process_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        print(f"Skipping {path}, syntax error: {e}")
        return 0

    transformer = GetTransformer()
    new_tree = transformer.visit(tree)
    ast.fix_missing_locations(new_tree)

    if transformer.replaced > 0:
        new_code = ast.unparse(new_tree)
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_code)
        print(f"Replaced {transformer.replaced} dict['intro/template/keywords'] reads with .get() in {path}")
    else:
        print(f"No replacements needed in {path}")

    return transformer.replaced


def main():
    if not os.path.isdir(TARGET_DIR):
        print(f"Target directory not found: {TARGET_DIR}")
        return

    total = 0
    print(f"Scanning and fixing directory: {TARGET_DIR}")
    for root, dirs, files in os.walk(TARGET_DIR):
        for name in files:
            if not name.endswith(".py"):
                continue
            path = os.path.join(root, name)
            total += process_file(path)

    print(f"\nTotal: replaced {total} 'intro'/'template'/'keywords' reads with .get(...)")
    print("(Only reading operations are changed, not assignments)")


if __name__ == "__main__":
    main()
