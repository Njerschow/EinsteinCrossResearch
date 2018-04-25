import sys
import numpy as np
import csv

WIGGLE_ROOM=0.005

reuseCtr = 0;
num = []
name = []
grade = []
sourcez = []
lensz = []
ra = []
dec = []
mags = []
magl = [] 
Nim = [] 
size = []

with open('./lenses.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
    	if (reuseCtr!=0):
    		num.append(int(row[0])-1) # minus one to make this a valid index for ~~indexing~~
    		name.append(row[1])
    		grade.append(row[2])
    		sourcez.append(row[3])
    		lensz.append(row[4])
    		
    		rdata = row[5].split(':')
    		rconv = float(rdata[0])*15.+float(rdata[1])*0.25+float(rdata[2])*0.00416667
    		ra.append(rconv)

    		ddata = row[6].split(':')
    		negative = 0
    		if(ddata[0][0]=='-'):
    			ddata[0] = -1.*float(ddata[0])
    			negative = 1
    		dconv = float(ddata[0]) + float(ddata[1])/60. + float(ddata[2])/3600
    		if (negative==1):
    			dconv = -1.*dconv
    		dec.append(dconv)

    		mags.append(row[7])
    		magl.append(row[8])
    		Nim.append(row[9])
    		size.append(float(row[10])*WIGGLE_ROOM) #convert from arcseconds to degrees (with extra wiggle room)
    	reuseCtr+=1


queries = open("Queries.txt","w") 

queries.seek(0)
queries.truncate() # empty file before writing

for i in num:
	ratop = ra[i]+size[i]  #Defining rectangle of interest 
	rabot = ra[i]-size[i]
	dectop = dec[i]+size[i]
	decbot = dec[i]-size[i]
	queries.write("java -jar casjobs.jar run 'SELECT ALL p.objid,p.ra,p.dec,pz.z INTO mydb.object_"+str(i)+" FROM PhotoObj AS p JOIN Photoz AS pz ON pz.objid = p.objid where p.ra between "+str(rabot)+" and "+str(ratop)+" and p.dec between "+str(decbot)+" and "+str(dectop)+"' \n\n")
	# and now to download table:
	#queries.write("java -jar casjobs.jar extract -b object_"+str(i)+" -F -type CSV -d ./Models/\n\n")
	# and now to drop table remotely:
	#queries.write("java -jar casjobs.jar execute -t 'mydb/1' 'drop table object_"+str(i)+"'\n\n")

queries.close()

print("donezo")
# ra = 0
# if (sys.argv[4]=="ra"):
# 	ra = 1

# h = sys.argv[1]
# m = sys.argv[2]
# s = sys.argv[3]

# converted = 0

# if (ra==1):
# 	converted = float(h)*15. + float(m)*0.25 + float(s)*0.00416667
# else:
# 	converted = float(h) + float(m)/60. + float(s)/3600.

# print(converted)