import numpy as np
import re
import math
import openai
from openai import OpenAI


class Interface:
    def __init__(self):
        self.key = ""
        with open("apikey.txt") as f:
            self.key = f.readline()
        print(self.key)
        self.client = OpenAI(api_key=self.key)

    def send_request(self):
        pass