# app/email_service.py
from flask import current_app
from flask_mail import Message
from app.extensions import mail
import logging

logger = logging.getLogger(__name__)

def send_otp_email(email, otp):
    """Send OTP via email with better error handling"""
    try:
        # Check if email configuration is properly set
        if not current_app.config.get('MAIL_USERNAME') or not current_app.config.get('MAIL_PASSWORD'):
            logger.error("Email configuration missing: MAIL_USERNAME or MAIL_PASSWORD not set")
            return False
            
        msg = Message(
            'Tourizo - Password Reset Code',
            sender=('Tourizo', current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@tourizo.com')),
            recipients=[email]
        )
        
        msg.html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="text-align: center; margin-bottom: 30px;">
                <h2 style="color: #43a047; margin: 0;">🌿 Tourizo</h2>
                <p style="color: #666; margin: 5px 0;">Your Adventure Awaits</p>
            </div>
            
            <div style="background: #f9f9f9; padding: 30px; border-radius: 10px; text-align: center;">
                <h3 style="color: #333; margin-bottom: 20px;">Password Reset Request</h3>
                <p style="color: #666; margin-bottom: 25px;">
                    You requested a password reset for your Tourizo account. 
                    Use the code below to reset your password:
                </p>
                
                <div style="background: #43a047; color: white; padding: 20px; border-radius: 8px; font-size: 24px; font-weight: bold; letter-spacing: 5px; margin: 20px 0;">
                    {otp}
                </div>
                
                <p style="color: #666; font-size: 14px; margin-bottom: 20px;">
                    This code will expire in <strong>15 minutes</strong>.
                </p>
                
                <p style="color: #999; font-size: 12px;">
                    If you didn't request this password reset, please ignore this email.
                </p>
            </div>
            
            <div style="text-align: center; margin-top: 30px; color: #999; font-size: 12px;">
                <p>© 2024 Tourizo. All rights reserved.</p>
            </div>
        </div>
        """
        
        msg.body = f"""
        Tourizo - Password Reset Code
        
        You requested a password reset for your Tourizo account.
        Use the code below to reset your password:
        
        {otp}
        
        This code will expire in 15 minutes.
        
        If you didn't request this password reset, please ignore this email.
        
        © 2024 Tourizo. All rights reserved.
        """
        
        mail.send(msg)
        logger.info(f"✅ Email sent successfully to {email}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to send email to {email}: {e}")
        return False

def test_email_configuration():
    """Test email configuration and return status"""
    config_status = {
        'MAIL_SERVER': current_app.config.get('MAIL_SERVER'),
        'MAIL_PORT': current_app.config.get('MAIL_PORT'),
        'MAIL_USE_TLS': current_app.config.get('MAIL_USE_TLS'),
        'MAIL_USERNAME': current_app.config.get('MAIL_USERNAME'),
        'MAIL_PASSWORD_SET': bool(current_app.config.get('MAIL_PASSWORD')),
        'MAIL_DEFAULT_SENDER': current_app.config.get('MAIL_DEFAULT_SENDER')
    }
    
    missing_configs = [key for key, value in config_status.items() 
                      if not value and key != 'MAIL_PASSWORD_SET']
    
    if missing_configs:
        logger.error(f"Missing email configurations: {missing_configs}")
        return False, config_status
    
    return True, config_status
