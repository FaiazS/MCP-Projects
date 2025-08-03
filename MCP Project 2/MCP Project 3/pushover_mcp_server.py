import os

import requests

from pydantic import BaseModel, Field

from dotenv import load_dotenv

from mcp.server.fastmcp import FastMCP

load_dotenv(override=True)

pushover_user = os.getenv('PUSHOVER_USER')

pushover_token = os.getenv('PUSHOVER_TOKEN')

pushover_url = 'https://api.pushover.net/1/messages.json'

pushover_mcp_server = FastMCP('Pushover MCP Server')

class PushNotification(BaseModel):

    notification_message: str = Field(description= 'A brief update message')


@pushover_mcp_server.tool()
def send_push_notifications(args: PushNotification):

    print(f"Pushing {args.notification_message}")

    payload = {'user': pushover_user, 'token': pushover_token, 'message' : args.notification_message}

    requests.post(url = pushover_url, data = payload)

    print('Notified user successfully.')


if __name__ == '__main__':

    pushover_mcp_server.run(transport= 'stdio')
