
from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
     classroom = State()
     
     
class ReportMessage(StatesGroup):
     report = State()
     
     
class MessageSender(StatesGroup):
     message_send = State()
     
     
class MsgUser(StatesGroup):
     id_ = State()
     msg_one_user = State()
     