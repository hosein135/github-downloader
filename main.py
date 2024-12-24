import os
import requests

def download_v_files(repo, api_token, target_directory, download_path):
    """
    Download all .v files from a specific directory of a GitHub repository.

    :param repo: Repository in the format 'owner/repo' (e.g., 'torvalds/linux')
    :param api_token: GitHub API token for authentication
    :param target_directory: Directory in the repo to search for .v files
    :param download_path: Local path to save the downloaded .v files
    """
    # GitHub API URL for the repo contents
    api_url = f"https://api.github.com/repos/{repo}/contents/{target_directory}"
    
    # Headers for authentication
    headers = {"Authorization": f"token {api_token}"}

    # Get the directory contents
    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch directory contents. Status code: {response.status_code}")
        print(f"Error message: {response.json().get('message', 'No message provided')}")
        return

    # Parse the response JSON
    files = response.json()

    # Ensure the download path exists
    os.makedirs(download_path, exist_ok=True)

    # Loop through files and download .v files
    for file in files:
        if file["type"] == "file" and file["name"].endswith(".v"):
            file_url = file["download_url"]
            file_name = file["name"]
            print(f"Downloading {file_name}...")
            file_response = requests.get(file_url)
            if file_response.status_code == 200:
                with open(os.path.join(download_path, file_name), "wb") as f:
                    f.write(file_response.content)
                print(f"Downloaded {file_name} to {download_path}")
            else:
                print(f"Failed to download {file_name}. Status code: {file_response.status_code}")
        else:
            print(f"Skipped {file['name']} (not a .v file)")

if __name__ == "__main__":
    # Input details
    repo = input("Enter the GitHub repository (e.g., 'owner/repo'): ").strip()
    api_token = input("Enter your GitHub API token: ").strip()
    target_directory = input("Enter the directory path in the repo: ").strip()
    download_path = input("Enter the local path to save .v files: ").strip()

    # Download .v files
    download_v_files(repo, api_token, target_directory, download_path)