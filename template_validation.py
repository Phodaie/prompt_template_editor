import re

def highlight_placeholders_with_html(input_string, allowed_placeholders):
    
        # Escape HTML tags by replacing < and > with their HTML entities
    input_string = input_string.replace('<', '&lt;').replace('>', '&gt;')

    # Regular expression to find all placeholders and macros
    placeholder_pattern = re.compile(r"\{\{(.+?)\}\}")
    macro_pattern = re.compile(r"(#IF|#ELSEIF|#ELSE|#ENDIF)")
    
    # Find all placeholders and macros in the input string
    extracted_placeholders = placeholder_pattern.findall(input_string)
    macros = macro_pattern.findall(input_string)
    
    # Start the HTML with a div that sets the font-family to Nunito Sans and overflow to auto for scrolling
    html_output = '<div style="font-family: \'Nunito Sans\', sans-serif; overflow: auto; max-height: 500px;">'
    
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
    
    # Append the processed input string to the HTML output
    html_output += input_string.replace('\n', '<br>') + '</div>'
    
    return html_output


