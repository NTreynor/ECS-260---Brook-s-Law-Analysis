from git.exc import GitCommandError
from pydriller import Repository
from pydriller.metrics.process.code_churn import CodeChurn
from pydriller.metrics.process.commits_count import CommitsCount
from datetime import datetime, timedelta, timezone
import pandas as pd
import pytz


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
  
    # testUrl = ["https://github.com/dbcli/mycli", "https://github.com/isocpp/CppCoreGuidelines", "https://github.com/isocpp/CppCoreGuidelines", "https://github.com/BVLC/caffe", "https://github.com/obsproject/obs-studio", "https://github.com/facebookresearch/Detectron", "https://github.com/Leaflet/Leaflet", "https://github.com/runelite/runelite", "https://github.com/cosmos/cosmos-sdk", "https://github.com/leereilly/swot", "https://github.com/goplus/gop", "https://github.com/ultralytics/yolov5", "https://github.com/xeolabs/scenejs", "https://github.com/github/gemoji", "https://github.com/piskelapp/piskel", "https://github.com/kitao/pyxel", "https://github.com/cloudhead/rx", "https://github.com/Orama-Interactive/Pixelorama", "https://github.com/bhollis/jsonview", "https://github.com/rtyley/bfg-repo-cleaner", "https://github.com/mhagger/git-imerge", "https://github.com/eddiezane/lunchy", "https://github.com/awaescher/RepoZ", "https://github.com/babysor/MockingBird"]
    # testUrl = ["https://github.com/misterokaygo/MapAssist"] ## just testing on this for now.
    # testUrl = ["https://github.com/misterokaygo/MapAssist", "https://github.com/BVLC/caffe", "https://github.com/obsproject/obs-studio", "https://github.com/Leaflet/Leaflet", "https://github.com/github/gemoji", "https://github.com/runelite/runelite", "https://github.com/cosmos/cosmos-sdk", "https://github.com/leereilly/swot"] ## just testing on this for now.
    #testUrl = ["https://github.com/matplotlib/basemap", "https://github.com/NUBIC/ncs_navigator_core", "https://github.com/github/android", "https://github.com/pculture/unisubs", "https://github.com/mana/manaserv"]
    # testUrl = ["https://github.com/ryanb/cancan", "https://github.com/mobify/mobifyjs", "https://github.com/Netflix/SimianArmy", "https://github.com/bitly/dablooms", "https://github.com/mongodb/mongo", "https://github.com/collectiveidea/delayed_job" ]
    # testUrl = ["https://github.com/jupiterjs/canjs"]
    #"https://github.com/Shopify/batman", "https://github.com/projectwonder/wonder", "https://github.com/mono/mono"]
    #testUrl = ["https://github.com/heroku/heroku-buildpack-ruby", "https://github.com/spree/spree_reviews", "https://github.com/gwu-libraries/launchpad", "https://github.com/seajs/seajs", "https://github.com/django-nonrel/djangotoolbox", "https://github.com/lml/quadbase", "https://github.com/dellcloudedge/barclamp-nova_dashboard"]
    #testUrl = ["https://github.com/dellcloudedge/barclamp-dns", "https://github.com/zendframework/ZendDeveloperTools", "https://github.com/jupiterjs/jquerymx", "https://github.com/dojo/dojox"]
    #testUrl = ["https://github.com/litl/rauth", "https://github.com/beefproject/beef", "https://github.com/recurly/recurly-js", "https://github.com/OpenMRS/openmrs-module-htmlformentry", "https://github.com/opscode-cookbooks/postgresql"]

    #testUrl = ["https://github.com/edgecase/ruby_koans", "https://github.com/habari/system", "https://github.com/inviqa/chef-php-extra", "https://github.com/technicalpickles/homesick", "https://github.com/UnionOfRAD/manual", "https://github.com/IronFoundry/ironfoundry"]
    testUrl = ["https://github.com/msgpack/msgpack", "https://github.com/urug/urug.github.io", "https://github.com/sds/mock_redis",
               "https://github.com/JFrogDev/build-info", "https://github.com/plone/plone.api", "https://github.com/jenkinsci/jclouds-plugin",
               "https://github.com/plone/plone.app.multilingual", "https://github.com/thoughtbot/flutie", "https://github.com/rails/sprockets-rails"]
    for x in testUrl:
        try:
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
        except GitCommandError:
            print(x)
            continue
        
