##################################################################
# Set Up Files
##################################################################

#setwd("/Users/Ben/Home/wc3data/bnet")

WCdata <- read.csv("bnetGames.csv", header=TRUE, sep=",")

# What's in here
  summary(WCdata)
  
  
# Packages
  install.packages("Hmisc")
  library(Hmisc)
  install.packages(("data.table"))
  library(data.table)



  
  
##################################################################
# Sanity Check
##################################################################

# Is p1 winning more often?
  t.test(WCdata$p1_win,WCdata$p2_win)
  
  
# Is p1 level higher?
  t.test(WCdata$p1_lvl, WCdata$p2_lvl)
  
  
# Check difference in levels
  WCdata$lvldiff <- WCdata$p1_lvl - WCdata$p2_lvl
  summary(WCdata$lvldiff)
  


  
# Look at races, maps, and heros
  describe(WCdata$p1_race)
  
  WCdata$p1_race <- factor(WCdata$p1_race,
                           levels = c(1,2,3,4,5,6,7,8),
                           labels = c("Night Elf", "Human", "Orc",
                                      "Undead", "Random Night Elf",
                                      "Random Human", "Random Orc",
                                      "Random Undead"))

  
  describe(WCdata$p1_hero_h1_id)
  
  
  WCdata$p1_race <- factor(WCdata$p1_race,
                           levels = c(1,2,3,4,5,6,7,8,9,10,
                                      11,12,13,14,15,16,17,
                                      18,19,20,21,22,23,24),
                           labels = c("DH","KOTG","POTM","WDN",
                                      "AM", "BLOOD", "MK", "PDN",
                                      "BLADE", "FS", "SH", "TC",
                                      "CL", "DK", "DL", "LCH", 
                                      "BEAST", "DR", "FL", "ALCH",
                                      "TINK", "NAGA", "PANDA",
                                      "PL"))

# Cross Tab: hero v. win %
  hero_p1_table <- table(WCdata$p1_hero_h1_id)
  round(100*prop.table(hero_p1_table), digits=0)
  cross<-table(WCdata$p1_hero_h1_id,WCdata$p1_win)
  round(prop.table(cross,1),digits=2)

  
  
##################################################################
# REGRESSIONS
##################################################################

# % impact on win % of each hero compared to DH
  fit1 <- lm(p1_win ~ factor(p1_hero_h1_id), data = WCdata)
  summary(fit1)

# Impact of lvldiff on win % (control for hero)
  fit2 <- lm(p1_win ~ lvldiff + factor(p1_hero_h1_id), data = WCdata)
  summary(fit2)

# Impact of lvldiff on win % (no controls)  
  fit3 <- lm(p1_win ~ lvldiff, data = WCdata)
  summary(fit3)

# Impact of lvldiff on win % (control for p2 level)
  fit4 <- lm(p1_win ~ lvldiff + p2_lvl, data = WCdata)
  summary (fit4)

# Impact of lvldiff on win% (control for map & p2 level)
  fit5 <- lm(p1_win ~ lvldiff + p2_lvl + factor(stage), data = WCdata)
  summary (fit5)

# Impact of lvldiff on win% (control for map & p2 level)
  #fit6 <- lm(p1_win ~ lvldiff + p2_lvl + factor(stage), data = subset(WCdata, XXXX>10)
  #summary (fit6)
  
  
############# Creating game #s by player
  table <- aggregate(WCdata$gametype, by = list(Category = WCdata$p1_name), FUN = sum)
  table2 <-aggregate(WCdata$gametype, by = list(Category = WCdata$p2_name), FUN = sum)
  table3 <- merge(table, table2, all = T)
  
  # Adding game # count to dataframe
  ### Rename columns in Table 3 as same as WCdata
  # Only then, use the merge below:
    # WCdata2 <- merge(WCdata, table3)
