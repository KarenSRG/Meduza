import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from apps.producers import routers as producer_router

from fastapi.middleware.cors import CORSMiddleware
from src.bot.api_actions import run_monitoring_bot
from src.bot.main import run_controller_bot


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pre-App-Start events #

    async with asyncio.TaskGroup() as group:
        group.create_task(run_controller_bot())
        group.create_task(run_monitoring_bot())

    # Pre-App-Start events #
    yield


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(producer_router.router, tags=["User"])

uvicorn.run(app, host="localhost")
