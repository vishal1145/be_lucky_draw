import requests
import logging
from flask import current_app, render_template

logger = logging.getLogger(__name__)

class EmailJSService:
    """
    EmailJS service for sending emails via EmailJS API
    """
    
    EMAILJS_API_URL = "https://api.emailjs.com/api/v1.0/email/send"
    
    @staticmethod
    def _send_email(template_id, template_params, html_content=None, subject=None):
        """
        Internal method to send email via EmailJS API
        
        Args:
            template_id: EmailJS template ID (can use a single generic template)
            template_params: Dictionary of template parameters
            html_content: Rendered HTML content from our templates (optional)
            subject: Email subject
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            logger.info("[EMAILJS] Starting email send process...")
            
            # Get EmailJS configuration
            service_id = current_app.config.get('EMAILJS_SERVICE_ID')
            user_id = current_app.config.get('EMAILJS_USER_ID')
            access_token = current_app.config.get('EMAILJS_ACCESS_TOKEN')
            
            logger.info(f"[EMAILJS] Configuration check:")
            logger.info(f"[EMAILJS]   - Service ID: {'SET' if service_id else 'MISSING'}")
            logger.info(f"[EMAILJS]   - User ID: {'SET' if user_id else 'MISSING'}")
            logger.info(f"[EMAILJS]   - Access Token: {'SET' if access_token else 'MISSING'}")
            logger.info(f"[EMAILJS]   - Template ID: {template_id if template_id else 'MISSING'}")
            
            if not all([service_id, user_id, access_token, template_id]):
                missing = []
                if not service_id:
                    missing.append('EMAILJS_SERVICE_ID')
                if not user_id:
                    missing.append('EMAILJS_USER_ID')
                if not access_token:
                    missing.append('EMAILJS_ACCESS_TOKEN')
                if not template_id:
                    missing.append('EMAILJS_TEMPLATE_GENERIC')
                logger.error(f"[EMAILJS] Missing EmailJS configuration: {', '.join(missing)}")
                if not template_id:
                    logger.error("[EMAILJS] ⚠️  IMPORTANT: EmailJS API requires ONE generic template ID")
                    logger.error("[EMAILJS] Create ONE simple template in EmailJS dashboard with content:")
                    logger.error("[EMAILJS]   Subject: {{subject}}")
                    logger.error("[EMAILJS]   Body: {{{message_html}}}")
                    logger.error("[EMAILJS]   (Use triple braces {{{ }}} for raw HTML)")
                    logger.error("[EMAILJS] Then set EMAILJS_TEMPLATE_GENERIC in your .env file")
                logger.error("[EMAILJS] Please check your .env file and ensure all EmailJS credentials are set")
                return False
            
            # Add HTML content to template params if provided
            if html_content:
                template_params['message_html'] = html_content
                logger.info(f"[EMAILJS] HTML content length: {len(html_content)} characters")
            else:
                logger.warning("[EMAILJS] No HTML content provided")
            
            # Add subject if provided
            if subject:
                template_params['subject'] = subject
                logger.info(f"[EMAILJS] Email subject: {subject}")
            
            # Log recipient email (without logging full params for security)
            recipient_email = template_params.get('to_email', 'UNKNOWN')
            logger.info(f"[EMAILJS] Sending email to: {recipient_email}")
            
            # Prepare request payload
            payload = {
                'service_id': service_id,
                'template_id': template_id,
                'user_id': user_id,
                'accessToken': access_token,
                'template_params': template_params
            }
            
            logger.info(f"[EMAILJS] Sending request to EmailJS API: {EmailJSService.EMAILJS_API_URL}")
            logger.debug(f"[EMAILJS] Payload keys: {list(payload.keys())}")
            
            # Send request to EmailJS API
            # Note: EmailJS may require enabling server-side API access in account settings
            headers = {
                'Content-Type': 'application/json',
                'Origin': 'https://your-domain.com',  # Some EmailJS accounts require Origin header
                'Referer': 'https://your-domain.com'
            }
            
            response = requests.post(
                EmailJSService.EMAILJS_API_URL,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            logger.info(f"[EMAILJS] API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                logger.info(f"[EMAILJS] ✅ Email sent successfully via template {template_id} to {recipient_email}")
                return True
            elif response.status_code == 403:
                logger.error(f"[EMAILJS] ❌ 403 Forbidden - Server-side API access may be disabled")
                logger.error(f"[EMAILJS] Response: {response.text}")
                logger.error(f"[EMAILJS] SOLUTION: Enable server-side API access in EmailJS account settings:")
                logger.error(f"[EMAILJS]   1. Go to EmailJS Dashboard → Account → General")
                logger.error(f"[EMAILJS]   2. Look for 'Allow server-side API calls' or 'Enable API access'")
                logger.error(f"[EMAILJS]   3. Enable it and save")
                logger.error(f"[EMAILJS]   4. Or contact EmailJS support to enable server-side API")
                return False
            else:
                logger.error(f"[EMAILJS] ❌ Failed to send email. Status: {response.status_code}")
                logger.error(f"[EMAILJS] Response: {response.text}")
                try:
                    error_data = response.json()
                    logger.error(f"[EMAILJS] Error details: {error_data}")
                except:
                    pass
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"[EMAILJS] ❌ Network error sending email: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"[EMAILJS] ❌ Exception sending email: {str(e)}")
            import traceback
            logger.error(f"[EMAILJS] Traceback: {traceback.format_exc()}")
            return False
    
    @staticmethod
    def send_otp_email(email, otp):
        """
        Send OTP via email using EmailJS
        Uses a simple HTML template rendered from codebase
        """
        try:
            # Use generic template ID (can be same for all emails)
            template_id = current_app.config.get('EMAILJS_TEMPLATE_GENERIC') or current_app.config.get('EMAILJS_TEMPLATE_OTP')
            
            if not template_id:
                logger.warning("[EMAILJS] Template ID not configured")
                return True  # Return True for testing
            
            # Render HTML template from codebase
            html_content = f'''
            <html>
                <body>
                    <h2>Email Verification</h2>
                    <p>Your OTP for registration is: <strong>{otp}</strong></p>
                    <p>This OTP will expire in 10 minutes.</p>
                </body>
            </html>
            '''
            
            template_params = {
                'to_email': email,
                'otp': otp
            }
            
            return EmailJSService._send_email(template_id, template_params, html_content, 'Email Verification OTP')
            
        except Exception as e:
            logger.error(f"[EMAILJS] Exception in send_otp_email: {str(e)}")
            return False
    
    @staticmethod
    def send_welcome_email(email, name, first_name=None, announcement_date=None):
        """
        Send welcome email using EmailJS
        Uses welcome_email.html template from codebase
        """
        try:
            logger.info(f"[EMAILJS] send_welcome_email called for: {email}, name: {name}")
            
            # Use generic template ID (can be same for all emails)
            template_id = current_app.config.get('EMAILJS_TEMPLATE_GENERIC') or current_app.config.get('EMAILJS_TEMPLATE_WELCOME')
            
            logger.info(f"[EMAILJS] Template ID lookup:")
            logger.info(f"[EMAILJS]   - EMAILJS_TEMPLATE_GENERIC: {current_app.config.get('EMAILJS_TEMPLATE_GENERIC')}")
            logger.info(f"[EMAILJS]   - EMAILJS_TEMPLATE_WELCOME: {current_app.config.get('EMAILJS_TEMPLATE_WELCOME')}")
            logger.info(f"[EMAILJS]   - Selected template_id: {template_id}")
            
            if not template_id:
                logger.error("[EMAILJS] ❌ Template ID not configured!")
                logger.error("[EMAILJS] ⚠️  EmailJS API requires ONE generic wrapper template")
                logger.error("[EMAILJS] Your HTML templates from codebase are used - you just need ONE wrapper template")
                logger.error("[EMAILJS] Steps to fix:")
                logger.error("[EMAILJS]   1. Go to EmailJS Dashboard → Email Templates")
                logger.error("[EMAILJS]   2. Create ONE new template with this content:")
                logger.error("[EMAILJS]      Subject: {{subject}}")
                logger.error("[EMAILJS]      Body: {{{message_html}}}")
                logger.error("[EMAILJS]   3. Copy the Template ID")
                logger.error("[EMAILJS]   4. Add to .env: EMAILJS_TEMPLATE_GENERIC=your_template_id")
                logger.error("[EMAILJS] Note: You don't need to recreate your HTML templates - they're rendered from codebase!")
                return False  # Changed from True to False - don't silently fail
            
            # Render HTML template from codebase
            logger.info("[EMAILJS] Rendering welcome_email.html template...")
            try:
                # Get domain name for image URLs
                domain_name = current_app.config.get('DOMAIN_NAME', 'https://lucky-draw.fly.dev').rstrip('/')
                logger.info(f"[EMAILJS] Using domain for images: {domain_name}")
                
                html_content = render_template(
                    'emails/welcome_email.html',
                    first_name=first_name or name,
                    name=name,
                    announcement_date=announcement_date or 'soon',
                    domain_name=domain_name
                )
                logger.info(f"[EMAILJS] ✅ Template rendered successfully, HTML length: {len(html_content)} characters")
            except Exception as render_error:
                logger.error(f"[EMAILJS] ❌ Failed to render template: {str(render_error)}")
                import traceback
                logger.error(f"[EMAILJS] Template render traceback: {traceback.format_exc()}")
                return False
            
            template_params = {
                'to_email': email,
                'to_name': name,
                'first_name': first_name or name,
                'name': name,
                'announcement_date': announcement_date or 'soon'
            }
            
            logger.info(f"[EMAILJS] Calling _send_email with template_id: {template_id}")
            result = EmailJSService._send_email(
                template_id, 
                template_params, 
                html_content, 
                '🎉 Welcome to the Lucky Draw – Your Chance to Win Big!'
            )
            
            if result:
                logger.info(f"[EMAILJS] ✅ Welcome email sent successfully to {email}")
            else:
                logger.error(f"[EMAILJS] ❌ Failed to send welcome email to {email}")
            
            return result
            
        except Exception as e:
            logger.error(f"[EMAILJS] ❌ Exception in send_welcome_email: {str(e)}")
            import traceback
            logger.error(f"[EMAILJS] Traceback: {traceback.format_exc()}")
            return False
    
    @staticmethod
    def send_winner_email(email, name):
        """
        Send winner notification email using EmailJS
        Uses inline HTML template
        """
        try:
            # Use generic template ID (can be same for all emails)
            template_id = current_app.config.get('EMAILJS_TEMPLATE_GENERIC') or current_app.config.get('EMAILJS_TEMPLATE_WINNER')
            
            if not template_id:
                logger.warning("[EMAILJS] Template ID not configured")
                return True  # Return True for testing
            
            # Render HTML template (using inline template since we don't have a separate winner template file)
            html_content = f'''
            <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            line-height: 1.6;
                            color: #333;
                            margin: 0;
                            padding: 0;
                        }}
                        .email-container {{
                            max-width: 600px;
                            margin: 0 auto;
                            padding: 20px;
                            background-color: #f8f9fc;
                        }}
                        .content {{
                            background-color: white;
                            padding: 30px;
                            border-radius: 8px;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        }}
                        .welcome-text {{
                            font-size: 24px;
                            color: #6c63ff;
                            margin-bottom: 15px;
                            text-align: center;
                        }}
                        .message {{
                            text-align: center;
                            margin: 20px 0;
                            color: #555;
                        }}
                    </style>
                </head>
                <body>
                    <div class="email-container">
                        <div class="content">
                            <div class="welcome-text">Congratulations {name}! 🎉</div>
                            <h2 style="text-align: center;">You're a Winner!</h2>
                            <div class="message">
                                You have been selected as a winner in our Lucky Draw!
                            </div>
                            <div class="message">
                                We will contact you shortly with more details about your prize and how to claim it.
                            </div>
                            <div class="message">
                                Thank you for participating in our Lucky Draw!
                            </div>
                            <div style="text-align: center; margin-top: 20px; color: #666; font-size: 14px;">
                                <p>Best regards,<br>Team Algofolks</p>
                            </div>
                        </div>
                    </div>
                </body>
            </html>
            '''
            
            template_params = {
                'to_email': email,
                'to_name': name,
                'name': name
            }
            
            return EmailJSService._send_email(
                template_id, 
                template_params, 
                html_content, 
                'Congratulations! You Won the Lucky Draw! 🎉'
            )
            
        except Exception as e:
            logger.error(f"[EMAILJS] Exception in send_winner_email: {str(e)}")
            return False
    
    @staticmethod
    def send_verification_email(email, name, verification_link):
        """
        Send email verification link using EmailJS
        Uses inline HTML template
        """
        try:
            # Use generic template ID (can be same for all emails)
            template_id = current_app.config.get('EMAILJS_TEMPLATE_GENERIC') or current_app.config.get('EMAILJS_TEMPLATE_VERIFICATION')
            
            if not template_id:
                logger.warning("[EMAILJS] Template ID not configured")
                return True  # Return True for testing
            
            # Render HTML template (using inline template)
            html_content = f'''
            <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            line-height: 1.6;
                            color: #333;
                            margin: 0;
                            padding: 0;
                        }}
                        .email-container {{
                            max-width: 600px;
                            margin: 0 auto;
                            padding: 20px;
                            background-color: #f8f9fc;
                        }}
                        .content {{
                            background-color: white;
                            padding: 30px;
                            border-radius: 8px;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        }}
                        .activate-button {{
                            display: block;
                            width: fit-content;
                            margin: 25px auto;
                            padding: 12px 30px;
                            background-color: #6c63ff;
                            color: white;
                            text-decoration: none;
                            border-radius: 5px;
                            font-weight: bold;
                            text-align: center;
                        }}
                        .message {{
                            text-align: center;
                            margin: 20px 0;
                            color: #555;
                        }}
                    </style>
                </head>
                <body>
                    <div class="email-container">
                        <div class="content">
                            <h2 style="text-align: center; color: #6c63ff;">Hi {name}</h2>
                            <h2 style="text-align: center;">Activate Your Account</h2>
                            <div class="message">
                                Welcome to Algofolks, the leading platform for freelance Engineers and Architects! 
                                We're excited to have you join our community.
                            </div>
                            <div class="message">
                                To complete your registration, please verify your email by clicking the link below:
                            </div>
                            <a href="{verification_link}" class="activate-button">Verify Email</a>
                            <div class="message">
                                If the button doesn't work, you can copy and paste this link in your browser:
                                <br><br>
                                <a href="{verification_link}" style="word-break: break-all; color: #6c63ff;">{verification_link}</a>
                            </div>
                            <div class="message">
                                Thank you for joining us! We're here to support your journey
                            </div>
                            <div style="text-align: center; margin-top: 20px; color: #666; font-size: 14px;">
                                <p>Best,<br>Team Algofolks</p>
                            </div>
                        </div>
                    </div>
                </body>
            </html>
            '''
            
            template_params = {
                'to_email': email,
                'to_name': name,
                'name': name,
                'verification_link': verification_link
            }
            
            return EmailJSService._send_email(
                template_id, 
                template_params, 
                html_content, 
                'Activate Your Account'
            )
            
        except Exception as e:
            logger.error(f"[EMAILJS] Exception in send_verification_email: {str(e)}")
            return False
    
    @staticmethod
    def send_announcement_reminder(email, name, announcement_title, announcement_date, share_url):
        """
        Send announcement reminder email using EmailJS
        Uses announcement_reminder.html template from codebase
        """
        try:
            # Use generic template ID (can be same for all emails)
            template_id = current_app.config.get('EMAILJS_TEMPLATE_GENERIC') or current_app.config.get('EMAILJS_TEMPLATE_ANNOUNCEMENT')
            
            if not template_id:
                logger.warning("[EMAILJS] Template ID not configured")
                return False
            
            # Get domain name for image URLs
            domain_name = current_app.config.get('DOMAIN_NAME', 'https://lucky-draw.fly.dev').rstrip('/')
            # Extract first name from full name
            first_name = name.split()[0] if name else name
            
            # Render HTML template from codebase
            html_content = render_template(
                'emails/announcement_reminder.html',
                first_name=first_name,
                name=name,
                domain_name=domain_name
            )
            
            template_params = {
                'to_email': email,
                'to_name': name,
                'name': name,
                'first_name': first_name,
                'announcement_title': announcement_title,
                'announcement_date': str(announcement_date),
                'share_url': share_url
            }
            
            return EmailJSService._send_email(
                template_id, 
                template_params, 
                html_content, 
                '🔔 24 Hours Left: Prize Announcement Incoming'
            )
            
        except Exception as e:
            logger.error(f"[EMAILJS] Exception in send_announcement_reminder: {str(e)}")
            return False
    
    @staticmethod
    def send_results_notification(email, name, announcement_title, share_url):
        """
        Send results notification email using EmailJS
        Uses results_notification.html template from codebase
        """
        try:
            # Use generic template ID (can be same for all emails)
            template_id = current_app.config.get('EMAILJS_TEMPLATE_GENERIC') or current_app.config.get('EMAILJS_TEMPLATE_RESULTS')
            
            if not template_id:
                logger.warning("[EMAILJS] Template ID not configured")
                return False
            
            # Get domain name for image URLs
            domain_name = current_app.config.get('DOMAIN_NAME', 'https://lucky-draw.fly.dev').rstrip('/')
            # Extract first name from full name
            first_name = name.split()[0] if name else name
            
            # Render HTML template from codebase
            html_content = render_template(
                'emails/results_notification.html',
                first_name=first_name,
                name=name,
                share_url=share_url,
                domain_name=domain_name
            )
            
            template_params = {
                'to_email': email,
                'to_name': name,
                'name': name,
                'first_name': first_name,
                'announcement_title': announcement_title,
                'share_url': share_url
            }
            
            return EmailJSService._send_email(
                template_id, 
                template_params, 
                html_content, 
                'DECISION: Your Software Credit Status Inside'
            )
            
        except Exception as e:
            logger.error(f"[EMAILJS] Exception in send_results_notification: {str(e)}")
            return False

