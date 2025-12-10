# Lucky Draw API - cURL Commands

Base URL: `https://lucky-draw.fly.dev`

---

## 🔐 Authentication & User Management

### 1. Get All Users
```bash
curl --location 'https://lucky-draw.fly.dev/api/users' \
--header 'accept: application/json' \
--header 'origin: https://algofolks.com'
```

---

## 📝 Registration APIs

### 2. Initiate Registration (Step 1 - Send OTP)
```bash
curl --location 'https://lucky-draw.fly.dev/api/register/initiate' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'name=John Doe' \
--data-urlencode 'email=john@example.com' \
--data-urlencode 'phone=+1234567890' \
--data-urlencode 'image=@/path/to/image.jpg'
```

**Note:** For image upload, use `-F` flag:
```bash
curl --location 'https://lucky-draw.fly.dev/api/register/initiate' \
--form 'name="John Doe"' \
--form 'email="john@example.com"' \
--form 'phone="+1234567890"' \
--form 'image=@"/path/to/image.jpg"'
```

### 3. Verify Registration (Step 2 - Verify OTPs)
```bash
curl --location 'https://lucky-draw.fly.dev/api/register/verify' \
--header 'Content-Type: application/json' \
--data '{
    "temp_id": "your_temp_id_from_step1",
    "email_otp": "123456",
    "phone_otp": "654321"
}'
```

---

## 🎯 Winner Selection

### 4. Select Winners
```bash
curl --location 'https://lucky-draw.fly.dev/api/select-winners' \
--header 'accept: application/json'
```

---

## 📢 Announcement APIs

### 5. Get All Announcements
```bash
curl --location 'https://lucky-draw.fly.dev/api/announcement' \
--header 'accept: application/json'
```

### 6. Create New Announcement (Replaces all previous)
```bash
curl --location 'https://lucky-draw.fly.dev/api/announcement' \
--header 'Content-Type: application/json' \
--data '{
    "title": "New Lucky Draw Announcement",
    "description": "This is the announcement description",
    "announcement_date": "2025-12-09 10:00:00"
}'
```

### 7. Send Announcement Reminders to All Users
```bash
curl --location 'https://lucky-draw.fly.dev/api/send-announcement-reminders' \
--header 'accept: application/json'
```

### 8. Send Results Notification (by Announcement ID)
```bash
curl --location 'https://lucky-draw.fly.dev/api/send-results-notification/1' \
--header 'accept: application/json'
```
**Replace `1` with the actual announcement ID**

---

## 📧 Email Templates (Preview)

### 9. Preview Announcement Email Template
```bash
curl --location 'https://lucky-draw.fly.dev/api/announcement-email' \
--header 'accept: text/html'
```
**Opens in browser to preview email template**

### 10. Preview Results Email Template
```bash
curl --location 'https://lucky-draw.fly.dev/api/test/email/results/1' \
--header 'accept: text/html'
```
**Replace `1` with announcement ID**

---

## 🔐 Admin APIs (Requires Cookie Authentication)

### 11. Login (Get Cookie)
```bash
curl --location 'https://lucky-draw.fly.dev/' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--cookie-jar cookies.txt \
--data-urlencode 'email=admin@gmail.com' \
--data-urlencode 'password=Algo@987!'
```

### 12. Get Registrations Page (Requires Login Cookie)
```bash
curl --location 'https://lucky-draw.fly.dev/registrations' \
--header 'accept: text/html' \
--cookie cookies.txt
```

### 13. Send Bulk Email - Announcement Template
```bash
curl --location 'https://lucky-draw.fly.dev/send-bulk-email/announcement' \
--header 'Content-Type: application/json' \
--cookie cookies.txt \
--request POST
```

### 14. Send Bulk Email - Results Template
```bash
curl --location 'https://lucky-draw.fly.dev/send-bulk-email/results' \
--header 'Content-Type: application/json' \
--cookie cookies.txt \
--request POST
```

---

## 📁 File Access

### 15. Access Uploaded File
```bash
curl --location 'https://lucky-draw.fly.dev/uploads/filename.jpg' \
--header 'accept: image/jpeg'
```
**Replace `filename.jpg` with actual filename**

---

## 🧪 Test Endpoints

### 16. Test Send Results Notification
```bash
curl --location 'https://lucky-draw.fly.dev/api/test/send-results/1' \
--header 'accept: application/json'
```
**Replace `1` with announcement ID**

---

## 📋 Complete Example Workflow

### Step 1: Register a User
```bash
# Initiate registration
curl --location 'https://lucky-draw.fly.dev/api/register/initiate' \
--form 'name="John Doe"' \
--form 'email="john@example.com"' \
--form 'phone="+1234567890"' \
--form 'image=@"/path/to/image.jpg"'

# Response will contain temp_id, save it!
# You'll receive OTPs via email and SMS
```

### Step 2: Verify Registration
```bash
curl --location 'https://lucky-draw.fly.dev/api/register/verify' \
--header 'Content-Type: application/json' \
--data '{
    "temp_id": "temp_id_from_step1",
    "email_otp": "123456",
    "phone_otp": "654321"
}'
```

### Step 3: Create Announcement
```bash
curl --location 'https://lucky-draw.fly.dev/api/announcement' \
--header 'Content-Type: application/json' \
--data '{
    "title": "Lucky Draw Results",
    "description": "Check out the winners!",
    "announcement_date": "2025-12-09 10:00:00"
}'
```

### Step 4: Send Notifications
```bash
# Send announcement reminders
curl --location 'https://lucky-draw.fly.dev/api/send-announcement-reminders'

# Send results notification (replace 1 with announcement ID)
curl --location 'https://lucky-draw.fly.dev/api/send-results-notification/1'
```

### Step 5: Select Winners
```bash
curl --location 'https://lucky-draw.fly.dev/api/select-winners'
```

---

## 🔍 Common Headers

For CORS-enabled requests:
```bash
--header 'origin: https://algofolks.com' \
--header 'accept: application/json'
```

For JSON requests:
```bash
--header 'Content-Type: application/json'
```

For form data:
```bash
--header 'Content-Type: application/x-www-form-urlencoded'
```

---

## ⚠️ Notes

1. **CORS Origins**: Make sure your frontend domain is in `CORS_ORIGINS` secret
2. **Admin Access**: Admin endpoints require cookie authentication
3. **File Uploads**: Use `-F` or `--form` for multipart/form-data
4. **OTP**: OTPs are sent via email and SMS (Twilio)
5. **Announcements**: Creating a new announcement deletes all previous ones

---

## 🐛 Troubleshooting

### Check if API is running:
```bash
curl --location 'https://lucky-draw.fly.dev/api/users'
```

### View logs:
```bash
flyctl logs --app lucky-draw
```

### Check app status:
```bash
flyctl status --app lucky-draw
```

