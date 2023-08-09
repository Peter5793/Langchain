import os 
from langchain import OpenAI
from langchain.agents import create_pandas_dataframe_agent
import pandas as pd
from apikey import api_key

# Setting up the api key
#import environ 
#
#env = environ.Env()
#environ.Env.read_env()
#
#API_KEY = env("api_key")


def create_agent(filename: str):
    """
         create an agent that can access a large langauge model

         args:
            filename with the path to the cdv with the data
         return :
            an agent that can access and use the LLM
    """
    #create an OpenaAI object
    llm = OpenAI(openai_api_key=api_key)

    # read the csv file into a pandas dataframe
    df = pd.read_csv(filename)

    # create a pandas dataframe agent
    return create_pandas_dataframe_agent(llm, df, verbose= True)

def query_agent(agent, query):
    """
    query an agent and return the response as a string

    args:
         agent: the agent to query
         query: the query to ask the agent
    returns:
        the response from the agent as a string
    """
    prompt = (
        """
            For the following query, if it requires drawing a table, reply as follows:
            {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...]}}

            If the query requires creating a bar chart, reply as follows:
            {"bar": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

            If the query requires creating a line chart, reply as follows:
            {"line": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

            There can only be two types of chart, "bar" and "line".

            If it is just asking a question that requires neither, reply as follows:
            {"answer": "answer"}
            Example:
            {"answer": "The title with the highest rating is 'Gilead'"}

            If you do not know the answer, reply as follows:
            {"answer": "I do not know."}

            Return all output as a string.

            All strings in "columns" list and data list, should be in double quotes,

            For example: {"columns": ["title", "ratings_count"], "data": [["Gilead", 361], ["Spider's Web", 5164]]}

            Lets think step by step.

            Below is the query.
            Query: 
            """
        + query
    )

    response = agent.run(prompt)

    #convert the reponse to a string
    return response.__str__()