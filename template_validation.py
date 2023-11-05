import re



def highlight_placeholders_with_html(input_string, allowed_placeholders):
    # Regular expression to find JSON blocks
    json_pattern = re.compile(r"```json(.+?)```", re.DOTALL)
    
    # Find all JSON blocks in the input string
    json_blocks = json_pattern.findall(input_string)
    
    # Escape HTML within JSON blocks and replace them with a placeholder in the input_string
    for i, json_block in enumerate(json_blocks):
        escaped_json = json_block.replace('<', '&lt;').replace('>', '&gt;').replace('&', '&amp;')
        placeholder = f"__JSON_BLOCK_{i}__"
        input_string = input_string.replace(f"```json{json_block}```", placeholder)
    
    # Escape HTML tags by replacing < and > with their HTML entities
    input_string = input_string.replace('<', '&lt;').replace('>', '&gt;')

    # Regular expression to find all placeholders and macros
    placeholder_pattern = re.compile(r"\{\{(.+?)\}\}")
    macro_pattern = re.compile(r"(#IF|#ELSEIF|#ELSE|#ENDIF)")
    
    # Find all placeholders and macros in the input string
    extracted_placeholders = placeholder_pattern.findall(input_string)
    macros = macro_pattern.findall(input_string)
    
    # Start the HTML with a div that sets the font-family to Nunito Sans and overflow to auto for scrolling
    html_output = '<div style="font-family: \'Nunito Sans\', sans-serif; overflow: auto; max-height: 200px;">'
    
    # Highlight macros with HTML span tags in purple
    for macro in set(macros):
        input_string = input_string.replace(macro, f'<span style="color: purple;">{macro}</span>')
    
    # Format extracted placeholders to match the allowed format
    formatted_placeholders = [f"{{{{{placeholder}}}}}" for placeholder in extracted_placeholders]
    
    # Highlight placeholders with HTML span tags
    for placeholder in formatted_placeholders:
        if placeholder in allowed_placeholders:
            # Allowed placeholders are highlighted in green
            input_string = input_string.replace(placeholder, f'<span style="color: green;">{placeholder}</span>')
        else:
            # Unallowed placeholders are highlighted in red
            input_string = input_string.replace(placeholder, f'<span style="color: red;">{placeholder}</span>')
    
    # Replace placeholders with formatted JSON blocks
    for i, json_block in enumerate(json_blocks):
        placeholder = f"__JSON_BLOCK_{i}__"
        formatted_json = f'<pre style="background-color: #f6f8fa;"><code>{json_block.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")}</code></pre>'
        input_string = input_string.replace(placeholder, formatted_json)
    
    # Append the processed input string to the HTML output
    html_output += input_string.replace('\n', '<br>') + '</div>'
    
    return html_output


