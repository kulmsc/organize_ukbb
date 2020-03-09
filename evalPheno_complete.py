import numpy as np
import pdb
import gzip
import os
import sys
import sys  
import re

useStrokeCodes = False
useSpecificCodes = False
usePittCodes = True

reload(sys)  
sys.setdefaultencoding('utf8')
r_date = re.compile('\d\d\d\d-\d\d-\d\d')

def normRead(fileName):
        with open(fileName,"r") as f:
                totalData=[]
                for line in f.read().splitlines():
                        totalData.append(line.split('\t'))
        header=totalData[0]
        del totalData[0]
        totalData=np.array(totalData)
        return(totalData,header)

def gzWrite(fileName,toWrite,isAllCode = False):
        with gzip.open(fileName,'w') as f:
		if isAllCode:
			for line in toWrite:
				f.write(line+'\n')
		else:
			for line in toWrite:
				f.write('\t'.join(line)+'\n')


def getInputs(fileName):
	primary_codes = []
	comp_codes = []
	comp_keys = []
	second_trait = []
	second_codes = []
	second_keys = []

	active_list = "primary_codes"
	num2_keys = -1
	num2_code = -1

	with open(fileName,"r") as f:
		totalData=[]
		active_list = "primary_codes"
		for ind, line in enumerate(f.read().splitlines()):

			if ind == 0:
				primary_trait = line

			elif ind == 1:
				pass

			#doing primary codes
			elif active_list == "primary_codes":
				if line.split('\t')[0] == '':
					primary_codes.append(line.split('\t')[1:])
				else:
					active_list = "comp_codes"

			#doing comp codes
			elif active_list == "comp_codes":
				if line.split('\t')[0] == '':
					toadd = line.split('\t')[1:]
					if toadd[0] == "None":
						comp_codes.append("None")
					else:
						comp_codes.append(line.split('\t')[1:])
				else:
					active_list = "comp_keys"

			#doing comp keys
			elif active_list == "comp_keys":
				if line.split('\t')[0] == '':
					comp_keys.append(line.split('\t')[1:])
				else:
					active_list = "second_trait"

			#doing second trait
			elif active_list == "second_trait":
				if line.split('\t')[0] == '':
					if line.split('\t')[1] == '':
						second_codes[num2_code].append(line.split('\t')[2:])
					else:
						second_trait.append(line.split('\t')[1:])
						second_codes.append([])
						num2_code += 1
				else:
					active_list = "second_keys"


			elif active_list == "second_keys":
				if line.split('\t')[0] == '':
					if line.split('\t')[1] == '':
						second_keys[num2_keys].append(line.split('\t')[2:])
					else:
						second_keys.append([])
						num2_keys += 1


		return(primary_trait, primary_codes, comp_codes, comp_keys, second_codes, second_trait, second_keys)




