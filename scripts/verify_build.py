#!/usr/bin/env python
import sys
import importlib

def test_imports():
    modules = [
        'flask',
        'flask_sqlalchemy',
        'flask_login',
        'flask_migrate',
        'langchain',
        'langchain_core',
        'langchain_groq',
        'langchain_community',
        'groq',
        'sqlalchemy',
        'PIL'  # Pillow
    ]
    
    failed = []
    print("Verifying dependencies...")
    for module in modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module} imported successfully")
        except ImportError as e:
            print(f"❌ {module} failed to import: {e}")
            failed.append(module)
            
    if failed:
        print(f"\nError: {len(failed)} dependency checks failed: {', '.join(failed)}")
        sys.exit(1)
    else:
        print("\nAll dependencies verified successfully! ✨")
        sys.exit(0)

if __name__ == "__main__":
    test_imports()
