from flask import Flask
import locale

# Set up locale for currency formatting
locale.setlocale(locale.LC_ALL, '')

def currency(value):
    """Format value as currency."""
    if value is None:
        return ""
    try:
        return locale.currency(float(value), grouping=True)
    except (ValueError, TypeError):
        return str(value)

def register_filters(app: Flask):
    """Register all custom filters with the Flask app."""
    app.jinja_env.filters['currency'] = currency