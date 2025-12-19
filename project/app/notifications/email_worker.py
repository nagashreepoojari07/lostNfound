import json
import smtplib
from email.mime.text import MIMEText
from rabbitQ_setup import get_mq_connection

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"Received message: {data}")

    # msg = MIMEText(data['body'], 'html')
    # msg['Subject'] = data['subject']
    # msg['From'] = "nagashreepoojari2017@gmail.com"
    # msg['To'] = data['to']

    # try:
    #     with smtplib.SMTP('smtp.yourprovider.com', 587) as server:
    #         server.starttls()
    #         server.login("smtp_user", "smtp_password")
    #         server.sendmail(msg['From'], [msg['To']], msg.as_string())
    #     print(f"Email sent to {data['to']}")
    #     ch.basic_ack(delivery_tag=method.delivery_tag)
    # except Exception as e:
    #     print("Error sending email:", e)
# def callback(ch, method, properties, body):
#    print(f"Received message: {body}")

connection = get_mq_connection()
channel = connection.channel()
channel.queue_declare(queue='email_queue', durable=True)
channel.basic_consume(
   queue='email_queue',
   on_message_callback=callback,
   auto_ack=True
)
print("Waiting for messages...")
channel.start_consuming()