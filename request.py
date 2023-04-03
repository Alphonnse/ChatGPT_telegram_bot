"""Modules"""
import os
import openai
from dotenv import load_dotenv


class Chat:
    """Conversation class"""

    def __init__(self):
        self.messages = []
        self.conv_name = []

    def get_api(self):
        """To get ChatGPT API"""
        load_dotenv()
        openai.api_key = os.getenv("CHAT_GPT_API")

    def add_system(self):
        """Adding the system to controle ChatGPT"""
        self.messages = [
                {"role": "system",
                 "content": "You’re a kind helpful assistant"}
                ]

    def conversation_name(self, answer):
        """To name the conversation"""
        self.conv_name = [
                {"role": "system",
                 "content": "You’re a kind helpful assistant"}
                ]

        self.conv_name.append(
                {"role": "user",
                 "content": "Придумай название для разговора, начинающегося с этого сообзения. "
                 + answer}
                )

        completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.conv_name
                )

        chat_response = completion.choices[0].message.content
        return chat_response

    def get_answer(self, question):
        """To request the answer"""
        self.messages.append({"role": "user", "content": question})

        completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.messages
                )

        chat_response = completion.choices[0].message.content
        self.messages.append({"role": "assistant", "content": chat_response})
        return chat_response
