from typing import List
from botbuilder.schema import ChannelAccount
import openai
from botbuilder.core import ActivityHandler, TurnContext, MessageFactory
import os
from bots.predict import create_chain, get_response_from_query, filterResponse
from bots.prompts import JLLServicesPrompt



chat_history = []

class JLLServicesBot(ActivityHandler):

    async def on_members_added_activity(self, members_added: List[ChannelAccount], turn_context: TurnContext):
        # for member in members_added:
        #     if member.id != turn_context.activity.recipient.id:
        #         await turn_context.send_activity("Hello and welcome to the Demo")
        pass

    async def on_message_activity(self, turn_context: TurnContext):
        user_input = turn_context.activity.text
        if user_input.startswith('/'):
            response = "Received a command, which I'm ignoring."
            return await turn_context.send_activity(response)

        chain = create_chain(namespace= "JLLServices", Prompt= JLLServicesPrompt)
        response = get_response_from_query(user_input, chain, chat_history)
        answer = response['Answer']

        invalid_response = filterResponse(answer)
        if invalid_response == "YES":
            return await turn_context.send_activity(MessageFactory.text(answer))

        sources = response['source']
        links = response['link']

        sources = list(dict.fromkeys(sources))
        links = list(dict.fromkeys(links))

        citations_string = "**Citations:**\n" + "\n".join([f"{i+1}. [{src}]({lnk})" for i, (src, lnk) in enumerate(zip(sources, links))])

        answer_with_citations = f"{answer}\n\n{citations_string}"
        return await turn_context.send_activity(MessageFactory.text(answer_with_citations))

