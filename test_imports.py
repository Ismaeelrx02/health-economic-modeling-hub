"""
Test script to verify all imports work correctly.
Run this to diagnose import errors before deployment.
"""
import sys
import traceback

def test_import(module_name, description):
    """Test importing a module"""
    try:
        if '.' in module_name:
            parts = module_name.split('.')
            obj = __import__(module_name)
            for part in parts[1:]:
                obj = getattr(obj, part)
        else:
            __import__(module_name)
        print(f"✅ {description}: OK")
        return True
    except Exception as e:
        print(f"❌ {description}: FAILED")
        print(f"   Error: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all import tests"""
    print("=" * 60)
    print("IMPORT TESTING - Health Economic Modeling Hub")
    print("=" * 60)
    
    tests = [
        ("dash", "Dash Framework"),
        ("dash_bootstrap_components", "Dash Bootstrap Components"),
        ("plotly", "Plotly"),
        ("pandas", "Pandas"),
        ("numpy", "NumPy"),
        ("scipy", "SciPy"),
        ("sqlalchemy", "SQLAlchemy"),
        ("config.settings", "Config Settings"),
        ("database", "Database Package"),
        ("database.models", "Database Models"),
        ("database.connection", "Database Connection"),
        ("database.services", "Database Services"),
        ("services.ai_service", "AI Service"),
        ("components.ai.AIChat", "AI Chat Component"),
    ]
    
    passed = 0
    failed = 0
    
    for module, desc in tests:
        if test_import(module, desc):
            passed += 1
        else:
            failed += 1
        print()
    
    print("=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed > 0:
        print("\n⚠️  Some imports failed. Fix these before deploying!")
        sys.exit(1)
    else:
        print("\n✅ All imports successful! Ready to deploy.")
        sys.exit(0)

if __name__ == "__main__":
    main()
