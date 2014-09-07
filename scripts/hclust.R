

distance_matrix <- read.delim("~/Dropbox/PyCharm projects/mimic_analysis/data/distance_matrix.txt")

dfr <- reshape(distance_matrix, direction="wide", idvar="strain2", timevar="strain1")

d <- as.dist(dfr[, -1])

attr(d, "Labels") <- dfr[, 1]

dm <- as.matrix(dist(d))

dmf <- as.dist(dm)

write.csv(file='dataframe', x=dm)

