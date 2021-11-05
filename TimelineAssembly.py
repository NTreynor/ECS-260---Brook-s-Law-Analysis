from pydriller import Repository
from pydriller.metrics.process.code_churn import CodeChurn
from datetime import datetime, timedelta


# Thought process: For a given github repo, our first task is to assemble a list of authors, and their start and end dates of active contribution.
# For now, we will define this as the period of time between their first and their final commit in a given repo. Once we have this data, we assemble a timeline
# by filling an array with the start and end dates of every author in a project (and information allowing for the retrieval of the author's id associated with said
# start or end date. A second array will consist of start and end dates, and the number of active developers present at the start of a given date.

class Author:
    def __init__(self, id, first_commit, last_commit):
        self.name = id
        self.first_commit = first_commit
        self.last_commit = last_commit

    def update_last_commit(self, new_last_commit):
        self.last_commit = new_last_commit

    def __str__(self):
        return "Author name is %s. Date of first commit is %s. Date of final commit is %s." % (self.name, str(self.first_commit), str(self.last_commit))


def main():
    testUrl = ["https://github.com/Leaflet/Leaflet"]
    uniqueAuthors, author_objects = populateAuthors(testUrl)

    print(len(uniqueAuthors))
    print(len(author_objects))
    print(str(author_objects[0]))
    print(str(author_objects[1])) # TODO: FIX BUG -- Subsequent author objects are NOT having their final commit date updated appropriately.
    print(str(author_objects[2])) # Actively investigating.
    return uniqueAuthors


def populateAuthors(repoUrl):
    repo_authors = []
    repo_author_objects = []
    for commit in Repository(path_to_repo=repoUrl).traverse_commits():
        current_author = commit.author.name
        if current_author in repo_authors: # A more recent commit by this author has been found
            print("Repeat commit by " + current_author)
            for x in repo_author_objects:
                if x.name == current_author: # so we find the appropriate author object
                    x.last_commit = commit.author_date # And update it's date.
                    print("New commit by " + current_author + "Appropriately updated")
                break
            continue
        else: # This is the first instance this author has been detected. Instantiate a new author object.
            repo_authors.append(current_author)
            new_author = Author(current_author, commit.author_date, commit.author_date)
            repo_author_objects.append(new_author)
            print("New Author Found: " + current_author)
    return repo_authors, repo_author_objects

# There should be a method to update this such that we can perform all updates in one pass to improve time complexity, I beleive.

# Perhaps unneeded function definitions below:
# def findFirstCommit(author, repoUrl):
# def findLastCommit(author, repoUrl):

main()
