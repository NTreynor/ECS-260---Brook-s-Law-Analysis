rm(list=ls()) 

library(lme4)

data=read.csv("/Users/halleh/Downloads/ECS-260---Brook-s-Law-Analysis-main/ScrapedRepoData.csv")

delta_churn=data["PostPeriodAvgChurn"]-data["PrePeriodAvgChurn"]
delta_churn=as.numeric(unlist(delta_churn))
delta_commits=data["PostPeriodAvgCommits"]-data["PrePeriodAvgCommits"]
delta_commits=as.numeric(unlist(delta_commits))

hist(delta_commits,
breaks=31,
main="Delta Commits",
xlab="Delta COmmits",
xlim=c(-30,30)
)
a=summary(delta_commits) 
print("Summary of Delta Commits")
print(a)

hist(delta_churn,
     breaks=51,
     main="Delta Churns",
     xlab="Delta Churns",
     xlim=c(-1000,1000)
)
a=summary(delta_churn)
print("Summary of Delta Churns")
print(a)

 a=t.test( data$PrePeriodAvgCommits,data$PostPeriodAvgCommits,paired=TRUE)
 print("Summary of t-Test")
 print(a)
 a=cor.test( data$PrePeriodAvgCommits,data$PostPeriodAvgCommits,paired=TRUE)
 print("Summary of cor-Test")
 print(a)
 
 a=t.test( data$PrePeriodAvgChurn,data$PostPeriodAvgChurn,paired=TRUE)
 print("Summary of t-Test")
 print(a)
 a=cor.test( data$PrePeriodAvgChurn,data$PostPeriodAvgChurn,paired=TRUE)
 print("Summary of cor-Test")
 print(a)
 
 model1 = lm(data$PrePeriodAvgCommits~data$PostPeriodAvgCommits, data=data)
 print(summary(model1))
 # vif(model1)
 plot(model1)
 print(anova(model1))
 
 
 