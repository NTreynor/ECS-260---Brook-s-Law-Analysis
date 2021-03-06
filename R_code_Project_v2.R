rm(list=ls()) 
library(car)
library(lme4)
library(tidyverse)

#Read data
data=read.csv("/Users/halleh/Downloads/ECS-260---Brook-s-Law-Analysis-main/ScrapedRepoDataTestAlternate.csv")
data=na.omit(data)

#QQ Plot
par(mfcol = c(1, 2))
qqnorm(data$PrePeriodAvgChurn, 
       ylab = "PrePeriodAvgChurn")
qqline(data$PrePeriodAvgChurn)

qqnorm(data$PostPeriodAvgChurn, 
       ylab = "PostPeriodAvgChurn")
qqline(data$PostPeriodAvgChurn)

#Filter data
data=data[data$PrePeriodAvgChurn>-681.4,]
data=data[data$PrePeriodAvgChurn<1643.43,]
data=data[data$PostPeriodAvgChurn>-681.4,]
data=data[data$PostPeriodAvgChurn<1643.43,]

data=data[data$PostPeriodAvgCommits<15,]
data=data[data$PrePeriodAvgCommits<15,]

#Delta Model
delta_churn=data["PostPeriodAvgChurn"]-data["PrePeriodAvgChurn"]
delta_churn=as.numeric(unlist(delta_churn))
delta_commits=data["PostPeriodAvgCommits"]-data["PrePeriodAvgCommits"]
delta_commits=as.numeric(unlist(delta_commits))

hist(delta_commits,
breaks=21,
main="Delta Commits",
xlab="Delta Commits",
xlim=c(-10,10)
)
a=summary(delta_commits) 
print("Summary of Delta Commits")
print(a)

hist(delta_churn,
     breaks=51,
     main="Delta Churn",
     xlab="Delta Churn",
     xlim=c(-1000,1000)
)
a=summary(delta_churn)
print("Summary of Delta Churns")
print(a)

#Regression Model
 a=t.test( data$PrePeriodAvgCommits,data$PostPeriodAvgCommits,paired=TRUE)
 print("Summary of t-Test")
 print(a)
 a=cor.test( data$PrePeriodAvgCommits,data$PostPeriodAvgCommits,paired=TRUE)
 print("Summary of cor-Test")
 print(a)
 # 
 model1 = lm(PrePeriodAvgCommits~PostPeriodAvgCommits, data=data)
 print(summary(model1))
 # vif(model1)
 plot(model1)
 print(anova(model1))
 
 ggplot(data,aes(x=PrePeriodAvgCommits, 
                 y=PostPeriodAvgCommits ))+
   geom_point()+
   geom_smooth(method="lm")
 
 a=t.test( data$PrePeriodAvgChurn,data$PostPeriodAvgChurn,paired=TRUE)
 print("Summary of t-Test")
 print(a)
 a=cor.test( data$PrePeriodAvgChurn,data$PostPeriodAvgChurn,paired=TRUE)
 print("Summary of cor-Test")
 print(a)
 # 
model2 = lm(data$PrePeriodAvgChurn~data$PostPeriodAvgChurn, data=data)
print(summary(model2))
# vif(model2)
plot(model2)
print(anova(model2))



ggplot(data,aes(x=PrePeriodAvgChurn, 
                y=PostPeriodAvgChurn ))+
  geom_point()+
  geom_smooth(method="lm")

#  