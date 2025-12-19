import email
from http.client import FOUND
from operator import attrgetter
from flask import Blueprint, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from elasticsearch import Elasticsearch
from common.database_connection import get_db_connection
from notifications.rabbitQ_setup import get_mq_connection, send_email_message
from common.utils import token_required


app = Blueprint('lost_items', __name__, url_prefix='/api/')

@app.route('/test', methods=['GET'])
@token_required
def test():
    return jsonify({"message":"hello"})

@app.route('/items', methods=['GET'])
@token_required
def get_items():
    # data = request.get_json()

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM public.\"lost_item\";",
    )

    items = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(items)

@app.route('/items', methods=['POST'])
@token_required
def post_item():
    data = request.get_json()

    name = data.get("name")
    description = data.get("description")
    user_id = request.current_user['id']  # Access logged-in user data
    

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO public.\"lost_item\" (\"name\", \"description\", \"user_id\") VALUES (%s, %s, %s)",
        (name, description, user_id)
    )
    conn.commit()
    cur.close()
    conn.close()

    message_payload = {
        "to": f"{request.current_user['email_id']}",
        "subject": "LostNFound",
        "body": f"Your Item {name} is missing!!"
        # "template": "welcome"
    }
    send_email_message(message_payload)

    # channel = get_mq_connection()
    # channel.basic_publish(
    #    exchange='',
    #    routing_key='test_queue',
    #    body=jsonify(message_payload)
    # )
    print("Message sent!")
    return jsonify({"message": "Lost Item added successfully"}), 201

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM public.\"lost_item\" WHERE \"id\" = %s",
        (item_id,)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Lost Item deleted successfully"}), 200

@app.route('/changeStatus/<int:item_id>/<string:status>', methods=['PUT'])
@token_required
def changeStatus(item_id, status):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE public.\"lost_item\" SET \"status\" = %s WHERE \"id\" = %s",
        (status, item_id)
    )
    # cur.execute(
    #     "INSERT INTO public.\"status_history\" (\"old_stat\", \"item_id\") VALUES (%s, %s)",
    #     (status, item_id)
    # )


    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Item status updated successfully"}), 200


# Connect to Elasticsearch running in Docker
es = Elasticsearch(
    "http://localhost:9200",
    headers={"Accept": "application/vnd.elasticsearch+json; compatible-with=8"}
)

@app.route("/item_search", methods=["GET"])
def search_items():
    query_term = request.args.get("q")  # e.g. /search?q=dog
    if not query_term:
        return jsonify({"error": "Missing query parameter 'q'"}), 400

    # Perform a search in lost_items_index
    response = es.search(
        index="lost_items_index",
        q=query_term
    )

    # Extract hits
    hits = [
        {
            "id": hit["_id"],
            "score": hit["_score"],
            "source": hit["_source"]
        }
        for hit in response["hits"]["hits"]
    ]

    return jsonify({"results": hits})
