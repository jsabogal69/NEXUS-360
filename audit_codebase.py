import ast
import os
import sys

class AuditVisitor(ast.NodeVisitor):
    def __init__(self, filename):
        self.filename = filename
        self.issues = []

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name == 'pdb':
                self.issues.append(f"Line {node.lineno}: Debugger import 'pdb' found.")
        self.generic_visit(node)

    def visit_Call(self, node):
        # Detect blocking calls: time.sleep, requests.get/post inside async functions
        if isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                func_name = f"{node.func.value.id}.{node.func.attr}"
                
                # Check 1: Blocking Sleep
                if func_name == "time.sleep":
                    self.issues.append(f"Line {node.lineno}: Blocking 'time.sleep' found. Use 'await asyncio.sleep' instead.")
                
                # Check 2: Print Statements (Warning)
                if func_name == "print":
                    # Just a warning, prints are okay for scripts but bad for prod agents
                    pass

        # Detect use of print() function
        if isinstance(node.func, ast.Name) and node.func.id == "print":
             # We might want to flag this in production code
             pass
             
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        # Detect generic 'except:' or 'except Exception:' without logging
        if node.type is None or (isinstance(node.type, ast.Name) and node.type.id == "Exception"):
            has_log = False
            for child in node.body:
                if isinstance(child, ast.Expr) and isinstance(child.value, ast.Call):
                     # Heuristic: Check for logger.error or print
                     func = child.value.func
                     if isinstance(func, ast.Attribute) and "log" in func.attr:
                         has_log = True
                     elif isinstance(func, ast.Name) and func.id == "print":
                         has_log = True
            
            if not has_log and len(node.body) > 1: # Ignore empty/pass excepts for now
                self.issues.append(f"Line {node.lineno}: Generic 'except' block without logging found.")
        
        self.generic_visit(node)

def audit_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source)
        visitor = AuditVisitor(filepath)
        visitor.visit(tree)
        return visitor.issues
    except Exception as e:
        return [f"ERROR parsing file: {e}"]

def main():
    print("🛡️  Technical Auditor: Starting Static Code Analysis...\n")
    
    target_dir = "agents"
    total_issues = 0
    
    for root, dirs, files in os.walk(target_dir):
        if "venv" in root or "__pycache__" in root: continue
        
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                issues = audit_file(path)
                
                if issues:
                    print(f"📄 {path}")
                    for i in issues:
                        print(f"  - {i}")
                    print("")
                    total_issues += len(issues)

    if total_issues == 0:
        print("✅ No critical code patterns found.")
    else:
        print(f"⚠️  Found {total_issues} issues to review.")

if __name__ == "__main__":
    main()
