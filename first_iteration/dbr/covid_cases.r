#This is the example of Denmark in theory.

library(tsfknn)
library(RPostgres)

pw <- {
  "ganggang"
}

connection <- dbConnect(RPostgres::Postgres(),dbname = 'covidregressiontest',
                        host = '104.248.249.225',
                        port = 5432,
                        user = 'd504',
                        password = pw)

rm(pw)

que <- "
        SELECT daterep AS date, cases AS denmark
        FROM casesbycountry
        WHERE country = 'Denmark' AND daterep > '2020-02-26'
        ORDER BY daterep ASC
        ;"

result <- dbSendQuery(connection, que)
cases <- dbFetch(result)

X_train_cases = cases["date"]
y_train_cases = cases["denmark"]


days <- as.numeric(X_train_cases$date)- as.numeric(X_train_cases$date[1]) + 1

first_day <- days[1]
last_day <- tail(days, n=1)

time_seri <- ts(y_train_cases$denmark, start = first_day, end = last_day, ylim = )
plot(time_seri, xy.label = FALSE)


pred <- knn_forecasting(
  time_seri,
  30,
  lags = 1:30,
  k = c(5),
  msas = c("recursive"),
  cf = c("weighted")
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

title(main = "Cases in Denmark",   ylab="Cases")

dbClearResult(result)

dbDisconnect(connection)
