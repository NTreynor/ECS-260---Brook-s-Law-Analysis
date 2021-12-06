from git.exc import GitCommandError
from pydriller import Repository
from pydriller.metrics.process.code_churn import CodeChurn
from pydriller.metrics.process.commits_count import CommitsCount
from datetime import datetime, timedelta, timezone
import pandas as pd

def main():
    df = pd.read_csv ('ScrapedRepoDataTestAlternate2.csv')
    print(df)
    print(df['Day1Commits'])

    df[['PrePeriodAvgChurn','PostPeriodAvgChurn','PrePeriodAvgCommits','PostPeriodAvgCommits','PrePeriodCommitters','PostPeriodCommitters','Day1Churn','Day2Churn','Day3Churn','Day4Churn','Day5Churn','Day6Churn','Day7Churn','Day8Churn','Day9Churn','Day10Churn','Day11Churn','Day12Churn','Day13Churn','Day14Churn','Day1Commits','Day2Commits','Day3Commits','Day4Commits','Day5Commits','Day6Commits','Day7Commits','Day8Commits','Day9Commits','Day10Commits','Day11Commits','Day12Commits','Day13Commits','Day14Commits','Day1Churn_Prior','Day2Churn_Prior','Day3Churn_Prior','Day4Churn_Prior','Day5Churn_Prior','Day6Churn_Prior','Day7Churn_Prior','Day8Churn_Prior','Day9Churn_Prior','Day10Churn_Prior','Day11Churn_Prior','Day12Churn_Prior','Day13Churn_Prior','Day14Churn_Prior','Day1Commits_Prior','Day2Commits_Prior','Day3Commits_Prior','Day4Commits_Prior','Day5Commits_Prior','Day6Commits_Prior','Day7Commits_Prior','Day8Commits_Prior','Day9Commits_Prior','Day10Commits_Prior','Day11Commits_Prior','Day12Commits_Prior','Day13Commits_Prior','Day14Commits_Prior']] = df[['PrePeriodAvgChurn','PostPeriodAvgChurn','PrePeriodAvgCommits','PostPeriodAvgCommits','PrePeriodCommitters','PostPeriodCommitters','Day1Churn','Day2Churn','Day3Churn','Day4Churn','Day5Churn','Day6Churn','Day7Churn','Day8Churn','Day9Churn','Day10Churn','Day11Churn','Day12Churn','Day13Churn','Day14Churn','Day1Commits','Day2Commits','Day3Commits','Day4Commits','Day5Commits','Day6Commits','Day7Commits','Day8Commits','Day9Commits','Day10Commits','Day11Commits','Day12Commits','Day13Commits','Day14Commits','Day1Churn_Prior','Day2Churn_Prior','Day3Churn_Prior','Day4Churn_Prior','Day5Churn_Prior','Day6Churn_Prior','Day7Churn_Prior','Day8Churn_Prior','Day9Churn_Prior','Day10Churn_Prior','Day11Churn_Prior','Day12Churn_Prior','Day13Churn_Prior','Day14Churn_Prior','Day1Commits_Prior','Day2Commits_Prior','Day3Commits_Prior','Day4Commits_Prior','Day5Commits_Prior','Day6Commits_Prior','Day7Commits_Prior','Day8Commits_Prior','Day9Commits_Prior','Day10Commits_Prior','Day11Commits_Prior','Day12Commits_Prior','Day13Commits_Prior','Day14Commits_Prior']].apply(pd.to_numeric)

    df['Day1Commits'] = df['Day1Commits'].astype(float)
    df['Day2Commits'] = df['Day2Commits'].astype(float)
    df['Day3Commits'] = df['Day3Commits'].astype(float)
    df['Day4Commits'] = df['Day4Commits'].astype(float)
    df['Day5Commits'] = df['Day5Commits'].astype(float)
    df['Day6Commits'] = df['Day6Commits'].astype(float)
    df['Day7Commits'] = df['Day7Commits'].astype(float)
    df['Day8Commits'] = df['Day8Commits'].astype(float)
    df['Day9Commits'] = df['Day9Commits'].astype(float)
    df['Day10Commits'] = df['Day10Commits'].astype(float)
    df['Day11Commits'] = df['Day11Commits'].astype(float)
    df['Day12Commits'] = df['Day12Commits'].astype(float)
    df['Day13Commits'] = df['Day13Commits'].astype(float)
    df['Day14Commits'] = df['Day14Commits'].astype(float)

    #print(df.types)


    df.Day1Commits = df.Day1Commits / df.PrePeriodAvgCommits
    df.Day2Commits = df.Day2Commits / df.PrePeriodAvgCommits
    df.Day3Commits = df.Day3Commits / df.PrePeriodAvgCommits
    df.Day4Commits = df.Day4Commits / df.PrePeriodAvgCommits
    df.Day5Commits = df.Day5Commits / df.PrePeriodAvgCommits
    df.Day6Commits = df.Day6Commits / df.PrePeriodAvgCommits
    df.Day7Commits = df.Day7Commits / df.PrePeriodAvgCommits
    df.Day8Commits = df.Day8Commits / df.PrePeriodAvgCommits
    df.Day9Commits = df.Day9Commits / df.PrePeriodAvgCommits
    df.Day10Commits = df.Day10Commits / df.PrePeriodAvgCommits
    df.Day11Commits = df.Day11Commits / df.PrePeriodAvgCommits
    df.Day12Commits = df.Day12Commits / df.PrePeriodAvgCommits
    df.Day13Commits = df.Day13Commits / df.PrePeriodAvgCommits
    df.Day14Commits = df.Day14Commits / df.PrePeriodAvgCommits

    df.Day1Churn = df.Day1Churn / df.PrePeriodAvgChurn
    df.Day2Churn = df.Day2Churn / df.PrePeriodAvgChurn
    df.Day3Churn = df.Day3Churn / df.PrePeriodAvgChurn
    df.Day4Churn = df.Day4Churn / df.PrePeriodAvgChurn
    df.Day5Churn = df.Day5Churn / df.PrePeriodAvgChurn
    df.Day6Churn = df.Day6Churn / df.PrePeriodAvgChurn
    df.Day7Churn = df.Day7Churn / df.PrePeriodAvgChurn
    df.Day8Churn = df.Day8Churn / df.PrePeriodAvgChurn
    df.Day9Churn = df.Day9Churn / df.PrePeriodAvgChurn
    df.Day10Churn = df.Day10Churn / df.PrePeriodAvgChurn
    df.Day11Churn = df.Day11Churn / df.PrePeriodAvgChurn
    df.Day12Churn = df.Day12Churn / df.PrePeriodAvgChurn
    df.Day13Churn = df.Day13Churn / df.PrePeriodAvgChurn
    df.Day14Churn = df.Day14Churn / df.PrePeriodAvgChurn

    df.Day1Commits_Prior = df.Day1Commits_Prior / df.PrePeriodAvgCommits
    df.Day2Commits_Prior = df.Day2Commits_Prior / df.PrePeriodAvgCommits
    df.Day3Commits_Prior = df.Day3Commits_Prior / df.PrePeriodAvgCommits
    df.Day4Commits_Prior = df.Day4Commits_Prior / df.PrePeriodAvgCommits
    df.Day5Commits_Prior = df.Day5Commits_Prior / df.PrePeriodAvgCommits
    df.Day6Commits_Prior = df.Day6Commits_Prior / df.PrePeriodAvgCommits
    df.Day7Commits_Prior = df.Day7Commits_Prior / df.PrePeriodAvgCommits
    df.Day8Commits_Prior = df.Day8Commits_Prior / df.PrePeriodAvgCommits
    df.Day9Commits_Prior = df.Day9Commits_Prior / df.PrePeriodAvgCommits
    df.Day10Commits_Prior = df.Day10Commits_Prior / df.PrePeriodAvgCommits
    df.Day11Commits_Prior = df.Day11Commits_Prior / df.PrePeriodAvgCommits
    df.Day12Commits_Prior = df.Day12Commits_Prior / df.PrePeriodAvgCommits
    df.Day13Commits_Prior = df.Day13Commits_Prior / df.PrePeriodAvgCommits
    df.Day14Commits_Prior = df.Day14Commits_Prior / df.PrePeriodAvgCommits

    df.Day1Churn_Prior = df.Day1Churn_Prior / df.PrePeriodAvgChurn
    df.Day2Churn_Prior = df.Day2Churn_Prior / df.PrePeriodAvgChurn
    df.Day3Churn_Prior = df.Day3Churn_Prior / df.PrePeriodAvgChurn
    df.Day4Churn_Prior = df.Day4Churn_Prior / df.PrePeriodAvgChurn
    df.Day5Churn_Prior = df.Day5Churn_Prior / df.PrePeriodAvgChurn
    df.Day6Churn_Prior = df.Day6Churn_Prior / df.PrePeriodAvgChurn
    df.Day7Churn_Prior = df.Day7Churn_Prior / df.PrePeriodAvgChurn
    df.Day8Churn_Prior = df.Day8Churn_Prior / df.PrePeriodAvgChurn
    df.Day9Churn_Prior = df.Day9Churn_Prior / df.PrePeriodAvgChurn
    df.Day10Churn_Prior = df.Day10Churn_Prior / df.PrePeriodAvgChurn
    df.Day11Churn_Prior = df.Day11Churn_Prior / df.PrePeriodAvgChurn
    df.Day12Churn_Prior = df.Day12Churn_Prior / df.PrePeriodAvgChurn
    df.Day13Churn_Prior = df.Day13Churn_Prior / df.PrePeriodAvgChurn
    df.Day14Churn_Prior = df.Day14Churn_Prior / df.PrePeriodAvgChurn

    df.PostPeriodAvgChurn = df.PostPeriodAvgChurn / df.PrePeriodAvgChurn
    df.PrePeriodAvgChurn = df.PrePeriodAvgChurn / df.PrePeriodAvgChurn
    df.PostPeriodAvgCommits = df.PostPeriodAvgCommits / df.PrePeriodAvgCommits
    df.PrePeriodAvgCommits = df.PrePeriodAvgCommits / df.PrePeriodAvgCommits

    print(df)
    print(df['Day1Commits'])


    df.to_csv('ScrapedRepoDataTestAlternate2Scaled.csv', index=False, sep=',')

main()