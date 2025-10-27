import time
from aiogram import BaseMiddleware,Router, F, types
from aiogram.types import Message
from collections import defaultdict


router = Router()
class AntiFloodMiddleware(BaseMiddleware):

    def __init__(self, delay: float = 2.0):
        self.delay = delay
        self.last_time = defaultdict(lambda: 0)

    async def __call__(self, handler, event: Message, data):
        user_id = event.from_user.id
        current_time = time.time()

        # написал в 12.00 current_time
        # self.last_time[user_id] последнее обращение
        if current_time - self.last_time[user_id] < self.delay:
            await event.answer("Подожди немного")
            return
        else:
            # upd time last call
            self.last_time[user_id] = current_time
            return await handler(event, data)
