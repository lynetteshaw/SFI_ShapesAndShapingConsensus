
library(plyr)
library(dplyr)
library(readr)


setwd("C:/Users/prosp/Documents/GitHub/openData/operation-marching-orders.march-on")

#Reading in original data
comments <- as.data.frame(read_csv("comments.csv", col_names = TRUE))
votes <- as.data.frame(read_csv("votes.csv", col_names = TRUE))


#Rewriting variable names
names(comments)[8] <- "commentbody"
names(comments)[3:4] <- c("commentid", "authorid")

names(votes)[3:4] <- c("commentid","voterid") 


# Metadata gathered in conversations with "I am..", "I identify", and "My ..." statements posted by the moderators (user 0)
# Seperating our subset of these
identifiers <- comments[grepl("I am |I identify|My ", comments$commentbody),]
author0 <- identifiers[(identifiers$authorid == 0),]

#Comments without metadata posts
comments_clean <- comments[!(comments$commentid %in% author0$commentid),]

#Metadata posts
metadata <- comments[comments$commentid %in% author0$commentid,]


# Participant X post vote data for metadata and comments
votes_metadata <- votes[votes$commentid %in% author0$commentid,]
votes_comments <- votes[!(votes$commentid %in% author0$commentid),]


