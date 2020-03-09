library(vroom)
#this process requires two files
#one - the pheno.csv
#two - a fam file from the sample application


#phen <- read.table("scottPheno.csv.gz",sep=",",stringsAsFactors=F,header=T)
phen <- as.data.frame(vroom("scottPheno.csv.gz",delim=','))
phen2 <- as.data.frame(vroom("scottPheno2.csv.gz",delim=','))

#read in the phases, these values are ordered to the PRSs
phase1 <-  read.table("scott.phase1",stringsAsFactors=F)
phase2 <-  read.table("scott.phase2",stringsAsFactors=F)

#subset the values that are in the current phenotype file
phase1.phen <- phase1[phase1[,1] %in% phen2[,1], , drop=F]
phase2.phen <- phase2[phase2[,1] %in% phen2[,1], , drop=F]

#make phen.1 and phen.2, phenotype files that correspond to phase1 and phase2
phen.1 <- phen[phen[,1] %in% phase1.phen[,1], ]
phen.2 <- phen[phen[,1] %in% phase2.phen[,1], ]

phen2.1 <- phen2[phen2[,1] %in% phase1.phen[,1], ]
phen2.2 <- phen2[phen2[,1] %in% phase2.phen[,1], ]

#reorder phen.1 and phen.2 so that they have the same order as the PRSs
phen.1 <- phen.1[order(phen.1[,1])[rank(phase1.phen[,1])],]
phen.2 <- phen.2[order(phen.2[,1])[rank(phase2.phen[,1])],]

phen2.1 <- phen2.1[order(phen2.1[,1])[rank(phase1.phen[,1])],]
phen2.2 <- phen2.2[order(phen2.2[,1])[rank(phase2.phen[,1])],]

#make indices so that the PRSs that are not within the phen can be removed
phase1.index <- which(phase1[,1] %in% phen.1[,1])
phase2.index <- which(phase2[,1] %in% phen.2[,1])

phen.1=cbind(phen.1,phen2.1)
phen.2=cbind(phen.2,phen2.2)

saveRDS(phen.1,"scottPheno.1.RDS")
saveRDS(phen.2,"scottPheno.2.RDS")

write.table(phase1.index,"scott2.phenIndex.1",quote=F,row.names=F,col.names=F)
write.table(phase2.index,"scott2.phenIndex.2",quote=F,row.names=F,col.names=F)
