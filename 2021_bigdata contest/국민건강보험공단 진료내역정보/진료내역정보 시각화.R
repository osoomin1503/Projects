# 데이터 불러오기
nhis1 <- read.csv("진료내역정보(2020).csv", stringsAsFactors=F,header=T)
nhis2 <- read.csv("T20_2019_1백만.1.csv", stringsAsFactors=F,header=T)
nhis3 <- read.csv("T20_2019_1백만.2.csv", stringsAsFactors=F,header=T)
nhis4 <- read.csv("T20_2019_1백만.3.csv", stringsAsFactors=F,header=T)
nhis5 <- read.csv("NHIS_OPEN_T20_2018_PART1.csv", stringsAsFactors=F,header=T)
nhis6 <- read.csv("NHIS_OPEN_T20_2018_PART2.csv", stringsAsFactors=F,header=T)
nhis7 <- read.csv("NHIS_OPEN_T20_2018-PART3.csv", stringsAsFactors=F,header=T)

rs <- read.csv("질병사인분류코드1.txt", sep="\t", stringsAsFactors=F,header=T)

# 데이터 합치기
ods <- rbind(nhis1, nhis2, nhis3, nhis4, nhis5, nhis6, nhis7)

# column subset
# 필요한 컬럼만 선택하고 이름 부여
mycols1 <- c(3, 5, 8)
dataset1 <- ods[ , mycols1]
colnames(dataset1) <- c("age", "ymd", "주상병")

# Missing Value 및 R을 위한 컬럼 Format 설정
summary(dataset1)
# 연령대 범주화 바꾸기
dataset1 <- within( dataset1, {
  연령대 <- NA
  연령대[age==1 | age==2] = "09세이하"
  연령대[age==3 | age==4] = "10~19세"
  연령대[age==5 | age==6] = "20~29세"
  연령대[age==7 | age==8] = "30~39세"
  연령대[age==9 | age==10] = "40~49세"
  연령대[age==11 | age==12] = "50~59세"
  연령대[age==13 | age==14] = "60~69세"
  연령대[age==15 | age==16] = "70~79세"
  연령대[age==17] = "80~84세"
  연령대[age==18] = "85세이상"
})
dataset1 <- dataset1[-1]
summary(dataset1); str(dataset1)

# 데이터 탐색
# 기본 집계표 생성
options( digits=5 )
options( scipen = 5) # 지수표기를 숫자표기로
Totals <- nrow( dataset1 )
TotalYmd <- as.data.frame(table( dataset1$ymd )) # 날짜 기준 집계
colnames(TotalYmd) <- c("ymd","x")
CountSick <- table( dataset1$주상병 )
TotalSick <- as.data.frame(CountSick)
CountAge <-  table( dataset1$연령대 ) 
TotalAge <- as.data.frame(CountAge)
TotalSick$per <- 100*TotalSick$Freq/Totals
TotalAge$per <- 100*TotalAge$Freq/Totals

# --------------------------------------------------

# 분석 대상 선정 -> 상위 20 주상병 & 50세 이상
TopSick <- TotalSick[ order(-TotalSick$Freq),c("Var1","Freq") ]
TopSick <- TopSick[1:20,] 
colnames( TopSick ) <- c("주상병","환자수")
data <- merge(x=dataset1,y=TopSick, by='주상병')
data <- data[,c("ymd","주상병","연령대")]
data2 <- subset(data, 연령대=="50~59세"|연령대=="60~69세"|연령대=="70~79세"|연령대=="80~84세"|연령대=="80세이상")


# 상위 20 주상병만 대상으로 재집계하고 시각화
CountSick <- table( data2$주상병 )
TotalSick <- as.data.frame(CountSick)
CountAge <-  table( data2$연령대 ) 
TotalAge <- as.data.frame(CountAge)
TotalSick$per <- 100*TotalSick$Freq/Totals
TotalAge$per <- 100*TotalAge$Freq/Totals
barplot( CountSick, main="주상병", xlab="주상병", ylab="환자수" ) # 상위 20개만 시각화
barplot( CountAge, main="연령대",xlab="연령대", ylab="환자수" )

# 주상병별 연령대 집계표
#install.packages("reshape")
library(reshape)
AgeTable <- table( data2$연령대, data2$주상병 )
AgeDf <- data.frame( AgeTable )
colnames(AgeDf) <- c("연령대", "주상병", "명")
SickAge <- cast(AgeDf, 주상병~연령대, value='명', fun.aggregate=sum)

