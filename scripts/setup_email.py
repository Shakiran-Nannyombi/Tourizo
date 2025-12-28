#!/usr/bin/env python3
"""
Email Configuration Setup Script for Tourizo
This script helps you set up email configuration for password reset functionality.
"""

import os
from dotenv import load_dotenv

def create_env_file():
    """Create a .env file with email configuration template"""
    
    # Check if .env file already exists
    if os.path.exists('.env'):
        print(" .env file already exists!")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return
    
    print("\n Tourizo Email Configuration Setup")
    print("=" * 50)
    
    # Get email configuration from user
    print("\n Email Configuration:")
    print("Choose your email provider:")
    print("1. Gmail")
    print("2. SendGrid")
    print("3. Mailgun")
    print("4. Custom SMTP")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        # Gmail configuration
        print("\n Gmail Configuration:")
        print("Note: You need to enable 2-Factor Authentication and generate an App Password")
        print("1. Go to https://myaccount.google.com/security")
        print("2. Enable 2-Step Verification")
        print("3. Go to App passwords")
        print("4. Generate a password for 'Mail'")
        
        email = input("Enter your Gmail address: ").strip()
        app_password = input("Enter your Gmail App Password: ").strip()
        
        config = f"""# Database Configuration
DATABASE_URL=mysql+pymysql://root:@localhost/travel_app

# Flask Configuration
SECRET_KEY=your-secret-key-here

# Email Configuration (Gmail)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME={email}
MAIL_PASSWORD={app_password}
MAIL_DEFAULT_SENDER=noreply@tourizo.com

# Admin email for contact inquiries
ADMIN_EMAIL={email}
"""
    
    elif choice == "2":
        # SendGrid configuration
        print("\n SendGrid Configuration:")
        api_key = input("Enter your SendGrid API Key: ").strip()
        
        config = f"""# Database Configuration
DATABASE_URL=mysql+pymysql://root:@localhost/travel_app

# Flask Configuration
SECRET_KEY=your-secret-key-here

# Email Configuration (SendGrid)
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=apikey
MAIL_PASSWORD={api_key}
MAIL_DEFAULT_SENDER=noreply@tourizo.com

# Admin email for contact inquiries
ADMIN_EMAIL=admin@tourizo.com
"""
    
    elif choice == "3":
        # Mailgun configuration
        print("\n Mailgun Configuration:")
        username = input("Enter your Mailgun username: ").strip()
        password = input("Enter your Mailgun password: ").strip()
        
        config = f"""# Database Configuration
DATABASE_URL=mysql+pymysql://root:@localhost/travel_app

# Flask Configuration
SECRET_KEY=your-secret-key-here

# Email Configuration (Mailgun)
MAIL_SERVER=smtp.mailgun.org
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME={username}
MAIL_PASSWORD={password}
MAIL_DEFAULT_SENDER=noreply@tourizo.com

# Admin email for contact inquiries
ADMIN_EMAIL=admin@tourizo.com
"""
    
    elif choice == "4":
        # Custom SMTP configuration
        print("\nCustom SMTP Configuration:")
        server = input("Enter SMTP server (e.g., smtp.gmail.com): ").strip()
        port = input("Enter SMTP port (e.g., 587): ").strip()
        username = input("Enter SMTP username: ").strip()
        password = input("Enter SMTP password: ").strip()
        use_tls = input("Use TLS? (y/N): ").strip().lower() == 'y'
        
        config = f"""# Database Configuration
DATABASE_URL=mysql+pymysql://root:@localhost/travel_app

# Flask Configuration
SECRET_KEY=your-secret-key-here

# Email Configuration (Custom SMTP)
MAIL_SERVER={server}
MAIL_PORT={port}
MAIL_USE_TLS={str(use_tls).lower()}
MAIL_USERNAME={username}
MAIL_PASSWORD={password}
MAIL_DEFAULT_SENDER=noreply@tourizo.com

# Admin email for contact inquiries
ADMIN_EMAIL=admin@tourizo.com
"""
    
    else:
        print(" Invalid choice!")
        return
    
    # Write configuration to .env file
    try:
        with open('.env', 'w') as f:
            f.write(config)
        
        print("\n .env file created successfully!")
        print("\n Next steps:")
        print("1. Restart your Flask application")
        print("2. Test email configuration by visiting: http://127.0.0.1:5000/auth/debug/test-email")
        print("3. Try the password reset functionality")
        
    except Exception as e:
        print(f" Error creating .env file: {e}")

def test_configuration():
    """Test the current email configuration"""
    load_dotenv()
    
    print("\nTesting Email Configuration:")
    print("=" * 40)
    
    required_vars = ['MAIL_SERVER', 'MAIL_PORT', 'MAIL_USERNAME', 'MAIL_PASSWORD']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        else:
            # Hide password for security
            display_value = value if var != 'MAIL_PASSWORD' else '*' * len(value)
            print(f"{var}: {display_value}")
    
    if missing_vars:
        print(f"\n Missing configuration: {', '.join(missing_vars)}")
        print("Please run the setup script to configure email settings.")
    else:
        print("\n All required email configurations are set!")
        print("You can test the configuration by visiting:")
        print("http://127.0.0.1:5000/auth/debug/test-email")

if __name__ == "__main__":
    print("🌿 Tourizo Email Setup")
    print("=" * 30)
    
    if os.path.exists('.env'):
        print("1. Test current configuration")
        print("2. Create new .env file (overwrite existing)")
        choice = input("\nEnter your choice (1-2): ").strip()
        
        if choice == "1":
            test_configuration()
        elif choice == "2":
            create_env_file()
        else:
            print(" Invalid choice!")
    else:
        create_env_file() 