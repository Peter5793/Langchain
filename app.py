from apikey import api_key
import os
from langchain.prompts import PromptTemplate

os.environ['OPENAI_API_KEY'] = api_key

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
llm = OpenAI(temperature=0.9)

chat = ChatOpenAI(temperature=0)
text = chat.predict('translate this sentence from English to Swahili. I love programming')

prompt = PromptTemplate.from_template('what is a good name for a {product} factory')
prompt.format(product = "colorful socks")
#link the prompts using chain
chain = LLMChain(llm=llm, prompt=prompt)
print(chain.run('colorful socks'))
