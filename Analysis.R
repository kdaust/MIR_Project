
library(data.table)
library(ggplot2)
red <- fread("./Redundancy_Metrics/Country_Metrics.csv")
setnames(red,c("Index","MeanRedund","StdevRedund","SSM"))
hist(red$MeanRedund)
pop <- fread("scripts/country.csv")
pop[,Index := 0:(nrow(pop)-1)]
red[pop, Pop_Ix := i.popularity, on = "Index"]
# redSSM <- red[!is.na(SSM),]
# redSSM <- redSSM[SSM > 0.65,]
# redSSM <- redSSM[MeanRedund > 50,]
# plot(Pop_Ix ~ SSM, data = redSSM)
# plot(SSM ~ MeanRedund, data = redSSM)
#red <- red[Pop_Ix > 0,]
red[,RedLev := fifelse(MeanRedund < 53, "R1",fifelse(MeanRedund < 63, "R2","R3"))]
red[,RedLev2 := fifelse(MeanRedund < 60, "R1","R2")]
red[,RedLev := as.factor(RedLev)]
red[,RedLev2 := as.factor(RedLev2)]
red <- red[MeanRedund > 45,]

plot(Pop_Ix ~ MeanRedund, data = red)
library(ggplot2)
ggplot(red, aes(x = RedLev2, y = Pop_Ix, group = RedLev2)) +
  geom_violin(draw_quantiles = 0.5) +
  xlab("Redundancy Level") +
  ylab("Popularity Index") +
  scale_x_discrete(labels = c("Low","Moderate", "High")) +
  ggtitle("Country")

ggsave("Country_Plot.png", width = 6, height = 5, units = "in",dpi = 600)

mod1 <- lm(Pop_Ix ~ RedLev2, weights = 1/red$StdevRedund^2, data = red)
#plot(mod1)
summary(mod1)

library(MASS)
red[Pop_Ix == 0, Pop_Ix := 1]
mod2 <- lm(Pop_Ix ~ MeanRedund, weights = 1/red$StdevRedund^2, data = red)
summary(mod2)
anova(mod2)

###pop
red <- fread("./Redundancy_Metrics/Pop_Metrics.csv")
setnames(red,c("Index","MeanRedund","StdevRedund","SSM"))
hist(red$MeanRedund)
pop <- fread("scripts/pop.csv")
pop[,Index := 0:(nrow(pop)-1)]
red[pop, Pop_Ix := i.popularity, on = "Index"]
hist(red$Pop_Ix)

red[,RedLev := fifelse(MeanRedund < 53, "R1",fifelse(MeanRedund < 63, "R2","R3"))]
red[,RedLev2 := fifelse(MeanRedund < 60, "R1","R2")]
red[,RedLev := as.factor(RedLev)]
red[,RedLev2 := as.factor(RedLev2)]

plot(Pop_Ix ~ MeanRedund, data = red)
ggplot(red, aes(x = RedLev, y = Pop_Ix, group = RedLev)) +
  geom_violin(draw_quantiles = 0.5) +
  xlab("Redundancy Level") +
  ylab("Popularity Index") +
  scale_x_discrete(labels = c("Low","Moderate", "High")) +
  ggtitle("Pop")
ggsave("Pop_Plot.png", width = 6, height = 5, units = "in", dpi = 600)


mod1 <- lm(Pop_Ix ~ RedLev, weights = 1/red$StdevRedund^2, data = red)
#plot(mod1)
summary(mod1)

red[Pop_Ix == 0, Pop_Ix := 1]
mod2 <- lm(Pop_Ix ~ MeanRedund, weights = 1/red$StdevRedund^2, data = red)
summary(mod2)
anova(mod2)

##jazz
###pop
red <- fread("./Redundancy_Metrics/Jazz_Metrics.csv")
setnames(red,c("Index","MeanRedund","StdevRedund","SSM"))
hist(red$MeanRedund)
pop <- fread("scripts/Jazz_Random.csv")
pop[,Index := 0:(nrow(pop)-1)]
red[pop, Pop_Ix := i.popularity, on = "Index"]
hist(red$Pop_Ix)

red[,RedLev := fifelse(MeanRedund < 53, "R1",fifelse(MeanRedund < 63, "R2","R3"))]
red[,RedLev2 := fifelse(MeanRedund < 60, "R1","R2")]
red[,RedLev := as.factor(RedLev)]
red[,RedLev2 := as.factor(RedLev2)]

plot(Pop_Ix ~ MeanRedund, data = red)
ggplot(red, aes(x = RedLev, y = Pop_Ix, group = RedLev)) +
  geom_violin(draw_quantiles = 0.5) +
  xlab("Redundancy Level") +
  ylab("Popularity Index") +
  scale_x_discrete(labels = c("Low","Moderate", "High")) +
  ggtitle("Jazz")
ggsave("Jazz_Plot.png", width = 6, height = 5, units = "in", dpi = 600)


mod1 <- lm(Pop_Ix ~ RedLev2, weights = 1/red$StdevRedund^2, data = red)
#plot(mod1)
summary(mod1)

red[Pop_Ix == 0, Pop_Ix := 1]
mod2 <- lm(Pop_Ix ~ MeanRedund, weights = 1/red$StdevRedund^2, data = red)
summary(mod2)
anova(mod2)

##all model
pop <- fread("Redundancy_Metrics/Pop_Metrics.csv")
setnames(pop,c("Index","MeanRedund","StdevRedund","SSM"))
pop_pop <- fread("scripts/pop.csv")
pop_pop[,Index := 0:(nrow(pop_pop)-1)]
pop[pop_pop, Pop_Ix := i.popularity, on = "Index"]
pop[,Genre := "Pop"]

country <- fread("Redundancy_Metrics/Country_Metrics.csv")
setnames(country,c("Index","MeanRedund","StdevRedund","SSM"))
country_pop <- fread("scripts/country.csv")
country_pop[,Index := 0:(nrow(country_pop)-1)]
country[country_pop, Pop_Ix := i.popularity, on = "Index"]
country[,Genre := "Country"]

jazz <- fread("Redundancy_Metrics/Jazz_Metrics.csv")
setnames(jazz,c("Index","MeanRedund","StdevRedund","SSM"))
jazz_pop <- fread("scripts/Jazz_Random.csv")
jazz_pop[,Index := 0:(nrow(jazz_pop)-1)]
jazz[jazz_pop, Pop_Ix := i.popularity, on = "Index"]
jazz[,Genre := "Jazz"]

allDat <- rbind(pop, country, jazz)
fwrite(allDat, "Combined_Results.csv")

allDat[,Genre := as.factor(Genre)]
modAll <- lm(MeanRedund ~ Pop_Ix + Genre + Genre:Pop_Ix, 
             weights = 1/allDat$StdevRedund^2,
             data = allDat)
summary(modAll)
