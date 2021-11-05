from pydriller import Repository
from pydriller.metrics.process.code_churn import CodeChurn
from datetime import datetime, timedelta

# Thought process: For a given github repo, our first task is to assemble a list of authors, and their start and end dates of active contribution.
# For now, we will define this as the period of time between their first and their final commit in a given repo. Once we have this data, we assemble a timeline
# by filling an array with the start and end dates of every author in a project (and information allowing for the retrieval of the author's id associated with said
# start or end date. A second array will consist of start and end dates, and the number of active developers present at the start of a given date.

def main():
    testUrl = ["https://github.com/Leaflet/Leaflet"]
    uniqueAuthors = populateAuthors(testUrl)

    return uniqueAuthors

def populateAuthors(repoUrl):
    repo_authors = []
    for commit in Repository(path_to_repo=repoUrl).traverse_commits():
        current_author = commit.author.name
        if current_author in repo_authors:
            continue
        else:
            repo_authors.append(current_author)
            print("New Author Found: " + current_author )
    return repo_authors

# def findFirstCommit(author, repoUrl):

    # TODO: Find date of first commit from author

# def findLastCommit(author, repoUrl):

    # TODO: Find date of last commit from author

main()

