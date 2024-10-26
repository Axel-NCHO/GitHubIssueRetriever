# GitHub Issue Retriever

This program retrieves all the issues of a **public** git repository from GitHub.  
This project is compatible with **Python 3.10 or higher**.

### How to run it

1. Clone the repository  
    ```shell
   git clone https://github.com/Axel-NCHO/GitHubIssueRetriever.git
   
2. Install required packages
    ```shell
   pip install -r requirements.txt

3. Run the program
    ```shell
   python main.py
   
The issues are stored in a json file named `issues_<repo_owner>_<repo_name>.json`.

### Rate limit

The GiHub API uses rate limits to avoid DOS attacks. This program can only retrieve issues for  
public repositories as it doesn't use an API key. Therefore, it's limited to **60 requests per hour**.