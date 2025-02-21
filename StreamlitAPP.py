import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.logger import logging
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain

with open("D:\Vscode\HTML\Generative AI\mcqgen\Response.json") as f:
    RESPONSE_JSON = json.load(f)
    
st.title("MCQ Creator Application with LangChai")

with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Choose a file")
    
    mcq_count = number_input("No. of MCQs", min_value=3, max_value=50)
    
    subject = st.text_input("Insert Subject", max_chars=20)
    
    tone = st.text_input("Complexity Level Of Questions", max_chars=20, placeholder="Simple")
    
    button = st.form_submit_button("Create MCQs")
    
    if button and uploaded_file is not None and mcq_count and subject and tone:
           with st.spinner("loading..."):
               try:
                   text=read_file(uploaded_file)
                   with get_openai_callback() as cb:
                       response = generate_evaluate_chain(
                           {
                               "text": text,
                               "number": mcq_count,
                               "subject": subject,
                               "tone": tone,
                               "response_json": RESPONSE_JSON
                           }
                       )
                    
                except Exception as e:
                    traceback.print_exception(type(e), e, e.__traceback__)
                    st.error("Error")
                    
                else:
                    print(f"Total Tokens: {cb.total_tokens}")
                    print(f"Prompt Tokens: {cb.prompt_tokens}")
                    print(f"Completion Tokens: {cb.completion_tokens}")
                    print(f"Total Cost: {cb.total_cost}")
                    if isinstance(response, dict):
                        quiz=response.get("quiz", None)
                        if quiz is not None:
                            table_data = get_table_data(quiz)
                            if table_data is not None:
                                df=pd.DataFrame(table_data)
                                df.index=df.index+1
                                st.table(df)
                                st.text_area(label="Review", value=response["review"])
                            else:
                                st.error("Error in the table data")
                                
                    else:
                        st.write(response)
                