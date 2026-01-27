# _*_ encoding: utf-8 _*_

def read_markdown_file(file_path):
    """
    Reads the content of a Markdown file and returns it as a string.
    """
    try:
        # Open the file in read mode ('r') with UTF-8 encoding
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"Error: The file '{file_path}' was not found."
    except Exception as e:
        return f"An error occurred: {e}"