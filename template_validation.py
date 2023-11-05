import re
import json


# Updated function to preserve newlines in the HTML output
def highlight_placeholders_and_macros_with_html(input_string, allowed_placeholders , height=300):
    # Step 1: Escape all < and > in the input to prevent HTML injection
    input_string = input_string.replace('<', '&lt;').replace('>', '&gt;')

    # Step 2: Identify and temporarily remove JSON blocks, storing them for later
    json_blocks = []
    def extract_json_block(match):
        json_blocks.append(match.group(1))  # Store the JSON block
        return f"__JSON_BLOCK_{len(json_blocks) - 1}__"  # Return a placeholder

    # Use regex to find JSON blocks and replace them with placeholders
    input_string = re.sub(r"```json(.+?)```", extract_json_block, input_string, flags=re.DOTALL)

    # Step 3: Identify placeholders and macros
    placeholder_pattern = re.compile(r"\{\{(.+?)\}\}")
    macro_pattern = re.compile(r"(#IF|#ELSEIF|#ELSE|#ENDIF)")

    # Extract placeholders and macros from the input
    extracted_placeholders = placeholder_pattern.findall(input_string)
    macros = macro_pattern.findall(input_string)

    # Step 4: Highlight macros and placeholders
    # Highlight macros in purple
    for macro in set(macros):
        input_string = input_string.replace(macro, f'<span style="color: purple;">{macro}</span>')

    # Highlight placeholders depending on whether they are allowed or not
    for placeholder in set(extracted_placeholders):
        placeholder_tag = f"{{{{{placeholder}}}}}"
        if placeholder_tag in allowed_placeholders:
            # Allowed placeholders are highlighted in green
            input_string = input_string.replace(placeholder_tag, f'<span style="color: green;">{placeholder_tag}</span>')
        else:
            # Unallowed placeholders are highlighted in red
            input_string = input_string.replace(placeholder_tag, f'<span style="color: red;">{placeholder_tag}</span>')

    # Step 5: Validate and reinsert JSON blocks, now highlighted
    for i, json_block in enumerate(json_blocks):
        # Try to parse the JSON block to check if it's well-formed
        try:
            # Remove comments and reformat
            json_block_no_comments = re.sub(r'//.*', '', json_block)
            parsed_json = json.loads(json_block_no_comments)
            formatted_json = json.dumps(parsed_json, indent=4)
            json_formatted = f'<pre style="background-color: #f6f8fa;"><code>{formatted_json}</code></pre>'
        except json.JSONDecodeError as e:
            # JSON is invalid; highlight the error inline in red
            json_error_line = e.lineno
            json_error_col = e.colno
            json_lines = json_block.splitlines()
            json_lines[json_error_line - 1] = re.sub(
                r"^(.{" + str(json_error_col - 1) + r"})(.)", 
                r'\1<span style="color: red; font-weight: bold;">\2</span>',
                json_lines[json_error_line - 1]
            )
            highlighted_json = "\n".join(json_lines)
            json_formatted = f'<pre style="background-color: #f6f8fa;"><code>{highlighted_json}</code></pre>'
        input_string = input_string.replace(f"__JSON_BLOCK_{i}__", json_formatted)

    # Step 6: Wrap the result in a div with scrollable content, Nunito Sans font, and preserve whitespace and newlines
    html_output = f'<div style="font-family: \'Nunito Sans\', sans-serif; overflow: auto; max-height: {height}px; white-space: pre-wrap;">{input_string}</div>'
    
    return html_output

