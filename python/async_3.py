import asyncio
import smtplib
from threading import Thread

def send_notification(email):
    """Generate and send the notification email"""
    # Do some work to get email body
    message = ...

    # Connect to the server
    server = smtplib.SMTP("smtp.gmail.com:587")
    server.ehlo()
    server.starttls()
    server.login(username, password)

    # Send the email
    server.sendmail(from_addr, email, message)

    server.quit()

def start_email_worker(loop):
    """Switch to new event loop and run forever"""

    asyncio.set_event_loop(loop)
    loop.run_forever()

# Create the new loop and worker thread
worker_loop = asyncio.new_event_loop()
worker = Thread(target=start_email_worker, args=(worker_loop,))

# Start the thread
worker.start()

# Assume a Flask restful interface endpoint
@app.route("/notify")
def notify(email):
    """Request notification email"""
    worker_loop.call_soon_threadsafe(send_notification, email)
