from pydriller import Repository

urls = ["https://github.com/runelite/runelite"]

for commit in Repository(path_to_repo=urls).traverse_commits():
    print(commit.hash)