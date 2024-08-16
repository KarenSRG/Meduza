from src.apps.chats.dao import ChatDAO
from src.apps.consumers.dao import ConsumerDAO
from src.apps.messages.dao import MessageDAO
from src.apps.producers.dao import ProducerDAO


class MainDAO:
    message = MessageDAO()
    producer = ProducerDAO()
    consumer = ConsumerDAO()
    chat = ChatDAO()


dao = MainDAO()
