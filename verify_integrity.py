import os
import re
import sys

def check_security_basics():
    print("🛡️  Technical Auditor: Starting Integrity & Security Check...\n")
    
    issues = []
    warnings = []
    
    # 1. Critical Files Check
    required_files = ["serviceAccountKey.json", ".env", ".gitignore"]
    for f in required_files:
        if not os.path.exists(f):
            issues.append(f"MISSING: Critical file '{f}' not found in root.")
        else:
            print(f"✅ Found {f}")

    # 2. Gitignore Check
    if os.path.exists(".gitignore"):
        with open(".gitignore", "r") as f:
            content = f.read()
            if "serviceAccountKey.json" not in content:
                issues.append("SECURITY: 'serviceAccountKey.json' NOT in .gitignore!")
            else:
                print("✅ .gitignore correctly excludes serviceAccountKey.json")
                
            if ".env" not in content:
                issues.append("SECURITY: '.env' NOT in .gitignore!")
            else:
                print("✅ .gitignore correctly excludes .env")

    # 3. Secret Pattern Scan
    print("\n🔍 Scanning codebase for exposed secrets (heuristic)...")
    secret_patterns = {
        "Google API Key": r"AIza[0-9A-Za-z-_]{35}",
        "OpenAI Key": r"sk-[a-zA-Z0-9]{48}",
        "Firebase Config": r"apiKey.*AIza"
    }
    
    ignored_dirs = ["venv", "node_modules", ".git", ".firebase", "__pycache__", "gcloud auth login"]
    
    for root, dirs, files in os.walk("."):
        # Skip ignored dirs
        dirs[:] = [d for d in dirs if d not in ignored_dirs]
        
        for file in files:
            if file.endswith((".py", ".js", ".json", ".md")) and file != "serviceAccountKey.json":
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        for key_type, pattern in secret_patterns.items():
                            matches = re.finditer(pattern, content)
                            for match in matches:
                                # Start/End index for context
                                start = max(0, match.start() - 10)
                                end = min(len(content), match.end() + 10)
                                snippet = content[start:end].replace("\n", " ")
                                
                                # Ignore if it looks like a variable name or placeholder
                                if "os.getenv" in snippet or "os.environ" in snippet:
                                    continue
                                    
                                warnings.append(f"EXPOSED SECRET ({key_type}) in {path}: ...{snippet}...")
                except Exception as e:
                    pass

    # Report
    print("\n" + "="*40)
    print("AUDIT RESULTS")
    print("="*40)
    
    if not issues and not warnings:
        print("✅ PASSED. No critical issues found.")
    else:
        if issues:
            print("\n🚨 CRITICAL ISSUES:")
            for i in issues: print(f" - {i}")
            
        if warnings:
            print("\n⚠️  WARNINGS (Verify Manually):")
            for w in warnings: print(f" - {w}")

if __name__ == "__main__":
    check_security_basics()