# All metric evaluations go in this function
# Evaluates metrics, then outputs the results into a table
def evaluate_metrics(repo, interval_list):
    print("%s %50s %40s" %("Interval", "Average Code Churn Per Day", "Average Commit Count Per Day"))
    
    for i in range(0, len(interval_list)): 
        start_date = interval_list[i][0].date
        mid_date = interval_list[i][1].date
        end_date = interval_list[i][2].date

        activeDevsPrePeriod = interval_list[i][0].active_devs
        activeDevsPostPeriod = interval_list[i][1].active_devs

        avg_churn_pre, avg_cc_pre, avg_churn_post, avg_cc_post = calc_metrics_in_range(repo, start_date, mid_date, end_date)

        daily_churn, daily_commits = calc_14_day_metrics(repo, mid_date)
        daily_churn_prior, daily_commits_prior = calc_14_day_metrics(repo, (mid_date - timedelta(seconds=1209601)))

        print("%d   %s to %s %22s: %.3f %29s: %.3f" %(i+1, str(start_date.strftime('%Y-%m-%d')), str(mid_date.strftime('%Y-%m-%d')), "Pre-Period", avg_churn_pre, "Pre-period", avg_cc_pre))
        print("%52s: %.3f %30s: %.3f" %("Post-period", avg_churn_post, "Post-period:", avg_cc_post))

        df.loc[len(df.index)] = [repo, str(start_date.strftime('%Y-%m-%d')), str(mid_date.strftime('%Y-%m-%d')), str(end_date.strftime('%Y-%m-%d')),
                                 avg_churn_pre, avg_churn_post, avg_cc_pre, avg_cc_post, activeDevsPrePeriod, activeDevsPostPeriod, daily_churn, daily_commits, daily_churn_prior, daily_commits_prior]

        df2.loc[len(df2.index)] = [repo, str(start_date.strftime('%Y-%m-%d')), str(mid_date.strftime('%Y-%m-%d')), str(end_date.strftime('%Y-%m-%d')),
                                   avg_churn_pre, avg_churn_post, avg_cc_pre, avg_cc_post, activeDevsPrePeriod, activeDevsPostPeriod, daily_churn[0], daily_churn[1],
                                   daily_churn[2], daily_churn[3], daily_churn[4], daily_churn[5], daily_churn[6], daily_churn[7], daily_churn[8], daily_churn[9],
                                   daily_churn[10], daily_churn[11], daily_churn[12], daily_churn[13], daily_commits[0], daily_commits[1], daily_commits[2], daily_commits[3],
                                   daily_commits[4], daily_commits[5], daily_commits[6], daily_commits[7], daily_commits[8], daily_commits[9], daily_commits[10], daily_commits[11],
                                   daily_commits[12], daily_commits[13], daily_churn_prior[0], daily_churn_prior[1],
                                   daily_churn_prior[2], daily_churn_prior[3], daily_churn_prior[4], daily_churn_prior[5], daily_churn_prior[6], daily_churn_prior[7], daily_churn_prior[8], daily_churn_prior[9],
                                   daily_churn_prior[10], daily_churn_prior[11], daily_churn_prior[12], daily_churn_prior[13], daily_commits_prior[0], daily_commits_prior[1], daily_commits_prior[2], daily_commits_prior[3],
                                   daily_commits_prior[4], daily_commits_prior[5], daily_commits_prior[6], daily_commits_prior[7], daily_commits_prior[8], daily_commits_prior[9], daily_commits_prior[10], daily_commits_prior[11],
                                   daily_commits_prior[12], daily_commits_prior[13]]
        
    
    return None

# def calc_14_day_metrics(repo, start_date):
#     daily_churn = []
#     for i in range (0, 14):
#         print(i)
#         days_churn = CodeChurn(path_to_repo=repo, since=(start_date + timedelta(days=(i+0))) , to=(start_date + timedelta(days=(i+1))))
#         daily_churn_total = days_churn.count()

#         values_array_cc = daily_churn_total.values()
#         daily_churn.append(sum(values_array_cc))

#     daily_commits = []
#     for i in range (0, 14):
#         print(i)
#         days_commits = CommitsCount(path_to_repo=repo, since=(start_date + timedelta(days=(i+0))), to=(start_date + timedelta(days=(i+1))))
#         daily_commits_total = days_commits.count()

#         values_array_commits = daily_commits_total.values()
#         daily_commits.append(sum(values_array_commits))

#     for i in range (0, 14):
#         print("On Day " + str(i) + " churn was " + str(daily_churn[i]) + " lines")
#         print("On Day " + str(i) + " there were " + str(daily_commits[i]) + " commits.")

#     return daily_churn, daily_commits

def calc_14_day_metrics(repo, start_date):
    end_date = start_date + timedelta(days=14)
    curr_date = start_date

    one_day = timedelta(days=1)

    days_commit_hashes = [[]]*14
    days_commits_churn = [0]*14
    days_commits_count = [0]*14

    day = 0
    temp = list()
    day_commits = 0
    for commit in Repository(path_to_repo=repo, since=start_date, to=end_date).traverse_commits():
        print("day", day)
        print(commit.hash)

        flag = 0
        while (flag == 0):
            # Check if commit was made on same day
            commit_date = (commit.committer_date)
            if commit_date - curr_date < one_day:
                # If commit is on the same day, add the commit hash to that day's list
                print(commit_date-curr_date)
                temp.append(commit.hash)

                if day >= 1:
                    print("days = " + str(day))

                days_commit_hashes[day] = temp      #TODO: If we want, can make more efficient by updating less



                days_commits_count[day] += 1
                days_commits_churn[day] -= commit.deletions
                days_commits_churn[day] += commit.insertions
                flag = 1

            else:
                # Else, increment the current day and day counter
                temp = list()
                curr_date += one_day
                day += 1
                #days_commits_count[day] += 1
                #days_commits_churn[day] -= commit.deletions
                #days_commits_churn[day] += commit.insertions

    return days_commits_churn, days_commits_count

