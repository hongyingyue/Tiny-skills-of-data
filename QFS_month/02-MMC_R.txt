
library(plyr)
library(ggplot2)
library(reshape2)
library(ggthemes)

setwd('C:/Users/longtan/Desktop/00-Code/06-QFS_month')
Raw<-read.csv("app.csv",header=T,sep=',')
Raw=data.frame(Raw)
Raw$Month<-as.factor(Raw$Month)
#Data<-ddply(Raw,.(Month),summarize,Rate=mean(Grade),Sample=length(Month))
Data<-Raw
Data<-Data[(nrow(Data)-5):nrow(Data),]
p<-ggplot(Data,aes(x=Month,y=Rate))+geom_point(aes(size=Sample),color="blue",pch="\u2605",alpha=0.6)+scale_size_continuous(range = c(10,15))+geom_text(aes(x=Month,y=Rate+0.4,label=round(Rate,1)))
p<-p+xlab("Calendar month")+ylab("Apple store grade")+ylim(1,5)+ theme_wsj(color='gray')+theme(legend.position='none')

#write.csv(Data,"Data.csv",row.names=FALSE)




MMC<-read.csv("web.csv",header=T,sep=',')
MMC<-data.frame(MMC)
MMC<-MMC[(nrow(MMC)-5):nrow(MMC),]
MMC$Date<-as.factor(MMC$Date)
Data<-melt(MMC,id.vars="Date")

p2<-ggplot(Data,aes(x=Date,y=value,color=variable))+geom_line(aes(group=variable),size=2)+geom_point(size=2)+scale_colour_manual(values = c("sea green","blue3"))
p2<-p2+scale_y_continuous("Complaint Rate [%]",labels=scales::percent)+xlab("Calendar month")+theme_wsj(color='gray')+theme(legend.position='none')


