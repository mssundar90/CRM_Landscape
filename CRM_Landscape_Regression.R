setwd("~/Documents/Projects/CRMLandscape")

data<-read.csv("~/Documents/Projects/CRMLandscape/sanitized_reviews.json.csv", sep=",",dec=".",header=T)
usage_months<-data[,2]
noe_0_100<-data[,3]
noe_100_500<-data[,4]
noe_500_1000<-data[,5]
noe_above_1000<-data[,6]
position_associate<-data[,7]
position_mid_senior<-data[,8]
position_executive<-data[,9]
sentiment_score<-data[,10]

model1=lm(sentiment_score~usage_months+noe_above_1000+noe_500_1000+noe_100_500+position_associate+position_mid_senior)
summary(model1)