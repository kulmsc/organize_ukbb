#the input if the fam file
famFile <- "scott.fam"

fam <- read.table(famFile, stringsAsFactors=F)
p1 <- read.table("p1Index",stringsAsFactors=F)
p2 <- read.table("p2Index",stringsAsFactors=F)

fam1 <- fam[p1[,1],1]
fam2 <- fam[p2[,1],1]

firstPart <- strsplit(famFile,".",fixed=T)[[1]][1]
write.table(fam1,paste0(firstPart,".phase1"),quote=F,row.names=F,col.names=F)
write.table(fam2,paste0(firstPart,".phase2"),quote=F,row.names=F,col.names=F)
