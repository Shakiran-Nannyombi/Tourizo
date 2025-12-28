import importlib
import pytest
import os
import sys

def test_critical_imports():
    """Verify that all core dependencies can be imported."""
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
        'PIL'
    ]
    for module in modules:
        try:
            importlib.import_module(module)
        except ImportError as e:
            pytest.fail(f"Module {module} failed to import: {e}")

def test_wsgi_entry_point():
    """Verify that wsgi.py exists and contains a valid Flask app instance."""
    # Check file exists
    assert os.path.exists('wsgi.py'), "wsgi.py entry point missing!"
    
    # Try importing the 'app' from wsgi
    try:
        # Add current directory to path to ensure wsgi can be imported
        sys.path.append(os.getcwd())
        from wsgi import app as flask_app
        assert flask_app is not None
        from flask import Flask
        assert isinstance(flask_app, Flask)
    except Exception as e:
        pytest.fail(f"Could not load 'app' from wsgi.py: {e}")
    finally:
        if os.getcwd() in sys.path:
            sys.path.remove(os.getcwd())

def test_requirements_file():
    """Verify requirements.txt looks valid."""
    assert os.path.exists('requirements.txt')
    with open('requirements.txt', 'r') as f:
        content = f.read()
        assert 'Flask' in content
        assert 'gunicorn' in content
