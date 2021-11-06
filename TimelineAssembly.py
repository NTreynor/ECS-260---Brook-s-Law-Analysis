from pydriller import Repository
from pydriller.metrics.process.code_churn import CodeChurn
from pydriller.metrics.process.commits_count import CommitsCount
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
    testUrl = ["https://github.com/Leaflet/Leaflet", "https://github.com/runelite/runelite"]
    for x in testUrl:
        uniqueAuthors, author_objects = populateAuthors(x)

        # print(len(uniqueAuthors))
        # print(len(author_objects))
        #print(str(author_objects[0]))
        #print(str(author_objects[1]))
        #print(str(author_objects[2]))

        timeline = populateTimeline(author_objects)
        intervals = locatePairedTwoWeekPlusIntervals(timeline)
        # print(len(intervals))
    
        calculate_code_churn(x, intervals)
        calculate_commit_count(x, intervals)

def calculate_code_churn(repo, interval_list):
    # Loops through all significant intervals of development of a given repository and calculators the average code churn per day
    for i in range(0, len(interval_list)): 
        pre_start_date = interval_list[i][0].date
        pre_end_date = interval_list[i][1].date
        post_end_date = interval_list[i][2].date
        
        pre_metric = CodeChurn(path_to_repo=repo, since=pre_start_date, to=pre_end_date)
        pre_churn_total = pre_metric.count()    # Returns the total code churn in range
        
        post_metric = CodeChurn(path_to_repo=repo, since=pre_end_date, to=post_end_date)
        post_churn_total = post_metric.count()
        
        print("Average Code Churn - Interval %d" %(i+1))
        
        values_array = pre_churn_total.values()
        pre_days_difference = abs(pre_start_date - pre_end_date).total_seconds() / 86400.0
        avg_churn = sum(values_array)/pre_days_difference
        print("Average code churn for pre-period", pre_start_date, "to", pre_end_date + ":", avg_churn)
        
        values_array = post_churn_total.values()
        post_days_difference = abs(post_end_date - pre_end_date).total_seconds() / 86400.0
        avg_churn = sum(values_array)/post_days_difference
        print("Average code churn for post-period", pre_end_date, "to", post_end_date + ":", avg_churn)
    
def calculate_commit_count(repo, interval_list):
    for i in range(0, len(interval_list)): 
        pre_start_date = interval_list[i][0].date
        pre_end_date = interval_list[i][1].date
        post_end_date = interval_list[i][2].date
        
        pre_metric = CommitsCount(path_to_repo=repo, since=pre_start_date, to=pre_end_date)
        pre_cc_total = pre_metric.count()    # Returns the total code churn in range
        
        post_metric = CommitsCount(path_to_repo=repo, since=pre_end_date, to=post_end_date)
        post_cc_total = post_metric.count()
        
        print("Average Commit Count - Interval %d" %(i+1))
        
        values_array = pre_cc_total.values()
        pre_days_difference = abs(pre_start_date - pre_end_date).total_seconds() / 86400.0
        avg_cc = sum(values_array)/pre_days_difference
        print("Average commit count for pre-period", pre_start_date, "to", pre_end_date + ":", avg_cc)
        
        values_array = post_cc_total.values()
        post_days_difference = abs(post_end_date - pre_end_date).total_seconds() / 86400.0
        avg_cc = sum(values_array)/post_days_difference
        print("Average commit count for post-period", pre_end_date, "to", post_end_date + ":", avg_cc)
        
    

def locatePairedTwoWeekPlusIntervals(timeline):
    # print("Attempting to locate paired two week intervals")
    significantBreakpoints = []
    for i in range (1, len(timeline)-1):
        timeDiff = timeline[i+1].date - timeline[i].date
        #print("Difference in time: " + str(timeDiff))
        if (timeDiff >= timedelta(days=14)) and (timeline[i].active_devs < timeline[i+1].active_devs) and timeline[i].active_devs >= 5:

            # If this is the case, then we have a 2 week period of stable development, that meet our team size requirements, after the addition of a new team member.

            timeDiffPrev = timeline[i].date - timeline[i-1].date
            if (timeDiffPrev >= timedelta(days=14)) and timeline[i-1].active_devs >= 5:

                # And we can now also confirm that we had a two week stable development period beforehand with which to compare, and can make note of it.
                # print("Significant period of development found surrounding " + str(timeline[i]))
                # print("Stable development from " + (str(timeline[i-1].date)) + " to " + (str(timeline[i].date)))
                # print("and from " + (str(timeline[i].date)) + " to " + (str(timeline[i+1].date)) + "\n")
                significantBreakpoints.append((timeline[i-1], timeline[i], timeline[i+1]))
    return significantBreakpoints

def populateTimeline(author_objects):
    timeline = []
    for x in author_objects:
        if (x.first_commit != x.last_commit):
            firstBreakpoint = TimelineBreakPoint(x.first_commit, 1, 0, x.name)
            secondBreakpoint = TimelineBreakPoint(x.last_commit, 0, 1, x.name)
            # print("Two breakpoints added. " + str(x.first_commit), str(x.last_commit))

            # Sorting?
            timeline.append(firstBreakpoint)
            timeline.append(secondBreakpoint)
        else:
            continue
            # print("First and final commit are the same. No breakpoint to create.")

    new_list = sorted(timeline, key=lambda y: y.date, reverse=False)

    activeDevelopers = 0
    for z in new_list:
        if z.was_first_commit:
            activeDevelopers += 1
            z.active_devs = activeDevelopers
        if z.was_final_commit:
            activeDevelopers -= 1
            z.active_devs = activeDevelopers
        # print(str(z))

    return new_list

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
