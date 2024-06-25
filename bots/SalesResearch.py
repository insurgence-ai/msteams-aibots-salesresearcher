from typing import List
from botbuilder.schema import ChannelAccount
import openai
from botbuilder.core import ActivityHandler, TurnContext, MessageFactory
import os
from .sales_research_bot import SalesResearchBot
import regex as re


chat_history = []

class SalesResearchBot(ActivityHandler):

    async def on_members_added_activity(self, members_added: List[ChannelAccount], turn_context: TurnContext):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome to the Demo")
        pass

    async def on_message_activity(self, turn_context: TurnContext):
        user_input = turn_context.activity.text
        if user_input.startswith('/'):
            response = "Received a command, which I'm ignoring."
            return await turn_context.send_activity(response)
        # Define a regular expression pattern to match URLs
        url_pattern = r'http?://\S+|www\.\S+'
        salesbot = SalesResearchBot()
        # Get the text of the received message
        message_text = turn_context.activity.text

        # Check if the message contains a URL
        if re.search(url_pattern, message_text):
            await turn_context.send_activity(
            MessageFactory.text(f"Researching request: {message_text}. Meanwhile, sip your coffee ☕ and let me handle the work 💼."))
            # If a URL is found, call the agent and send response
            try:
                response_text = salesbot.run_agent(message_text)
                print("Got the output")
                response = MessageFactory.text(response_text)
            except Exception as e:
                response = MessageFactory.text(f"Error: {e}")
        else:
            # If no URL is found, send a different response
            response = MessageFactory.text(f"Hi, I am a sales research bot created by Nazim at insurgence.ai.\n\nType a URL to get started.")

        await turn_context.send_activity(response)
