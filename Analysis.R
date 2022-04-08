setwd("~/Desktop/MIR_Project")
library(data.table)
red <- fread("./Redundancy_Metrics/Country_Metrics.csv")
setnames(red,c("Index","MeanRedund","StdevRedund","SSM"))
hist(red$MeanRedund)
pop <- fread("scripts/country.csv")
pop[,Index := 0:(nrow(pop)-1)]
red[pop, Pop_Ix := i.popularity, on = "Index"]
redSSM <- red[!is.na(SSM),]
redSSM <- redSSM[SSM > 0.65,]
redSSM <- redSSM[MeanRedund > 50,]
plot(Pop_Ix ~ SSM, data = redSSM)
plot(SSM ~ MeanRedund, data = redSSM)
#red <- red[Pop_Ix > 0,]
red[,RedLev := fifelse(MeanRedund < 53, "R1",fifelse(MeanRedund < 63, "R2","R3"))]
red[,RedLev2 := fifelse(MeanRedund < 60, "R1","R2")]
red[,RedLev := as.factor(RedLev)]
red[,RedLev2 := as.factor(RedLev2)]
#red <- red[MeanRedund > 45,]

plot(Pop_Ix ~ MeanRedund, data = red)
library(ggplot2)
ggplot(red, aes(x = RedLev2, y = Pop_Ix, group = RedLev2)) +
  geom_violin()
mod1 <- lm(Pop_Ix ~ RedLev2, weights = 1/red$StdevRedund^2, data = red)
plot(mod1)
summary(mod1)

library(MASS)
red[Pop_Ix == 0, Pop_Ix := 1]
mod2 <- lm(Pop_Ix ~ MeanRedund, weights = 1/red$StdevRedund^2, data = red)
bc <- boxcox(mod2)
(lambda <- bc$x[which.max(bc$y)])

#fit new linear regression model using the Box-Cox transformation
new_model <- lm(((Pop_Ix^lambda-1)/lambda) ~ MeanRedund,weights = 1/red$StdevRedund^2, data = red)
plot(new_model)
summary(new_model)
