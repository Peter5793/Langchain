import streamlit as st
import pandas as pd
import json

from trial import query_agent, create_agent

def decode_response(response: str) -> dict:
    """
     converts the string reponse from the model to dictionary obejct
    Agrs:
        reponse (str): response from the model
    Returns:
    dict: dictionary with reponse data
    """
    return json.loads(response)

def write_response(response_dict: dict):
    """
    write a reposne from an agent to a streamlit app

    args:
        response_dict : the reposne from the agent
    
        Returns:
            None
    """
    if "answer" in response_dict:
        st.write(response_dict["answer"])
    
    #check if the response is a bar chart
    if "bar" in response_dict:
        data = response_dict["bar"]
        df = pd.DataFrame(data)
        df.set_index("columns",inplace = True)
        st.bar_chart(df)
    # check if the response is a line chart

    if "line" in response_dict:
        data = response_dict["line"]
        df = pd.DataFrame(data)
        df.set_index("columns", inplace=True)
        st.line_chart(df)
    #check if the response is a table
    if "table" in response_dict:
        data = response_dict["table"]
        df = pd.DataFrame(data["data"], columns= data["columns"])
        st.table(df)

    # interface for the app
    
st.title("Make sense of Data")

st.write("Please upload your CSV file below")
data = st.file_uploader("Upload a CSV")
query = st.text_area("Insert your query")

if st.button("Submit Query", type = "primary"):
    # create an agent from the CSV file
    agent = create_agent(data)

    # query the agent
    response = query_agent(agent= agent, query= query)

    # decode the response
    decoded_response  = decode_response(response)

    #write the response  to the streamlit app
    write_response(decoded_response)




