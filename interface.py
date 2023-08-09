import streamlit as st
import pandas as pd
import json

from trial import query_agent, create_agent

def decode_response(response: str) -> dict:
    """
    Converts the string response from the model to a dictionary object.
    Args:
        response (str): Response from the model.
    Returns:
        dict: Dictionary with response data.
    """
    try:
        parsed_response = json.loads(response)
        return parsed_response
    except json.JSONDecodeError:
        # Handle the case where response contains both final answer and action request
        response_dict = {"answer": None, "action": None}
        
        # Split the response into the final answer and action parts
        parts = response.split("Action:")
        
        for part in parts:
            if "Final Answer:" in part:
                response_dict["answer"] = part.strip().replace("Final Answer:", "").strip()
            elif "python_repl_ast" in part:
                # Extract the action input (which is in JSON format)
                action_input = part.split("Action Input:")[1].strip().replace("'", "\"")
                response_dict["action"] = json.loads(action_input.replace("'", "\""))  # Replace single quotes in action_input
                
        return response_dict  
   
    

def write_response(response_dict: dict):
    """
    write a reposne from an agent to a streamlit app

    args:
        response_dict : the reposne from the agent
    
        Retruns:
            None
    """
    if "answer" in response_dict:
        st.write(response_dict["answer"])
    
    #check if the response is a bar chart
    if "bar" in response_dict:
        data = response_dict["bar"]
        #initialize a dictionary to build dataframe
        try:
            df_data = {
                col:[x[i] if isinstance (x, list) else x for x in data ['data']]
                for i, col in enumerate(data['columns'])
            }
            df = pd.DataFrame(data)
            df.set_index("columns",inplace = True)
            st.bar_chart(df)
        except ValueError:
            print(f"Could not create dataframe. {data}")
    # check if the response is a line chart

    if "line" in response_dict:
        data = response_dict["line"]
        try:
            df_data = {
                col:[x[i] if isinstance (x, list) else x for x in data ['data']]
                for i, col in enumerate(data['columns'])
            }
            df = pd.DataFrame(data)
            df.set_index("columns",inplace = True)
            st.line_chart(df)
        except ValueError:
            print(f"Could not create dataframe. {data}")

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
    print("response string:", response)


    # decode the response
    decoded_response  = decode_response(response)

    try:
        decoded_response = decode_response(response)
        print("Decoded Response:", decoded_response)  # Debugging print statement
    except json.JSONDecodeError as e:
        print("JSON Decoding Error:", e)
        print("Problematic Response:", response)

    #write the response  to the streamlit app
    write_response(decoded_response)
