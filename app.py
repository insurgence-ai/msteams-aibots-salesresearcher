import sys, traceback
from http import HTTPStatus
from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.core import TurnContext
from botbuilder.integration.aiohttp import CloudAdapter, ConfigurationBotFrameworkAuthentication
from botbuilder.schema import Activity
from bots.MAServices import MAServicesBot
from bots.Tendered import TenderedBot
from bots.JLLServices import JLLServicesBot
from bots.ServiceFm import ServiceFMBot
from bots.Insurgence import InsurgenceBot
from bots.SalesResearch import SalesResearchBot
from bots.Downer import DownerBot
from config import (MASERVICES_BOT_CONFIG, TENDERED_BOT_CONFIG, JLLSERVICES_BOT_CONFIG, 
    SERVICEFM_BOT_CONFIG, DOWNER_BOT_CONFIG, INSURGENCE_BOT_CONFIG, SALESRESEARCH_BOT_CONFIG)
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

MASERVICES_APAPTER = CloudAdapter(ConfigurationBotFrameworkAuthentication(MASERVICES_BOT_CONFIG))
TENDERED_APAPTER = CloudAdapter(ConfigurationBotFrameworkAuthentication(TENDERED_BOT_CONFIG))
JLLSERVICES_APAPTER = CloudAdapter(ConfigurationBotFrameworkAuthentication(JLLSERVICES_BOT_CONFIG))
SERVICEFM_APAPTER = CloudAdapter(ConfigurationBotFrameworkAuthentication(SERVICEFM_BOT_CONFIG))
DOWNER_APAPTER = CloudAdapter(ConfigurationBotFrameworkAuthentication(DOWNER_BOT_CONFIG))
INSURGENCE_APAPTER = CloudAdapter(ConfigurationBotFrameworkAuthentication(INSURGENCE_BOT_CONFIG))
SALESRESEARCH_ADAPTER = CloudAdapter(ConfigurationBotFrameworkAuthentication(SALESRESEARCH_BOT_CONFIG))

async def on_error(context: TurnContext, error: Exception):
    print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)

    # Log additional details about the error
    print(f"Error type: {type(error).__name__}", file=sys.stderr)
    print(f"Error args: {error.args}", file=sys.stderr)
    
    # Log information about the current turn context
    print(f"Activity type: {context.activity.type}", file=sys.stderr)
    print(f"Conversation ID: {context.activity.conversation.id}", file=sys.stderr)
    print(f"From ID: {context.activity.from_property.id}", file=sys.stderr)

    traceback.print_exc()

    await context.send_activity("The bot encountered an error or bug. Please contact the insurgence support team to resolve this.")
    

MASERVICES_APAPTER.on_turn_error = on_error
TENDERED_APAPTER.on_turn_error = on_error
JLLSERVICES_APAPTER.on_turn_error = on_error
SERVICEFM_APAPTER.on_turn_error = on_error
DOWNER_APAPTER.on_turn_error = on_error
INSURGENCE_APAPTER.on_turn_error = on_error
SALESRESEARCH_ADAPTER.on_turn_error = on_error
MASERVICES_BOT = MAServicesBot()
TENDERED_BOT = TenderedBot()
JLLSERVICES_BOT = JLLServicesBot()
SERVICEFM_BOT = ServiceFMBot()
DOWNER_BOT = DownerBot()
INSURGENCE_BOT = InsurgenceBot()
SALESRESEARCH_BOT = SalesResearchBot()

async def messageMAServices(req: Request) -> Response:
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    response = await MASERVICES_APAPTER.process_activity(auth_header, activity, MASERVICES_BOT.on_turn)
    if response:
        return json_response(data=response.body, status=response.status)
    return Response(status=HTTPStatus.OK)


async def messageTendered(req: Request) -> Response:
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    response = await TENDERED_APAPTER.process_activity(auth_header, activity, TENDERED_BOT.on_turn)
    if response:
        return json_response(data=response.body, status=response.status)
    return Response(status=HTTPStatus.OK)


async def messageJLLServices(req: Request) -> Response:
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    response = await JLLSERVICES_APAPTER.process_activity(auth_header, activity, JLLSERVICES_BOT.on_turn)
    if response:
        return json_response(data=response.body, status=response.status)
    return Response(status=HTTPStatus.OK)


async def messageServiceFMBot(req: Request) -> Response:
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    response = await SERVICEFM_APAPTER.process_activity(auth_header, activity, SERVICEFM_BOT.on_turn)
    if response:
        return json_response(data=response.body, status=response.status)
    return Response(status=HTTPStatus.OK)

async def messageDownerBot(req: Request) -> Response:
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    response = await DOWNER_APAPTER.process_activity(auth_header, activity, DOWNER_BOT.on_turn)
    if response:
        return json_response(data=response.body, status=response.status)
    return Response(status=HTTPStatus.OK)

async def messageInsurgenceBot(req: Request) -> Response:
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    response = await INSURGENCE_APAPTER.process_activity(auth_header, activity, INSURGENCE_BOT.on_turn)
    if response:
        return json_response(data=response.body, status=response.status)
    return Response(status=HTTPStatus.OK)

async def messageSalesResearchBot(req: Request) -> Response:
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    response = await SALESRESEARCH_ADAPTER.process_activity(auth_header, activity, 
                                                            SALESRESEARCH_BOT.on_turn)
    if response:
        return json_response(data=response.body, status=response.status)
    return Response(status=HTTPStatus.OK)

def init_func(argv):
    APP = web.Application()
    APP.router.add_post("/api/messages/maservices", messageMAServices)
    APP.router.add_post("/api/messages/tendered", messageTendered)
    APP.router.add_post("/api/messages/jllservices", messageJLLServices)
    APP.router.add_post("/api/messages/service-fm", messageServiceFMBot)
    APP.router.add_post("/api/messages/downer", messageDownerBot)
    APP.router.add_post("/api/messages/insurgence", messageInsurgenceBot)
    APP.router.add_post("/api/messages/sales-research", messageSalesResearchBot)
    return APP


if __name__ == "__main__":
    APP = init_func(None)
    try:
        web.run_app(APP, host="0.0.0.0", port=8000)
    except Exception as error:
        raise error