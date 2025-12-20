def read_template(data: list) -> str:
    if not data:
        return "No records were found."

    return f"I found {len(data)} records matching your request."

def create_template() -> str:
    return "The record has been created successfully."

def update_template() -> str:
    return "The record has been updated successfully."

def delete_template() -> str:
    return "The record has been deleted successfully."

def install_template(module_name: str) -> str:
    return f"The module '{module_name}' has been installed successfully."
