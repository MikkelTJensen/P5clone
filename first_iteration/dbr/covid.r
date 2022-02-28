#This is to the result in the report.


#Needed packages
library(RPostgres)
#library(DBI)
#library(FNN)
#library(MASS)
#library(caTools)
#library(dplyr)
library(tsfknn)

pw <- {
  "ganggang"
}

connection <- dbConnect(RPostgres::Postgres(),dbname = 'covidregressiontest',
                        host = '104.248.249.225',
                        port = 5432,
                        user = 'd504',
                        password = pw)

rm(pw)

denque <- "SELECT date AS datespec, rate AS denmark
          FROM cleansubnational
          WHERE nut = 'DK014' AND date > '2020-03-01' AND cleansubnational.date < '2020-07-31'
          AND rate IS NOT NULL
          ORDER BY datespec ASC"

result <- dbSendQuery(connection, denque)
cases <- dbFetch(result)

cases$date <- as.Date(cases$date)
cases <- aggregate(cases$denmark, by=list(cases$date), sum)

colnames(cases)[1] <- "datespec"
colnames(cases)[2] <- "denmark"

X_train_cases = cases["datespec"]
y_train_cases = cases["denmark"]


days <- as.numeric(X_train_cases$date)- as.numeric(X_train_cases$date[1]) + 1

first_day <- days[1]
last_day <- tail(days, n=1)

time_seri <- ts(y_train_cases$denmark, start = first_day, end = last_day)
plot(time_seri, main = "Daily Cases per 100.000 in DK014",   ylab="Cases per 100.000")



pred <- knn_forecasting(
  time_seri,
  30,
  lags = 1:12,
  k = c(1:10),
  msas = c("recursive"),
  cf = c("mean", "median", "weighted")
)

prat <- knn_forecasting(
  time_seri,
  40,
  lags = NULL,
  k = c(5,10,20,30,40),
  msas = c("MIMO", "recursive"),
  cf = c("mean", "median", "weighted")
)

pred$prediction # To see a time series with the forecasts

plot(pred) # To see a plot with the forecast


title(main = "Daily Cases per 100.000 in DK014",   ylab="Cases per 100.000")
ro <- rolling_origin(pred, h = 30)

ro$global_accu

plot(ro, h = 30)

dbClearResult(result)

dbDisconnect(connection)

