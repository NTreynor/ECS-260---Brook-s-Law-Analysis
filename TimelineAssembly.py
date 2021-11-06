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

class TimelineBreakPoint:
    def __init__(self, date, was_first_commit, was_final_commit, authorEmail):
        self.date = date
        self.was_first_commit = was_first_commit
        self.was_final_commit = was_final_commit
        self.authorEmail = authorEmail
        self.active_devs = 0

    def __str__(self):
        return "Breakpoint on %s. First commit: %s. Final commit: %s. Active devs from this point on: %s. Author was %s." % (str(self.date), self.was_first_commit, self.was_final_commit, self.active_devs, self.authorEmail)


def main():
    testUrl = ["https://github.com/Leaflet/Leaflet"]
    uniqueAuthors, author_objects = populateAuthors(testUrl)

    print(len(uniqueAuthors))
    print(len(author_objects))
    #print(str(author_objects[0]))
    #print(str(author_objects[1]))
    #print(str(author_objects[2]))

    populateTimeline(author_objects)
    return uniqueAuthors



def populateTimeline(author_objects):
    timeline = []
    for x in author_objects:
        if (x.first_commit != x.last_commit):
            firstBreakpoint = TimelineBreakPoint(x.first_commit, 1, 0, x.name)
            secondBreakpoint = TimelineBreakPoint(x.last_commit, 0, 1, x.name)
            print("Two breakpoints added. " + str(x.first_commit), str(x.last_commit))

            # Sorting?
            timeline.append(firstBreakpoint)
            timeline.append(secondBreakpoint)
        else:
            print("First and final commit are the same. No breakpoint to create.")

    new_list = sorted(timeline, key=lambda y: y.date, reverse=False)

    activeDevelopers = 0
    for z in new_list:
        if z.was_first_commit:
            activeDevelopers += 1
            z.active_devs = activeDevelopers
        if z.was_final_commit:
            activeDevelopers -= 1
            z.active_devs = activeDevelopers
        print(str(z))






def populateAuthors(repoUrl):
    repo_authors = []
    repo_author_objects = []
    for commit in Repository(path_to_repo=repoUrl).traverse_commits():
        current_author = commit.committer.email
        if current_author in repo_authors: # A more recent commit by this author has been found
            #print("Repeat commit by " + current_author)
            for x in repo_author_objects:
                if x.name == current_author: # so we find the appropriate author object
                    x.last_commit = commit.committer_date # And update it's date.
                    #print("New commit by " + current_author + " appropriately updated")
                    break
            continue
        else: # This is the first instance this author has been detected. Instantiate a new author object.
            repo_authors.append(current_author)
            new_author = Author(current_author, commit.committer_date, commit.committer_date)
            repo_author_objects.append(new_author)
            #print("New Author Found: " + current_author)
    return repo_authors, repo_author_objects

# There should be a method to update this such that we can perform all updates in one pass to improve time complexity, I beleive.

# Perhaps unneeded function definitions below:
# def findFirstCommit(author, repoUrl):
# def findLastCommit(author, repoUrl):

main()