def tabulate(read_in_name, out_name, tort, primary_data = None, primary_codes = None):
	outputFile = read_in_name + ".events"
	outputTimeFile = read_in_name + ".time"

	if read_in_name == "see_data":
		come_back = "early"
		primary_data = primary_data[0]
	else:
		primary_data, primary_codes, comp_codes, comp_keys, second_codes, second_data, second_keys = getInputs(read_in_name)
		come_back = "late"

	print("INFO")
	print("primary_data")
	print(primary_data)
	print("primary_codes")
	print(primary_codes)


	if primary_data=="selfReportDisease":
		codingName="coding6.tsv"
		coding1=["20002-0.0"]
		coding2=["20002-2.28"]	
                timeCoding1=["20008-0.0"]
                timeCoding2=["20008-2.33"]
	elif primary_data=="selfReportCancer":
		codingName="coding3.tsv"
		coding1=["20001-0.0"]
		coding2=["20001-2.5"]
		timeCoding1=[None]
		timeCoding2=[None]
	elif primary_data=="icd10":
		codingName="coding19.tsv"
		coding1=["41202-0.0","41204-0.0","40006-0.0","40001-0.0","40002-0.0"]
		coding2=["41202-0.65","41204-0.183","40006-16.0","40001-1.0","40002-1.13"]
		timeCoding1=["41262-0.0","41280-0.0",None,"40000-0.0","40000-0.0"]
		timeCoding2=["41262-0.65","41280-0.212",None,"40000-1.0","40000-0.0"]
	elif primary_data=="icd9":
		codingName="coding87.tsv"
		coding1=["41203-0.0","41205-0.0","40013-0.0"]
		coding2=["41203-0.27","41205-0.29","40013-14.0"]
                timeCoding1=["41263-0.0","41281-0.0",None]
		timeCoding2=["41263-0.27","41281-0.46",None]
	elif primary_data=="opcs":
		codingName="coding240.tsv"
		coding1=["41200-0.0","41210-0.0"]
		coding2=["41200-0.48","41210-0.85"]
                timeCoding1=[None]
                timeCoding2=[None]
	elif primary_data=="bioFamily":
		codingName="coding1010.tsv"
		coding1=["20107-0.0","20110-0.0","20111-0.0"]
		coding2=["20107-2.9","20110-2.10","20111-2.11"]
                timeCoding1=[None]
                timeCoding2=[None]
	elif primary_data=="meds":
		codingName="coding4.tsv"
		coding1=["20003-0.0"]
		coding2=["20003-2.47"]
                timeCoding1=[None]
                timeCoding2=[None]
	elif primary_data=="jobs":
		codingName="coding497.tsv"
		coding1=["22601-0.0"]
		coding2=["22601-0.39"]
                timeCoding1=[None]
                timeCoding2=[None]
	elif primary_data=="blood": #nothing needs to be done
		codingName=None
		coding1=["30000-0.0"]
		coding2=["30300-0.0"]
                timeCoding1=[None]
                timeCoding2=[None]
	elif primary_data=="basics": #nothing needs to be done
		codingName=None
		coding1=[None]
		coding2=[None]
                timeCoding1=[None]
                timeCoding2=[None]

	pheno, phenoHeader = normRead("scott." + primary_data + "."+tort)
	phenoHeader = np.array(phenoHeader)


	# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
	# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
	# if the file type does not have a codingName then we are already done  
	if codingName == None:
		for i in range(pheno.shape[0]):
			for j in range(pheno.shape[1]):
				if pheno[i,j]=="NA":
					pheno[i,j] = '-12345'
				elif pheno[i,j]=="TRUE":
					pheno[i,j] = "1"
				elif pheno[i,j]=="FALSE":
					pheno[i,j] = "2"
				
		pheno = pheno.astype("float")
		np.savetxt(outputFile,pheno)
		os.system("gzip "+outputFile)
		return(None)

	# remove duplicates in the coding
	coding, codingHead=normRead(codingName)
	check = np.unique(coding[:,0],return_counts=True)
	badCode = check[0][check[1]>1]
	if len(badCode)>0:
		for bad in badCode:
			coding = coding[coding[:,0] != bad, :]

	for i in range(coding.shape[0]):
		coding[i,1] = coding[i,1].replace(" ","_")




        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
	# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
	# This section is doing some additional formatting to the pheno file, particularly making sure the time component is matched right

	subPheno = "None"
	addPheno = "None"
	codeTrack = 0
	for c1,c2,t1,t2 in zip(coding1,coding2,timeCoding1,timeCoding2):
		print("start")
		print(c1)
		print("end")
		print(c2)
		start = np.where(phenoHeader==c1)[0][0]
		end = np.where(phenoHeader==c2)[0][0]
                if t1 != None and t2 != None:
			startTime = np.where(phenoHeader==t1)[0][0]
	                endTime = np.where(phenoHeader==t2)[0][0]
		if type(subPheno) == type("None"):
			subPheno = pheno[:,start:(end+1)]
			if t1 != None and t2 != None:
				subTime = pheno[:,startTime:(endTime+1)]
			else:
				subTime = np.array([["allSame" for j in range(subPheno.shape[1])] for k in range(subPheno.shape[0])])
		else:
			addPheno = pheno[:,start:(end+1)]
			if t1 != None and t2 != None:
				addTime = pheno[:,startTime:(endTime+1)]
			else:
				addTime = np.array([["allSame" for j in range(addPheno.shape[1])] for k in range(addPheno.shape[0])])

		#data-type specific modifications
		if primary_data == "icd10":
			if codeTrack == 1:
				#Secondary Diagnosis
				realTime = np.array([["NA" for j in range(addPheno.shape[1])] for k in range(addPheno.shape[0])])
				realTime = realTime.astype(subTime.dtype)
				for j in range(realTime.shape[0]):
					goodDate = np.setdiff1d(np.where(addTime[j,:] != "NA")[0], np.where(subTime[j,:] != "NA")[0])
					realTime[j,0:len(goodDate)] = addTime[j,goodDate]
				addTime = realTime
			elif codeTrack == 4:
				#Secondary Cause of Death
				addTime = np.array(map(list, zip(*[addTime[:,0] for j in range(addPheno.shape[1])])))
	
		if type(addPheno) != type("None"):
			subPheno = np.hstack((subPheno,addPheno))
			subTime = np.hstack((subTime,addTime))

		codeTrack += 1

	# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
	# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
	# setup for making comparisons between two different phenotypes
	if come_back == "early":
		return subPheno, subTime


	if len(second_data) != 0:
		pdb.set_trace()
		all_second_pheno = []
		all_second_time = []
		all_second_code = []
		for sd, sc in zip(second_data, second_codes):
			secondPheno, secondTime = tabulate("see_data", "None", tort, sd, sc)
			all_second_pheno.append(secondPheno)
			all_second_time.append(secondTime)


	# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
	# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
	# now we actually fill in the event matrix
	#primary_codes = [["I50"], ["I46"]]
	#comp_codes = [["I46"], ["I20"]]
	#comp_keys = ["early", "compete"]
	#second_codes = [[["F104"],["F104"]]] # - can really be list of list as it now is
	#second_keys = [["None", "add"]] #- about checking out the secondPheno, secondTime

	#use goodInds to get the time and events to get the pheno
	#allCodes can be a list of lists, len(allCodes) is the number of columns of the final events
	#if any of the elements in the allCodes sublist are matched to a person then the events space is true
	#the options are compete, early, add

	events = np.zeros((subPheno.shape[0], len(primary_codes)))
	timeEvents = np.zeros((subPheno.shape[0], len(primary_codes))).astype("str")
	for k in range(subPheno.shape[0]):
		for i in range(len(primary_codes)):
			primary_inds = []
			second_inds = [[] for x in range(len(second_codes))]
			comp_inds = []

			for j in range(len(primary_codes[i])):
				if any([primary_codes[i][j] in x for x in subPheno[k,:]]):
					#primary_inds.append(np.where([primary_codes[i][j] in x for x in subPheno[k,:]]))
					primary_inds.append(np.where([primary_codes[i][j] == x for x in subPheno[k,:]]))

			if comp_codes[i] != "None":
				for j in range(len(comp_codes[i])):
					if any([comp_codes[i][j] in x for x in subPheno[k,:]]):
						#comp_inds.append(np.where([comp_codes[i][j] in x for x in subPheno[k,:]]))
						comp_inds.append(np.where([comp_codes[i][j] == x for x in subPheno[k,:]]))

			for ii in range(len(second_codes)):
				if second_codes[ii][i] != "None":
					for j in range(len(second_codes[ii][i])):
						if any([second_codes[ii][i][j] in x for x in all_second_pheno[ii][k,:]]):
							#second_inds[ii].append(np.where([second_codes[ii][i][j] in x for x in all_second_pheno[ii][k,:]]))
							second_inds[ii].append(np.where([second_codes[ii][i][j] == x for x in all_second_pheno[ii][k,:]]))

			if len(primary_inds) > 0:
				flat_primary_inds = np.unique([yy for xx in primary_inds for yy in list(xx[0])])
				flat_comp_inds = np.unique([yy for xx in comp_inds for yy in list(xx[0])])
				flat_second_inds = []
				for ii in range(len(second_codes)):
					flat_second_inds.append(np.unique([yy for xx in second_inds[ii] for yy in list(xx[0])]))


				primary_date = subTime[k, flat_primary_inds]
				if len(flat_comp_inds) > 0:
					comp_date = subTime[k, flat_comp_inds]
				else:
					comp_date = "None"

				second_date = []
				for ii in range(len(second_codes)):
					if len(flat_second_inds[ii]) > 0:
						second_date.append(all_second_time[ii][k, flat_second_inds])
					else:
						second_date.append("None")


				print("ADD")
				# ADD ##############
				for ii in range(len(second_keys)):
					if second_keys[ii][i] == "add" and type(second_date[ii]) != type("None"):
						primary_date = primary_date + second_date[ii]
				if comp_keys[i] == "add" and type(comp_date) != type("None"):
					primary_date = primary_date + comp_date
					pdb.set_trace()

				print("EARLY")
				# EARLY #############
				for ii in range(len(second_keys)):
					if second_keys[ii][i] == "early" and type(second_date[ii]) != type("None"):
						pdb.set_trace()
						just_date = [xx for xx in second_date[ii] if r_date.match(xx) is not None]
						earliest_date = np.sort(just_date)[0]
						primary_date = [xx for xx in primary_date if r_date.match(xx) is not None]
						primary_date = [xx for xx in primary_date if xx < earliest_date]
				if comp_keys[i] == "early" and type(comp_date) != type("None"):
					just_date = [xx for xx in comp_date if r_date.match(xx) is not None]
					earliest_date = np.sort(comp_date)[0]
					primary_date = [xx for xx in primary_date if r_date.match(xx) is not None]
					primary_date = [xx for xx in primary_date if xx < earliest_date]

				print("COMPETE")
				# COMPETE ###########
				for ii in range(len(second_keys)):
					if second_keys[ii][i] == "compete" and type(second_date[ii]) != type("None"):
						primary_date = []
				if comp_keys[i] == "compete" and type(comp_date) != type("None"):
					pdb.set_trace()
					primary_date = []


				print("at the bottom")
				events[k,i] = len(set(primary_date))




	print("DONE")
	np.savetxt(outputFile, events)
	os.system("gzip "+outputFile)

	np.savetxt(outputTimeFile, timeEvents, fmt="%s")
	os.system("gzip "+outputTimeFile)
	return(None)



tabulate("test_input_file", "out1", "1")

#tabulate("selfReportDisease")
#tabulate("selfReportCancer")
#tabulate("icd9")
#tabulate("icd10", ["opcs"])

#tabulate("blood")
#tabulate("opcs")
#tabulate("bioFamily")
#tabulate("meds")
#tabulate("basics")
#tabulate("jobs")
