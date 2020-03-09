
workingName="all"
tort="2"

readFile=paste0("scottPheno.",tort,".RDS")
pheno <- readRDS(readFile)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# DEFINE ALL OF THE DIFFERENT GROUPS TO MAKE ########

#noncancer
noncancer=c("20002-0.0","20002-2.33")
noncancerAge=c("20008-0.0","20008-2.33") #first app
selfReportDiseaseList=list(noncancer,noncancerAge)

#cancer
cancer=c("20001-0.0","20001-2.5")
selfReportCancerList=list(cancer)

#icd10
icd10=c("41202-0.0","41202-0.65")
icd10Second=c("41204-0.0","41204-0.183")
icd10Cancer=c("40006-0.0","40006-16.0")
icd10Death=c("40001-0.0","40001-1.0")
icd10DeathSecond=c("40002-0.0","40002-1.13")
timeicd10=c("41280-0.0","41280-0.212") #second app
timeicd10Second=c("41262-0.0","41262-0.65") #second app
dateDeath=c("40000-0.0","40000-1.0") #first app
icd10List=list(icd10,icd10Second,icd10Cancer,icd10Death,icd10DeathSecond,timeicd10,timeicd10Second,dateDeath)

#icd9
icd9=c("41203-0.0","41203-0.27")
icd9Second=c("41205-0.0","41205-0.29")
icd9Cancer=c("40013-0.0","40013-14.0")
timeicd9=c("41263-0.0","41263-0.27") #second app
timeicd9Second=c("41281-0.0","41281-0.46")
icd9List=list(icd9,icd9Second,icd9Cancer,timeicd9,timeicd9Second)

#opcs
opcs=c("41200-0.0","41200-0.48")
opcsSecond=c("41210-0.0","41210-0.85")
opcsList=list(opcs,opcsSecond)

#family illness
fatherIllness=c("20107-0.0","20107-2.9")
motherIllness=c("20110-0.0","20111-2.10")
siblingIllness=c("20111-0.0","20111-2.11")
adoptedFatherIllness=c("20112-0.0","20112-2.6")
adoptedMotherIllness=c("20113-0.0","20113-2.5")
adoptedSiblingIllness=c("20114-0.0","20114-2.6")
bioFamilyList=list(fatherIllness,motherIllness,siblingIllness)
adoptFamilyList=list(adoptedFatherIllness,adoptedMotherIllness,adoptedSiblingIllness)

#medication
medication=c("20003-0.0","20003-2.47")
medicationList=list(medication)

#jobs
job=c("22601-0.0","22601-0.39")
jobList=list(job)

#blood
blood=c("30000-0.0","30300-0.0")
bloodList=list(blood)

#basic information
basicsSingle=c("31-0.0","189-0.0")
basicsStart=c("48-0.0","93-0.0","1259-0.0","3526-0.0","4501-0.0","20116-0.0","134-0.0","3140-0.0","4407-0.0")
basicsEnd=c("51-0.0","95-0.0","3160-0.0","3982-0.0","5364-0.0","22001-0.0","2936-0.0","3882-0.0","5959-0.0")
basicsList=list(basicsSingle,basicsStart,basicsEnd)

#all of the lists
allLists=list("selfReportDisease"=selfReportDiseaseList,"selfReportCancer"=selfReportCancerList,"icd10"=icd10List,"icd9"=icd9List,"opcs"=opcsList,
              "bioFamily"=bioFamilyList,"adoptFamily"=adoptFamilyList,"meds"=medicationList,"jobs"=jobList,"basics"=basicsList,"blood"=bloodList)


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Actually go through and pull out the indices and write

writeFunc <- function(workingName){
  outFile=paste0("scott.",workingName,".",tort)
  workingList=allLists[[workingName]]

  #basics and blood need some more work to fix the names
  if(workingName=="basics"){
    indices=which(colnames(pheno) %in% workingList[[1]])
    for(i in 1:length(workingList[[2]])){
      firstSpot=which(colnames(pheno)==workingList[[2]][i])
      secondSpot=which(colnames(pheno)==workingList[[3]][i])
      if(length(firstSpot) > 1 & length(secondSpot) > 1){
        firstSpot=firstSpot[1]
        secondSpot=secondSpot[1]
      } else if (length(firstSpot) > 1){
        spotDiff=abs(c(firstSpot[1]-secondSpot,firstSpot[2]-secondSpot))
        firstSpot=firstSpot[which(spotDiff==min(spotDiff))]
      } else if (length(secondSpot) > 1){
        spotDiff=abs(c(secondSpot[1]-firstSpot,secondSpot[2]-firstSpot))
        secondSpot=secondSpot[which(spotDiff==min(spotDiff))]
      }

      initialNames=colnames(pheno)[firstSpot:secondSpot]
      pullNames=initialNames[grep("-0.0",initialNames)]
      finalNames=pullNames[!(pullNames %in% colnames(pheno)[indices])]
      print(finalNames)
      indices=c(indices,which(colnames(pheno) %in% finalNames & 1:ncol(pheno) %in% which(!duplicated(colnames(pheno)))))
    }
    indices=unique(indices)

  } else if(workingName=="blood"){
    firstSpot=which(colnames(pheno)==workingList[[1]][1])
    secondSpot=which(colnames(pheno)==workingList[[1]][2])
    initialNames=colnames(pheno)[firstSpot:secondSpot]
    pullNames=initialNames[grep("-0.0",initialNames)]
    indices=which(colnames(pheno) %in% pullNames)

  } else {
    indices=c()
    for(labelGroup in workingList){
      indices=c(indices,which(colnames(pheno)==labelGroup[1])[1]:which(colnames(pheno)==labelGroup[2])[1])
    }
  }

  indices <- sort(indices)
  outPheno <- pheno[,indices]

  write.table(outPheno,outFile,quote=F,sep='\t',row.names=F,col.names=T)
}

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#Actually use the function

if(workingName=="all"){
  for(inputName in names(allLists)){
    print(inputName)
    writeFunc(inputName)
  }
} else {
  writeFunc(workingName)
}
