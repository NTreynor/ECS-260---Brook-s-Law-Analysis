from pydriller import Repository
from pydriller.metrics.process.code_churn import CodeChurn
from pydriller.metrics.process.commits_count import CommitsCount
from datetime import datetime, timedelta, timezone
from dateutil import tz
import pytz

# Can be local or remote repository
urls = ["https://github.com/NTreynor/ECS-260---Brook-s-Law-Analysis"]
# urls = ["https://github.com/cosmos/cosmos-sdk"]       
# urls = ["https://github.com/deepmind/alphafold"]      
# urls = ["https://github.com/MangoDB-io/MangoDB"]      
# urls = ["https://github.com/bcrypt-ruby/bcrypt-ruby"]
# urls = ["https://github.com/zeroclipboard/zeroclipboard"]
# urls = ["https://github.com/github/resque"]
# urls = ["https://github.com/leereilly/swot"]

'''
PermissionError: [WinError 5] Access is denied:...
Using certain methods from pydriller returns a permission error
commit.committer_name, commit.comitter_date
'''
# urls = ["https://github.com/dbcli/mycli"]

# PermissionError: [WinError 5] Access is denied: 
# urls = ["https://github.com/facebook/flow"]

 # Gets stuck for a long time (5+ minutes); Might not work?
# urls = ["https://github.com/mysql/mysql-server"]

'''
Dictionary to store active developers
key: author_name, item: list of commit dates
{"author_name": [commit_date_1, commit_date_2, ...]}
'''
# active_contributors = {}

# Two-week time period
# TWO_WEEKS = timedelta(days=14)

# Searches through all commit history
# for commit in Repository(path_to_repo=urls).traverse_commits():
    # '''
    # Print commit author information
    # No Error
    # '''
    # print(commit.hash, commit.author.name, commit.author_date)
    
    # '''
    # An attempt to do something else with commit.author.name and commit.author_date
    # No error
    # '''
    # commit_author = commit.author.name
    # commit_date = commit.author_date
    # print(commit_author, commit_date)
    
    # '''
    # Store authors into dictionary
    # PermissionError: [WinError 5] Access is denied?
    # Both lines return the same errors
    # '''
    # active_contributors[commit.author.name].append(commit.author_date)
    # active_contributors[commit_author].append(commit_date)
    
# print(active_contributors)
    

# Search through commit history between 2 dates
# start_date = datetime(2019,1,1)
# end_date = datetime(2020,1,1)
# for commit in Repository(path_to_repo=urls, since=start_date, to=end_date).traverse_commits():
#     print(commit.hash)

# TODO: Separate the hashes by day
# Issue: Appends ALL hashes into every day
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
            commit_date = (commit.committer_date).replace(tzinfo=tz.tzoffset('UTC', 28800))
            if commit_date - curr_date < one_day:
                # If commit is on the same day, add the commit hash to that day's list
                print(commit_date-curr_date)
                temp.append(commit.hash)

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

# Need to make sure that both datetime objects are either aware or naive. Can't do arithmetic between naive and aware
start_date = datetime(2021, 11, 18, tzinfo=tz.tzoffset('UTC', 28800))
daily_churn, daily_commits = calc_14_day_metrics(urls, start_date)

print(daily_churn, daily_commits)


    
# Search through a range of history from start_commit to end_commit
# start_commit = "63034431c06398c215fcaf2e1aa29ec28294f121"     # Specific to repository
# end_commit = "357daadb8b4d323216f7761b727e8154bb8178d1"       # Specific to repository
# for commit in Repository(path_to_repo=urls, from_commit=start_commit, to_commit=end_commit).traverse_commits():
#     print(commit.hash)

# Checking metrics (code_churn)
# metric = CodeChurn(path_to_repo=urls, since=start_date, to=end_date)
# churn_total = metric.count()    # Returns the total code churn in range
# churn_max = metric.max()        # Returns the max code churn in range
# churn_avg = metric.avg()        # Returns the average code churn in range

# print("Total code churn: \n", churn_total)
# print("Max code churn: \n", churn_max)
# print("Average code churn: \n", churn_avg)