# 비교 시각화
barplot( AgeTable, main="연령대별 주상병"
         ,xlab="주상병", ylab="연령대", col=rainbow(10) )
legend(locator(1), levels(TotalAge$Var1), fill=rainbow(10))


# 100% 비율로 비교 시각화
AgeTableProp <- prop.table( AgeTable, 2)
barplot( AgeTableProp, main = "연령대별 주상병"
         ,xlab="주상병", ylab="연령대",col=rainbow(10))
legend(locator(1), levels(TotalAge$Var1), fill=rainbow(10))

# treemap으로 텍스트 시각화 해보기
library(dplyr)
library(treemap)
CountSick2 <- table( data2$주상병 )
TotalSick2 <- as.data.frame(CountSick2)
str(TotalSick2)
treemap(TotalSick2, index = c("Var1"), vSize="Freq", type="value", bg.labels="yellow")
rs$KCD분류 <- as.character(rs$KCD분류)
str(rs)
Sick <- inner_join(x=TotalSick2, y=rs, by=c("Var1"="KCD분류"))
treemap(Sick, index=c("병명"), vSize="Freq", type="value")

#install.packages("textplot")
library(textplot)
x <- sort(CountSick2)
textplot_bar(x, panel = "Code", col.panel = "darkgrey", 
             xlab = "Listings", cextext = 0.75, addpct = TRUE, cexpct = 0.5)


# --------------------------------------------------
# 분석 대상 선정 -> 상위 20 주상병 & 10-30대
TopSick <- TotalSick[ order(-TotalSick$Freq),c("Var1","Freq") ]
TopSick <- TopSick[1:20,] 
colnames( TopSick ) <- c("주상병","환자수")
data <- merge(x=dataset1,y=TopSick, by='주상병')
data <- data[,c("ymd","주상병","연령대")]
data2 <- subset(data, 연령대=="10~19세"|연령대=="20~29세"|연령대=="30~39세")


# 상위 20 주상병만 대상으로 재집계하고 시각화
CountSick <- table( data2$주상병 )
TotalSick <- as.data.frame(CountSick)
CountAge <-  table( data2$연령대 ) 
TotalAge <- as.data.frame(CountAge)
TotalSick$per <- 100*TotalSick$Freq/Totals
TotalAge$per <- 100*TotalAge$Freq/Totals
barplot( CountSick, main="주상병", xlab="주상병", ylab="환자수" ) # 상위 20개만 시각화
barplot( CountAge, main="연령대",xlab="연령대", ylab="환자수" )

# 주상병별 연령대 집계표
#install.packages("reshape")
library(reshape)
AgeTable <- table( data2$연령대, data2$주상병 )
AgeDf <- data.frame( AgeTable )
colnames(AgeDf) <- c("연령대", "주상병", "명")
SickAge <- cast(AgeDf, 주상병~연령대, value='명', fun.aggregate=sum)

# 비교 시각화
barplot( AgeTable, main="연령대별 주상병"
         ,xlab="주상병", ylab="연령대", col=rainbow(10) )
legend(locator(1), levels(TotalAge$Var1), fill=rainbow(10))


# 100% 비율로 비교 시각화
AgeTableProp <- prop.table( AgeTable, 2)
barplot( AgeTableProp, main = "연령대별 주상병"
         ,xlab="주상병", ylab="연령대",col=rainbow(10))
legend(locator(1), levels(TotalAge$Var1), fill=rainbow(10))

# treemap으로 텍스트 시각화 해보기
library(dplyr)
library(treemap)
CountSick2 <- table( data2$주상병 )
TotalSick2 <- as.data.frame(CountSick2)
str(TotalSick2)
treemap(TotalSick2, index = c("Var1"), vSize="Freq", type="value", bg.labels="yellow")
rs$KCD분류 <- as.character(rs$KCD분류)
str(rs)
Sick <- inner_join(x=TotalSick2, y=rs, by=c("Var1"="KCD분류"))
treemap(Sick, index=c("병명"), vSize="Freq", type="value")

#install.packages("textplot")
library(textplot)
x <- sort(CountSick2)
textplot_bar(x, panel = "Code", col.panel = "darkgrey", 
             xlab = "Listings", cextext = 0.75, addpct = TRUE, cexpct = 0.5)
