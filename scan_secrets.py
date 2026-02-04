import os
import re

def scan_for_secrets(start_dir):
    # Regex patterns for common keys
    patterns = {
        "Google API Key": r"AIza[0-9A-Za-z-_]{35}",
        "Generic Secret": r"(?i)(api_key|secret|password|token)\s*=\s*['\"][A-Za-z0-9-_\.]+['\"]",
        "OpenAI Key": r"sk-[a-zA-Z0-9]{48}"
    }

    findings = []
    
    # Files/Dirs to ignore
    ignore_dirs = {".git", ".agent", "venv", "__pycache__", "node_modules", ".pytest_cache"}
    ignore_files = {".env", "scan_secrets.py", "audit_codebase.py"}

    print(f"🕵️  Scanning for secrets in {start_dir}...")

    for root, dirs, files in os.walk(start_dir):
        # Filter out ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        for file in files:
            if file in ignore_files or file.endswith(".pyc") or file.endswith(".png"):
                continue
                
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    for key_type, pattern in patterns.items():
                        matches = re.finditer(pattern, content)
                        for match in matches:
                            # Verify it's not a placeholder (e.g. "YOUR_API_KEY")
                            val = match.group(0)
                            if "YOUR_" in val or "EXAMPLE" in val or "os.environ" in val or "getenv" in val:
                                continue
                                
                            # Check if line is commented out (Python/JS)
                            start_pos = max(0, content.rfind('\n', 0, match.start()))
                            line = content[start_pos:match.end()].strip()
                            if line.startswith("#") or line.startswith("//"):
                                continue

                            findings.append(f"⚠️  {key_type} found in {filepath}: {val[:10]}...")
            except Exception as e:
                pass

    if findings:
        print("\n🚨 Potential Secrets Found:")
        for f in findings:
            print(f"  - {f}")
    else:
        print("\n✅ No hardcoded secrets detected in source code.")

if __name__ == "__main__":
    scan_for_secrets(".")