def calc_metrics_in_range(repo, start_date, mid_date, end_date):

    pre_commits = 0
    post_commits = 0
    pre_churn = 0
    post_churn = 0

    pre_days_difference = abs(start_date - mid_date).total_seconds() / 86400.0
    post_days_difference = abs(mid_date - end_date).total_seconds() / 86400.0

    for commit in Repository(path_to_repo=repo, since=start_date, to=end_date).traverse_commits():
        if commit.committer_date < mid_date:
            pre_churn -= commit.deletions
            pre_churn += commit.insertions
            pre_commits += 1
        if commit.committer_date >= mid_date:
            post_churn -= commit.deletions
            post_churn += commit.insertions
            post_commits += 1

    pre_churn_avg = pre_churn / pre_days_difference
    pre_commits_avg = pre_commits / pre_days_difference
    post_churn_avg = post_churn / post_days_difference
    post_commits_avg = post_commits / post_days_difference

    return pre_churn_avg, pre_commits_avg, post_churn_avg, post_commits_avg



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
        'PostPeriodCommitters':[],
        'DailyChurn':[],
        'DailyCommits':[],
        'DailyChurnPrior':[],
        'DailyCommitsPrior':[]}

df = pd.DataFrame(data=data)

# Alternate method:

data2 = {'Repo':[],
        'StartPeriod':[],
        'MidPeriod':[],
        'EndPeriod':[],
        'PrePeriodAvgChurn':[],
        'PostPeriodAvgChurn':[],
        'PrePeriodAvgCommits':[],
        'PostPeriodAvgCommits':[],
        'PrePeriodCommitters':[],
        'PostPeriodCommitters':[],
         'Day1Churn':[],
         'Day2Churn':[],
         'Day3Churn':[],
         'Day4Churn':[],
         'Day5Churn':[],
         'Day6Churn':[],
         'Day7Churn':[],
         'Day8Churn':[],
         'Day9Churn':[],
         'Day10Churn':[],
         'Day11Churn':[],
         'Day12Churn':[],
         'Day13Churn':[],
         'Day14Churn':[],
         'Day1Commits':[],
         'Day2Commits':[],
         'Day3Commits':[],
         'Day4Commits':[],
         'Day5Commits':[],
         'Day6Commits':[],
         'Day7Commits':[],
         'Day8Commits':[],
         'Day9Commits':[],
         'Day10Commits':[],
         'Day11Commits':[],
         'Day12Commits':[],
         'Day13Commits':[],
         'Day14Commits':[],
         'Day1Churn_Prior':[],
         'Day2Churn_Prior':[],
         'Day3Churn_Prior':[],
         'Day4Churn_Prior':[],
         'Day5Churn_Prior':[],
         'Day6Churn_Prior':[],
         'Day7Churn_Prior':[],
         'Day8Churn_Prior':[],
         'Day9Churn_Prior':[],
         'Day10Churn_Prior':[],
         'Day11Churn_Prior':[],
         'Day12Churn_Prior':[],
         'Day13Churn_Prior':[],
         'Day14Churn_Prior':[],
         'Day1Commits_Prior':[],
         'Day2Commits_Prior':[],
         'Day3Commits_Prior':[],
         'Day4Commits_Prior':[],
         'Day5Commits_Prior':[],
         'Day6Commits_Prior':[],
         'Day7Commits_Prior':[],
         'Day8Commits_Prior':[],
         'Day9Commits_Prior':[],
         'Day10Commits_Prior':[],
         'Day11Commits_Prior':[],
         'Day12Commits_Prior':[],
         'Day13Commits_Prior':[],
         'Day14Commits_Prior':[]}

df2 = pd.DataFrame(data=data2)

# Format for inserting new line into dataframe:
# data.loc[len(data.index)] = ['Repo', 'StartPeriod', 'MidPeriod', 'EndPeriod', 'PrePeriodAvgChurn', 'PostPeriodAvgChurn', 'PrePeriodAvgCommits', 'PostPeriodAvgCommits']
main()

# df.to_csv('ScrapedRepoData.csv', index=False, sep=',')
df.to_csv('ScrapedRepoDataTest2.csv', index=False, sep=',')
df2.to_csv('ScrapedRepoDataTestAlternate2.csv', index=False, sep=',')
