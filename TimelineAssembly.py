from pydriller import Repository
from pydriller.metrics.process.code_churn import CodeChurn
from pydriller.metrics.process.commits_count import CommitsCount
from datetime import datetime, timedelta
import pandas as pd


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


# urls = ["https://github.com/runelite/runelite"]
# urls = ["https://github.com/cosmos/cosmos-sdk"]
# urls = ["https://github.com/deepmind/alphafold"]
# urls = ["https://github.com/MangoDB-io/MangoDB"]
# urls = ["https://github.com/bcrypt-ruby/bcrypt-ruby"]
# urls = ["https://github.com/zeroclipboard/zeroclipboard"]
# urls = ["https://github.com/github/resque"]
# urls = ["https://github.com/leereilly/swot"]


def main():
    testUrl = ["https://github.com/dbcli/mycli", "https://github.com/isocpp/CppCoreGuidelines", "https://github.com/isocpp/CppCoreGuidelines", "https://github.com/BVLC/caffe", "https://github.com/obsproject/obs-studio", "https://github.com/facebookresearch/Detectron", "https://github.com/Leaflet/Leaflet", "https://github.com/runelite/runelite", "https://github.com/cosmos/cosmos-sdk", "https://github.com/leereilly/swot", "https://github.com/goplus/gop", "https://github.com/ultralytics/yolov5", "https://github.com/xeolabs/scenejs", "https://github.com/github/gemoji", "https://github.com/piskelapp/piskel", "https://github.com/kitao/pyxel", "https://github.com/cloudhead/rx", "https://github.com/Orama-Interactive/Pixelorama", "https://github.com/misterokaygo/MapAssist", "https://github.com/bhollis/jsonview", "https://github.com/rtyley/bfg-repo-cleaner", "https://github.com/mhagger/git-imerge", "https://github.com/eddiezane/lunchy", "https://github.com/awaescher/RepoZ", "https://github.com/babysor/MockingBird"]
    for x in testUrl:
        uniqueAuthors, author_objects = populateAuthors(x)

        # print(len(uniqueAuthors))
        # print(len(author_objects))
        # print(str(author_objects[0]))
        # print(str(author_objects[1]))
        # print(str(author_objects[2]))

        timeline = populateTimeline(author_objects)
        intervals = locatePairedTwoWeekPlusIntervals(timeline)
        # print(len(intervals))
    
        # calculate_code_churn(x, intervals)
        # calculate_commit_count(x, intervals)
        evaluate_metrics(x, intervals)
        
# All metric evaluations go in this function
# Evaluates metrics, then outputs the results into a table
def evaluate_metrics(repo, interval_list):
    print("%s %50s %40s" %("Interval", "Average Code Churn Per Day", "Average Commit Count Per Day"))
    
    for i in range(0, len(interval_list)): 
        pre_start_date = interval_list[i][0].date
        pre_end_date = interval_list[i][1].date
        post_end_date = interval_list[i][2].date

        activeDevsPrePeriod = interval_list[i][0].active_devs
        activeDevsPostPeriod = interval_list[i][1].active_devs
        
        pre_days_difference = abs(pre_start_date - pre_end_date).total_seconds() / 86400.0
        post_days_difference = abs(post_end_date - pre_end_date).total_seconds() / 86400.0
        
        # Metric: Code Churn (Average/day)
        pre_metric_churn = CodeChurn(path_to_repo=repo, since=pre_start_date, to=pre_end_date)
        pre_churn_total = pre_metric_churn.count()    # Returns the total code churn in range
    
        post_metric_churn = CodeChurn(path_to_repo=repo, since=pre_end_date, to=post_end_date)
        post_churn_total = post_metric_churn.count()
        
        values_array_churn = pre_churn_total.values()
        avg_churn_pre = sum(values_array_churn)/pre_days_difference
        
        values_array_churn = post_churn_total.values()
        avg_churn_post = sum(values_array_churn)/post_days_difference
        
        # Metric: Commit Count (Average/day)
        pre_metric_cc = CommitsCount(path_to_repo=repo, since=pre_start_date, to=pre_end_date)
        pre_cc_total = pre_metric_cc.count()    # Returns the total code churn in range
        
        post_metric_cc = CommitsCount(path_to_repo=repo, since=pre_end_date, to=post_end_date)
        post_cc_total = post_metric_cc.count()
        
        values_array_cc = pre_cc_total.values()
        avg_cc_pre = sum(values_array_cc)/pre_days_difference
        
        values_array_cc = post_cc_total.values()
        avg_cc_post = sum(values_array_cc)/post_days_difference
        
        print("%d   %s to %s %22s: %.3f %29s: %.3f" %(i+1, str(pre_start_date.strftime('%Y-%m-%d')), str(pre_end_date.strftime('%Y-%m-%d')), "Pre-Period", avg_churn_pre, "Pre-period", avg_cc_pre))
        print("%52s: %.3f %30s: %.3f" %("Post-period", avg_churn_post, "Post-period:", avg_cc_post))

        df.loc[len(df.index)] = [repo, str(pre_start_date.strftime('%Y-%m-%d')), str(pre_end_date.strftime('%Y-%m-%d')), str(post_end_date.strftime('%Y-%m-%d')), avg_churn_pre, avg_churn_post, avg_cc_pre, avg_cc_post, activeDevsPrePeriod, activeDevsPostPeriod]
        
    
    return None

def locatePairedTwoWeekPlusIntervals(timeline):
    # print("Attempting to locate paired two week intervals")
    significantBreakpoints = []
    for i in range (1, len(timeline)-1):
        timeDiff = timeline[i+1].date - timeline[i].date
        #print("Difference in time: " + str(timeDiff))
        if (timeDiff >= timedelta(days=14)) and (timeline[i-1].active_devs < timeline[i].active_devs) and timeline[i].active_devs >= 5:

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
data = {'Repo':[],
        'StartPeriod':[],
        'MidPeriod':[],
        'EndPeriod':[],
        'PrePeriodAvgChurn':[],
        'PostPeriodAvgChurn':[],
        'PrePeriodAvgCommits':[],
        'PostPeriodAvgCommits':[],
        'PrePeriodCommitters':[],
        'PostPeriodCommitters':[]}
df = pd.DataFrame(data=data)

# Format for inserting new line into dataframe:
# data.loc[len(data.index)] = ['Repo', 'StartPeriod', 'MidPeriod', 'EndPeriod', 'PrePeriodAvgChurn', 'PostPeriodAvgChurn', 'PrePeriodAvgCommits', 'PostPeriodAvgCommits']
main()

df.to_csv('ScrapedRepoData.csv', index=False, sep=',')