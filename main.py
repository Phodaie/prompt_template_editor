import streamlit as st
import requests
import json
from typing import List, Dict
from pydantic import BaseModel

class Template(BaseModel):
    template_id: str
    content: str



def get_templates()->List[Template]:
    
    response = requests.get("https://9v7s2vz54k.execute-api.us-east-1.amazonaws.com/Prod/templates")

    if response.status_code == 200:
        templates = json.loads(response.content.decode())
        return [Template(**template) for template in templates]
    else:
        return []


def update_templates():
    
    for template in templates:
        response = requests.put(f"https://9v7s2vz54k.execute-api.us-east-1.amazonaws.com/Prod/templates/{template.template_id}",data=json.dumps(template.dict()))
        
        if response.status_code == 200:
            #st.success(f"Template {template.template_id} updated")
            pass
        else:
            st.error(f"Template {template.template_id} failed to update")

templates : List[Template] = []

def main():
    st.subheader("Prompt Template Editor")
    
    global templates
    templates = get_templates()

    for template in templates:

        with st.expander(template.template_id): 
            template.content = st.text_area('', template.content , height=200 , key=template.template_id)
        
    
    st.button("Update",on_click=update_templates)






if __name__ == "__main__":
    main()