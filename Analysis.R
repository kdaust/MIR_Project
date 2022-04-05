setwd("~/Desktop/MIR_Project")
library(data.table)
red <- fread("./Redundancy_Metrics/Pop_Metrics.csv")
hist(red$MeanRedund)
pop <- fread("scripts/pop.csv")
pop[,Index := 0:(nrow(pop)-1)]
red[pop, Pop_Ix := i.popularity, on = "Index"]
red <- red[Pop_Ix > 0,]
red[,RedLev := fifelse(MeanRedund < 53, "R1",fifelse(MeanRedund < 63, "R2","R3"))]
red[,RedLev := as.factor(RedLev)]
plot(Pop_Ix ~ MeanRedund, data = red)
library(ggplot2)
ggplot(red, aes(x = RedLev, y = Pop_Ix, group = RedLev)) +
  geom_boxplot()
mod1 <- lm(Pop_Ix ~ RedLev, data = red)
summary(mod1)
