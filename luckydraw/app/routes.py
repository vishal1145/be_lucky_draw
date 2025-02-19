@main_bp.route('/preview/welcome-email')
def preview_welcome_email():
    return render_template('emails/welcome_email.html', name="John Doe") 