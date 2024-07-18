import os
from github import Github
import base64

# Initialize GitHub client
g = Github(os.environ['UPDATE_GITHUB_ACTION_TOKEN'])

# Get the target repository
target_repo = g.get_repo(os.environ['WEBSITE_REPO'])

# Specify the path to assets_data.js
file_path = os.environ['ASSETS_DATA_FILE_PATH']

# Get the base URL for assets
base_url = os.environ['BASE_URL']

# Get the current content of assets_data.js
github_file = target_repo.get_contents(file_path)
current_content = base64.b64decode(github_file.content).decode('utf-8')

# Function to get all files in a directory
def get_files(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            # This will keep the full file name including extension
            file_list.append(os.path.join(root, file).replace('\\', '/').replace(f"{directory}/", ""))
    return file_list

# Get all directories in the base repository
directories = [d for d in os.listdir() if os.path.isdir(d) and not d.startswith('.')]

# Generate new content
new_content = "// This file is auto-generated. Do not edit manually.\n\n"
for directory in directories:
    files = get_files(directory)
    if files:  # Only create array if folder is not empty
        new_content += f"export const {directory} = [\n"
        for file in files:
            new_content += f'  "{base_url}/{directory}/{file}",\n'
        new_content += "];\n\n"

# Update the file if content has changed
if new_content != current_content:
    target_repo.update_file(
        file_path,
        "Updated assets_data.js file with latest list assets",
        new_content,
        github_file.sha
    )
    print(f"{file_path} updated successfully")
else:
    print(f"No changes needed in {file_path}")