import json
import pika, json

def get_mq_connection():
# Connection parameters
    connection_params = pika.ConnectionParameters(
    host='localhost',
    port=5672,
    credentials=pika.PlainCredentials('guest', 'guest')
    )
    # Establish connection and channel
    connection = pika.BlockingConnection(connection_params)
    # channel = connection.channel()
    # # Declare a queue
    # channel.queue_declare(queue='test_queue')
    print("Connected to RabbitMQ.")

    return connection
# channel.basic_publish(
#    exchange='',
#    routing_key='test_queue',
#    body='Hello, RabbitMQ!'
# )
# print("Message sent!")

# def callback(ch, method, properties, body):
#    print(f"Received message: {body}")

# channel.basic_consume(
#    queue='test_queue',
#    on_message_callback=callback,
#    auto_ack=True
# )
# print("Waiting for messages...")
# channel.start_consuming()

def send_email_message(payload):
    connection = get_mq_connection()
    channel = connection.channel()
    # Declare queue
    channel.queue_declare(queue='email_queue', durable=True)
    
    # Publish message
    channel.basic_publish(
        exchange='',
        routing_key='email_queue',
        body=json.dumps(payload),
        properties=pika.BasicProperties(
            delivery_mode=2  # make message persistent
        )
    )
    connection.close()
