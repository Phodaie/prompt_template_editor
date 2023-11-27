import streamlit as st
import requests
import json
from typing import List, Dict, Literal
from pydantic import BaseModel
import streamlit.components.v1 as components

from template_validation import highlight_placeholders_and_macros_with_html


class Template(BaseModel):
    template_id: str
    content: str
    variableNames: List[str] = []
    maxWords: int = 100
    height: int = 300

def get_templates()->List[Template]:
    
    response = requests.get(f"https://lmwznlj2ta.execute-api.us-east-1.amazonaws.com/Prod/templates/{user_name}")
    #response = requests.get(f"http://127.0.0.1:8000/templates/{user_name}")

    if response.status_code == 200:
        templates = json.loads(response.content.decode())
        return [Template(**template) for template in templates]
    else:
        return []


def update_templates():
    
    dictTemplates = [template.model_dump() for template in templates]
    response = requests.put(f"https://lmwznlj2ta.execute-api.us-east-1.amazonaws.com/Prod/templates/{user_name}",data=json.dumps(dictTemplates))
    #response = requests.put(f"http://127.0.0.1:8000/templates/{user_name}",data=json.dumps(dictTemplates))
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n!!!!!!!!!!!!!!!")
    if response.status_code == 200:
        st.success(f"Templates updated")
    else:
        st.error(f"Templates failed to update")

    # for template in templates:
    #     response = requests.put(f"https://lmwznlj2ta.execute-api.us-east-1.amazonaws.com/Prod/templates/{user_name}",data=json.dumps(template.model_dump()))
        
    #     if response.status_code == 200:
    #         #st.success(f"Template {template.template_id} updated")
    #         pass
    #     else:
    #         st.error(f"Template {template.template_id} failed to update")

templates : List[Template] = []
user_name : Literal['User1', 'User2', 'User3' , 'User4' ] = 'User1'

def main():

    st.set_page_config(page_title="Template Editor", page_icon=":pencil2:" , layout="wide")
    
    st.subheader("Simulation Prompt Templates")
    

    global user_name 
    user_name = st.selectbox(
        "Prompt templates for:",
        ("User1", "User2", "User3" , "User4"),
        index=0,
        #placeholder="Select contact method...",
    )
    
    st.write(f"{user_name} templates")

    global templates
    templates = get_templates()

    for template in templates:

        with st.expander(template.template_id): 
            template.content = st.text_area('', template.content , height=template.height , key=template.template_id)

            st.write(', '.join(template.variableNames))

            if st.button('Validate' , key=f'{template.template_id}_va'):
                components.html(highlight_placeholders_and_macros_with_html(template.content,template.variableNames , template.height - 20), height=template.height , scrolling=True)

        
    
    st.button("Update",on_click=update_templates)






if __name__ == "__main__":
    main()