from rabbitQ_setup import get_mq_connection

channel = get_mq_connection()
def callback(ch, method, properties, body):
   print(f"Received message: {body}")

channel.basic_consume(
   queue='test_queue',
   on_message_callback=callback,
   auto_ack=True
)
print("Waiting for messages...")
channel.start_consuming()