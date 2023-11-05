import streamlit as st
import requests
import json
from typing import List, Dict, Literal
from pydantic import BaseModel
import streamlit.components.v1 as components

from template_validation import highlight_placeholders_with_html


class Template(BaseModel):
    template_id: str
    content: str
    variableNames: List[str] = []
    maxWords: int = 100
    height: int = 300

def get_templates()->List[Template]:
    
    response = requests.get(f"https://lmwznlj2ta.execute-api.us-east-1.amazonaws.com/Prod/templates/{user_name}")

    if response.status_code == 200:
        templates = json.loads(response.content.decode())
        return [Template(**template) for template in templates]
    else:
        return []


def update_templates():
    
    for template in templates:
        response = requests.put(f"https://lmwznlj2ta.execute-api.us-east-1.amazonaws.com/Prod/templates/{user_name}",data=json.dumps(template.dict()))
        
        if response.status_code == 200:
            #st.success(f"Template {template.template_id} updated")
            pass
        else:
            st.error(f"Template {template.template_id} failed to update")

templates : List[Template] = []
user_name : Literal['User1', 'User2', 'User'] = 'User1'

def main():
    st.subheader("Prompt Template Editor")
    

    global user_name 
    user_name = st.selectbox(
        "Prompt templates for:",
        ("User1", "User2", "User3"),
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
                components.html(highlight_placeholders_with_html(template.content,template.variableNames), height=500)

        
    
    st.button("Update",on_click=update_templates)






if __name__ == "__main__":
    main()