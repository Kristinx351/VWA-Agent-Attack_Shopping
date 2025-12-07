import ast
import os
from pathlib import Path

TARGET_FILE = Path("/root/Project/visualwebarena/agent/prompts/prompt_constructor.py")

print(f"🔍 Patching file: {TARGET_FILE}")

if not TARGET_FILE.exists():
    print("❌ Error: target file does not exist.")
    raise SystemExit(1)

source = TARGET_FILE.read_text()

try:
    tree = ast.parse(source)
except SyntaxError as e:
    print("❌ Cannot parse prompt_constructor.py (still has a syntax error):")
    print(e)
    raise SystemExit(1)


class SafeGetTransformer(ast.NodeTransformer):
    """
    Turn reads like:
        instruction["intro"]
    into:
        instruction.get("intro", "")
    but ONLY when:
      - It's a read (ctx is ast.Load)
      - The key is 'intro', 'template', or 'keywords'
      - The base is instruction / self.instruction / meta_data / self.meta_data
    """

    def visit_Subscript(self, node: ast.Subscript):
        # First transform children
        self.generic_visit(node)

        # Don't touch store contexts (LHS of assignment)
        if not isinstance(node.ctx, ast.Load):
            return node

        # Extract the key if it's a constant string
        key = None

        # Python 3.10 can still use ast.Index in some cases
        slice_node = node.slice
        if isinstance(slice_node, ast.Constant) and isinstance(slice_node.value, str):
            key = slice_node.value
        elif hasattr(ast, "Index") and isinstance(slice_node, ast.Index):
            inner = slice_node.value
            if isinstance(inner, ast.Constant) and isinstance(inner.value, str):
                key = inner.value

        if key not in ("intro", "template", "keywords"):
            return node

        base = node.value

        # Check if base is instruction, self.instruction, meta_data, or self.meta_data
        allowed = False

        # instruction[...] or meta_data[...]
        if isinstance(base, ast.Name) and base.id in ("instruction", "meta_data"):
            allowed = True

        # self.instruction[...] or self.meta_data[...]
        if (
            isinstance(base, ast.Attribute)
            and isinstance(base.value, ast.Name)
            and base.value.id == "self"
            and base.attr in ("instruction", "meta_data")
        ):
            allowed = True

        if not allowed:
            return node

        # Choose default based on key
        if key in ("intro", "template"):
            default = ast.Constant(value="")
        elif key == "keywords":
            default = ast.Constant(value=[])
        else:
            return node  # Should not reach here

        new_call = ast.Call(
            func=ast.Attribute(
                value=base,
                attr="get",
                ctx=ast.Load(),
            ),
            args=[
                ast.Constant(value=key),
                default,
            ],
            keywords=[],
        )

        return ast.copy_location(new_call, node)


transformer = SafeGetTransformer()
new_tree = transformer.visit(tree)
ast.fix_missing_locations(new_tree)

try:
    new_source = ast.unparse(new_tree)
except Exception as e:
    print("❌ Failed to unparse AST back to source:")
    print(e)
    raise SystemExit(1)

# Optional: backup original file
backup_path = TARGET_FILE.with_suffix(".py.bak_ast_fix")
if not backup_path.exists():
    backup_path.write_text(source)
    print(f"💾 Backup saved to: {backup_path}")

TARGET_FILE.write_text(new_source)
print("✅ Finished patching prompt_constructor.py with safe .get() reads.")
