rm(list=ls()) 
library(car)
library(lme4)
library(tidyverse)

data=read.csv("/Users/halleh/Downloads/ECS-260---Brook-s-Law-Analysis-main/ScrapedRepoDataTestAlternate.csv")

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
 # 
 # a=t.test( data$PrePeriodAvgChurn,data$PostPeriodAvgChurn,paired=TRUE)
 # print("Summary of t-Test")
 # print(a)
 # a=cor.test( data$PrePeriodAvgChurn,data$PostPeriodAvgChurn,paired=TRUE)
 # print("Summary of cor-Test")
 # print(a)
 # 
 model1 = lm(PrePeriodAvgCommits~PostPeriodAvgCommits, data=data)
 print(summary(model1))
 # vif(model1)
 # plot(model1)
 print(anova(model1))

 data2=reshape(data=data, idvar="PrePeriodAvgCommits",
               varying = c("PrePeriodAvgChurn","PostPeriodAvgChurn"),
               v.names = "Churn",
               timevar = "Period", 
               new.row.names = 1:1000,
               direction = "long")
 data2=data2[data2$Churn>-1000,]
 ggplot(data2,aes(x=PrePeriodAvgCommits, 
                  y=Churn,
                  color=as.character(Period) ))+
         geom_point()+
         geom_smooth(method="lm")
 
a=t.test( data$PrePeriodAvgCommits,delta_churn,paired=TRUE)
print("Summary of t-Test")
print(a)
a=cor.test( data$PrePeriodAvgCommits,delta_churn,paired=TRUE)
print("Summary of cor-Test")
print(a)

model2 = lm(data$PrePeriodAvgCommits~data$PostPeriodAvgChurn, data=data)
print(summary(model2))
# vif(model2)
# plot(model2)
print(anova(model2))

model3 = lm(data$PrePeriodAvgCommits~data$PrePeriodAvgChurn, data=data)
print(summary(model3))
# vif(model3)
# plot(model3)
print(anova(model3))

#  