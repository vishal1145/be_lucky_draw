from app import db
from app.models.registration import Registration
from app.models.announcement import Announcement
from app.services.email_service import mail
from flask import render_template
from datetime import datetime, timedelta
from flask_mail import Message

class AnnouncementService:
    @staticmethod
    def send_announcement_reminders():
        print("=== Start: send_announcement_reminders ===")

        # Get announcements that are 3 days away
        from sqlalchemy import func

        three_days_from_now = datetime.utcnow() + timedelta(days=3)
        print(f"Checking for announcements on (formatted date): {three_days_from_now.date()}")

        upcoming_announcements = Announcement.query.filter(
            func.date(Announcement.announcement_date) == three_days_from_now.date()
        ).all()

        if not upcoming_announcements:
            print(f"No announcements found for {three_days_from_now.date()}")
            return

        print(f"Found {len(upcoming_announcements)} announcements:")
        for ann in upcoming_announcements:
            print(f"- Announcement: {ann.id}, Title: {ann.title}, Date: {ann.announcement_date}")

        # Get all registered users
        registered_users = Registration.query.filter_by(is_active=True).all()

        if not registered_users:
            print("No active registered users found")
            return

        print(f"Found {len(registered_users)} active users:")
        for user in registered_users:
            print(f"- User: {user.id}, Email: {user.email}, Active: {user.is_active}")

        for announcement in upcoming_announcements:
            print(f"Processing announcement: {announcement.title}")

            for user in registered_users:
                try:
                    msg = None

                    msg = Message(
                        subject=f"Reminder: Upcoming Announcement - {announcement.title}",
                        recipients=[user.email]
                    )

                    msg.html = render_template(
                        'emails/announcement_reminder.html',
                        announcement=announcement,
                        name=user.name,
                        share_url="https://algofolks.com"
                    )

                    print(f"Sending email to {user.email}...")
                    mail.send(msg)
                    print(f"✅ Successfully sent reminder to {user.email}")

                except Exception as e:
                    print(f"❌ Failed to send email to {user.email}: {str(e)}")
                    continue

        print("=== End: send_announcement_reminders ===")

    @staticmethod
    def send_results_notification(announcement):
        print("=== Start: send_results_notification ===")
        
        # Get all registered users
        registered_users = Registration.query.filter_by(is_active=True).all()

        if not registered_users:
            print("No active registered users found")
            return

        print(f"Found {len(registered_users)} active users to notify about results")

        for user in registered_users:
            try:
                msg = Message(
                    subject=f"Results Available - {announcement.title}",
                    recipients=[user.email]
                )

                # Render email template
                msg.html = render_template(
                    'emails/results_notification.html',
                    announcement=announcement,
                    name=user.name,
                    share_url="https://algofolks.com"
                )

                print(f"Sending results notification to {user.email}...")
                mail.send(msg)
                print(f"✅ Successfully sent results notification to {user.email}")

            except Exception as e:
                print(f"❌ Failed to send results notification to {user.email}: {str(e)}")
                continue

        print("=== End: send_results_notification ===")
