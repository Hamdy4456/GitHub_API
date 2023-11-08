import requests
import pandas as pd

# Define GitHub API token
token = "copy_your_token"

# Define the URL to fetch public repositories
repos_url = "https://api.github.com/repositories?per_page=50"

# Define the number of repositories to retrieve
num_repos = 100

# Initialize an empty list to store the repository data
repos_data = []

# Send a request to the GitHub API to get the list of repositories
page = 1
while len(repos_data) < num_repos:
    response = requests.get(repos_url, headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 200:
        repos_data.extend(response.json())
        page += 1
    else:
        print(f"Request failed with status code {response.status_code}")
        break

# Initialize lists to store data
names = []
languages_counts = []
contributors_counts = []
stargazers_counts = []
languages_lists = []

# Define functions to get the contributors, languages, and subscribers for a repository
def get_repo_info(repo_url):
    response = requests.get(repo_url, headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 200:
        repo_data = response.json()
        names.append(repo_data.get("name", ""))
        
        # Count contributors
        contributors_url = repo_data.get("contributors_url", "")
        contributors_counts.append(len(requests.get(contributors_url, headers={"Authorization": f"Bearer {token}"}).json()))
        
        # List languages
        languages_url = repo_data.get("languages_url", "")
        languages_data = requests.get(languages_url, headers={"Authorization": f"Bearer {token}"}).json()
        languages_counts.append(len(languages_data))
        
        # Concatenate the languages into a comma-separated string
        languages_list = ", ".join(languages_data.keys())
        languages_lists.append(languages_list)
        
        # Fetch the repository's stargazers
        stargazers_url = repo_data.get("stargazers_url", "")
        stargazers_counts.append(len(requests.get(stargazers_url, headers={"Authorization": f"Bearer {token}"}).json()))
    else:
        names.append("")
        contributors_counts.append(0)
        languages_counts.append(0)
        languages_lists.append("")
        stargazers_counts.append(0)

# Iterate through each repository and fetch additional data
for repo in repos_data:
    repo_url = repo.get("url", "")
    get_repo_info(repo_url)

# Create a Pandas DataFrame
data = {
    "Name": names,
    "Languages Count": languages_counts,
    "Languages": languages_lists,
    "Contributors Count": contributors_counts,
    "stargazers Count": stargazers_counts
}

result_df = pd.DataFrame(data)

# Export data to a csv file
result_df.to_csv('github_repos.csv', index=False)

# Count the occurrences of each language
language_series = result_df['Languages'].str.split(', ').explode()
language_counts = language_series.value_counts()

# Get the three most trending languages and their counts
top_languages = language_counts.head(3)

# Print the results
print("Top 3 trending languages:")
for language, count in top_languages.items():
    print(f"{language}: {count} repos")

# Group the DataFrame by the 'Name' column and count the occurrences
name_counts = result_df['Name'].value_counts()

# Get the top 3 users
top_3_names = name_counts.head(3)

# Print the results
print("\nTop 3 users:")
for name, count in top_3_names.items():
    print(f"{name}: {count} Contributions")
