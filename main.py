import asyncio
import logging
import json
import random
from time import time
import asyncio
from datetime import datetime
from pytz import timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from prometheus_client import start_http_server, Summary

from config.constants import Constants
from factory.service import ServiceFactory

logging.basicConfig(
    filename="tests.log",
    format='%(asctime)s:%(levelname)s:%(message)s',
    encoding='utf-8',
    level=logging.INFO
)


async def shedule():
    test = ServiceFactory.get().test
    await test.init_client()
    run = test.client.run_until_disconnected()
    logging.debug("Preparing scheduling job")
    scheduler = AsyncIOScheduler()
    logging.debug("Starting schedule")
    interval = IntervalTrigger(minutes=5)
    cron_stat = CronTrigger(hour=21, timezone=timezone("Europe/Samara"))
    with open("resources/scenarios.json", "rb") as f:
        data = json.load(f)
        test.manager = await test.bot_client.get_entity(data["manager"])
        logging.info(f"Manager chat id :{test.manager.id}")
        for entry in data["scenarios"]:
            recipient = await test.client.get_entity(entry["recipient"])
            scheduler.add_job(
                test.test_bot,
                interval,
                next_run_time=datetime.now(),
                args=(entry["scenario"], entry["recipient"], recipient)
            )
    scheduler.add_job(test.start_cleanup, interval)
    scheduler.add_job(test.send_statistics, cron_stat)
    scheduler.start()
    await run


async def main():
    start_http_server(8080)
    await shedule()


if __name__ == "__main__":
    asyncio.run(main())
