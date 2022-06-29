import asyncio
import json
import logging
import random
from time import time
from typing import List

from telethon import events

from service.telegram import TelegramService
from config.constants import Constants
from repository.response import ResponseRepository
from entity.response import Response

WAIT_MIN = 20
WAIT_MAX = 90


async def wait():
    await asyncio.sleep(random.uniform(WAIT_MIN, WAIT_MAX))


class TestService:
    __slots__ = ["response_repository", "telegram_service", "account", "client", "respondent", "await_answers", "manager", "bot", "bot_client"]

    def __init__(self, telegram_service: TelegramService, response_repository: ResponseRepository, account: str, bot: str):
        self.telegram_service = telegram_service
        self.response_repository = response_repository

        self.account = account
        self.bot = bot
        self.client = None
        self.bot_client = None

        self.await_answers = {}
        self.manager = None

    async def advance_scenario(self, awaited_answer, recipient):
        await wait()
        scenario = awaited_answer["scenario"]
        message = scenario[0]
        self.await_answers[recipient] = {
            "name": awaited_answer["name"],
            "message": message,
            "timestamp": time(),
            "scenario": scenario[1:]
        }
        await self.telegram_service.send_message(self.client, recipient, message)

    # async fuckery because fuck python
    async def init_client(self):
        self.client = await self.telegram_service.login(self.account)
        logging.debug(f"API KEY for bot: {self.bot}")
        self.bot_client = await self.telegram_service.login_bot(self.bot)

        @self.client.on(events.NewMessage(incoming=True))
        async def handler(event):
            end = time()
            try:
                recipient = event.message.peer_id.user_id
                if recipient in self.await_answers:
                    awaited_answer = self.await_answers.pop(recipient)
                    scenario = awaited_answer["scenario"]
                    response_time = end - awaited_answer["timestamp"]
                    logging.info(f'Time on response for {awaited_answer["name"]}: {response_time}')
                    self.response_repository.save(Response(None, response_time, awaited_answer["name"]))
                    if response_time > Constants.TEST_TIMEOUT:
                        await wait()
                        await self.telegram_service.send_message(
                            self.bot_client,
                            self.manager,
                            f'''
Время отклика от бота {awaited_answer["name"]}
на сообщение {awaited_answer["message"]}: 
{response_time:.2f} секунд
                            ''')
                    if len(scenario) > 0:
                        await self.advance_scenario(awaited_answer, recipient)
                    else:
                        self.await_answers.pop(recipient)
            except Exception as exc:
                logging.info(exc)

    async def test_bot(self, scenario, name, recipient):
        start = {
            "name": name,
            "message": None,
            "timestamp": time(),
            "scenario": scenario
        }
        await self.advance_scenario(start, recipient.id)

    async def start_cleanup(self):
        for recipient in self.await_answers:
            response_time = time() - self.await_answers[recipient]["timestamp"]
            if response_time > Constants.ERROR_TIMEOUT:
                wait_task = wait()
                self.response_repository.save(Response(None, None, self.await_answers[recipient]["name"]))
                await wait_task
                await self.telegram_service.send_message(
                    self.bot_client,
                    self.manager,
                    f'''
Бот {self.await_answers[recipient]["name"]} не откликнулся 
на сообщение {self.await_answers[recipient]["message"]}: 
за {response_time:.2f} секунд
                    ''')

    async def send_statistics(self):
        statistics = self.response_repository.statistics()
        for bot in statistics:
            await wait()
            await self.telegram_service.send_message(
                self.bot_client,
                self.manager,
                f'''
Статистика по {bot["name"]}:
Среднее время отклика: {bot["average"]:.2f}
Отклонение времени отклика: {bot["deviation"]:.2f}
Всего сделано запросов сегодня: {bot["total"]}
Из них:
<1 секунды отклика: {bot["first_bucket"]}%
от 1 до 2 секунд отклика: {bot["second_bucket"]}%
от 2 до 3 секунд отклика: {bot["third_bucket"]}%
от 3 до 4 секунд отклика: {bot["fourth_bucket"]}%
от 4 до 5 секунд отклика: {bot["fifth_bucket"]}%
>5 секунд отклика: {bot["sixth_bucket"]}%
                ''')




