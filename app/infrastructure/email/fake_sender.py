import smtplib
from email.message import EmailMessage

from app.config import settings

SMTP_HOST = settings.smtp_host
SMTP_PORT = settings.smtp_port
FROM_EMAIL = settings.from_email


def send_login_notification(to_email: str, username: str):
    """
    Send a login notification to a user by email.

    Args:
        to_email: The email address of the user.
        username: The username of the user.

    This function sends an email to the user with a notification of a successful login.
    It includes text and HTML versions of the message.
    """
    subject = "🔐 Inicio de sesión exitoso"

    plain_text = f"""\
Hola {username},

Se ha iniciado sesión exitosamente en tu cuenta.

Si no fuiste tú, por favor cambia tu contraseña inmediatamente.
"""

    html_content = f"""\
<!DOCTYPE html>
<html>
  <body style="font-family: Arial, sans-serif; background-color: #f8f9fa; padding: 20px;">
    <div style="max-width: 600px; margin: auto; background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
      <h2 style="color: #333;">👋 ¡Hola, {username}!</h2>
      <p style="color: #555; font-size: 16px;">
        Te informamos que has iniciado sesión exitosamente en tu cuenta.
      </p>
      <p style="color: #555; font-size: 16px;">
        Si no reconoces esta acción, te recomendamos cambiar tu contraseña lo antes posible.
      </p>
      <hr style="margin-top: 30px; margin-bottom: 20px;">
      <footer style="font-size: 14px; color: #999;">
        Este es un mensaje automático de <strong>MiApp</strong>. Por favor no respondas a este correo.
      </footer>
    </div>
  </body>
</html>
"""

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email

    msg.set_content(plain_text)
    msg.add_alternative(html_content, subtype="html")

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.send_message(msg)
