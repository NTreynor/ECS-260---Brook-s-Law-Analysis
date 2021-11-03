from pydriller import Repository
from pydriller.metrics.process.code_churn import CodeChurn
from datetime import datetime

# Can be local or remote repository
urls = ["https://github.com/runelite/runelite"]

# Searches through all commit history
# for commit in Repository(path_to_repo=urls).traverse_commits():
#     print(commit.hash)
    
# Search through commit history between 2 dates
start_date = datetime(2019,1,1)
end_date = datetime(2020,1,1)
# for commit in Repository(path_to_repo=urls, since=start_date, to=end_date).traverse_commits():
#     print(commit.hash)
    
# Search through a range of history from start_commit to end_commit
# start_commit = "63034431c06398c215fcaf2e1aa29ec28294f121"
# end_commit = "357daadb8b4d323216f7761b727e8154bb8178d1"
# for commit in Repository(path_to_repo=urls, from_commit=start_commit, to_commit=end_commit).traverse_commits():
#     print(commit.hash)

# Checking metrics (code_churn)
start_commit = "533bcd26be5e526681c001521e353ceb989efe2f"
end_commit = "357daadb8b4d323216f7761b727e8154bb8178d1"
metric = CodeChurn(path_to_repo=urls, since=start_date, to=end_date)
churn_total = metric.count()    # Returns the total code churn in range
churn_max = metric.max()        # Returns the max code churn in range
churn_avg = metric.avg()        # Returns the average code churn in range

print("Total code churn: \n", churn_total)
print("Max code churn: \n", churn_max)
print("Average code churn: \n", churn_avg)