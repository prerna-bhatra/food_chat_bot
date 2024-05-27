# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []



from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import logging  # Import the logging module
import json



class ActionFetchOrders(Action):
    def name(self) -> str:
        return "action_fetch_orders"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        user_message = tracker.latest_message.get('text')

        logging.info("Messsage: %s",user_message)

        logging.info("Tracker: %s", tracker.get_slot('token'))
        json_object = json.loads(user_message)
        logging.info("Tracker: %s", json_object)
        logging.info("token: %s", json_object['token'])

        user_token = 'Bearer'+' '+json_object['token']

        # logging.info("API token: %s", user_token)

        if not user_token:
            dispatcher.utter_message(text="I need a user token to fetch your orders.")
            return []

        headers = {
            'Authorization': user_token
        }
        
        response = requests.get('http://localhost:3005/api/order/history', headers=headers)
        logging.info("API response: %s", response)
        logging.info("API response: %s", response.json())
        # logging.info("API response: %s", response.json())


        if response.status_code == 401:
            dispatcher.utter_message(text="Something is related to token")
            return []

        if response.status_code != 200:
            dispatcher.utter_message(text="Failed to fetch orders.")
            return []

        # json_res = json.loads(response.json())
        # logging.info("API token: %s", json_res)

        orders = response.json()
        logging.info("API token: %s", orders)

        if not orders:
            dispatcher.utter_message(text="No orders found.")
            return []

        # Creating a string with the list of orders
        # orders_list = "\n".join([f"Order ID: {order['id']}, Status: {order['orderStatus']}" for order in orders])
        dispatcher.utter_message(json_message=orders)
        
        return []


class ActionCancelOrder(Action):
    def name(self) -> str:
        return "action_cancel_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        user_message = tracker.latest_message.get('text')
        json_object = json.loads(user_message)
        logging.info("Tracker: %s", json_object)
        logging.info("token: %s", json_object['token'])

        user_token = 'Bearer'+' '+json_object['token']

        order_id = json_object['order_id']

        logging.info("API token: %s", order_id)

        if not order_id:
            dispatcher.utter_message(text="I need a order id  to fetch your order.")
            return []

        if not user_token:
            dispatcher.utter_message(text="I need a user token to fetch your order.")
            return []

        headers = {
            'Authorization': user_token
        }
        
        response = requests.get(f'http://localhost:3005/api/order/cancel/{order_id}', headers=headers)
        # logging.info("API response: %s", response)
        # logging.info("API response: %s", response.json())
        # logging.info("API response: %s", response.json())

        if response.status_code == 401:
            dispatcher.utter_message(text="Something is related to token")
            return []

        if response.status_code == 400:
            dispatcher.utter_message(text="Order is cancelled already")
            return []

        if response.status_code != 200:
            dispatcher.utter_message(text="Failed to cancel orders")
            return []
        
        dispatcher.utter_message(text="order cancelled sucessfully")
        
        return []
