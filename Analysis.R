setwd("~/Desktop/MIR_Project")
library(data.table)
red <- fread("./Redundancy_Metrics/Pop_Metrics.csv")
hist(red$MeanRedund)
pop <- fread("scripts/pop.csv")
pop[,Index := 0:(nrow(pop)-1)]
red[pop, Pop_Ix := i.popularity, on = "Index"]
red <- red[Pop_Ix > 0,]
plot(Pop_Ix ~ MeanRedund, data = red)
