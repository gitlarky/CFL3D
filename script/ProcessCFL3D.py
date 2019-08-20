#==================================================================================================
# Title      : ProcessCFL3D
# Description: Pre & Post Process CFL3D Files
# Author     : Zhenyu Xu; westlark@outlook.com
# Start Time : 2019.08.01
# License    : MIT
#==================================================================================================

#============================ Module Importation ==================================================
import os
import sys

import statistics

from copy import deepcopy

import verb
#==================================================================================================

#============================ Basic Functions =====================================================
# Get the immediate level sub folder names --------------------------------------------------------
def TopLevelSubDir(dir):
	return [dir+'/'+name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir, name))]

# Get the angle of attack from the last several characters of the folder name ---------------------
def CaseNumber(List, Start=-6):
	p1=List[Start:]
	p2=p1.split('-')[1]
	p3=p2.replace('N', '-')
	p4=float(p3)

	return p4

# Get the case number from the last several characters of the folder name -------------------------
def CaseName(List, Splitter='/', Start=-6):
	p1=List[Start:]
	p2=p1.split(Splitter)[1]

	return p2

# Postprocessing cl cd cm from resid.out files of CFL3D -------------------------------------------
def CoefficientsFromFile(File='resid.out', MaxRead=5000, Accuracy=1e-6, MaxAll=False):
	c2=[]
	c3=[]
	c5=[]
	c=[0.0, 0.0, 0.0]

	if MaxAll:
		with open(File, 'r') as file:
			lines=file.readlines()[-MaxRead:]
			for line in lines:
				word=line.split()
				c2.append(float(word[2]))
				c3.append(float(word[3]))
				c5.append(float(word[5]))

			c[0]=statistics.mean(c2)
			c[1]=statistics.mean(c3)
			c[2]=statistics.mean(c5)
		file.close()
	else:
		residual=1.
		iterator=1
		while residual>Accuracy and iterator<=MaxRead:
			with open(File, 'r') as file:
				line=file.readlines()[-iterator]
				word=line.split()
				c2.append(float(word[2]))
				c3.append(float(word[3]))
				c5.append(float(word[5]))
			file.close()

			if(iterator==1):
				c[0]=c2[0]
				c[1]=c3[0]
				c[2]=c5[0]
			elif(iterator==2):
				residual=abs(c2[0]-c2[1])
				r3      =abs(c3[0]-c3[1])
				if r3>residual:
					residual=r3
				r5      =abs(c5[0]-c5[1])
				if r5>residual:
					residual=r5
				c[0]=statistics.mean(c2)
				c[1]=statistics.mean(c3)
				c[2]=statistics.mean(c5)
			else:
				residual=abs(c[0]-statistics.mean(c2))
				r3      =abs(c[1]-statistics.mean(c3))
				if r3>residual:
					residual=r3
				r5      =abs(c[2]-statistics.mean(c5))
				if r5>residual:
					residual=r5
				c[0]=statistics.mean(c2)
				c[1]=statistics.mean(c3)
				c[2]=statistics.mean(c5)
			iterator+=1

	return c

# Postprocessing a CFL3D test with variable AOA in each test --------------------------------------
def PostprocessCFL3DTest(TestDir):
	CasesDict={}
	with open(TestDir+'/DataProcessed.dat', 'w') as df:
		Cases=TopLevelSubDir(TestDir)
		for Case in Cases:
			os.chdir(Case)
			AOA=CaseNumber(Case)
			Coef=[-1,0,1]
			Coef=CoefficientsFromFile()
			CasesDict.update({AOA: Coef})
		for key in sorted(CasesDict.keys()):
			df.write("%9.2f\t% 9.6e\t% 9.6e\t% 9.6e\n" % 
				(key, CasesDict[key][0], CasesDict[key][1], CasesDict[key][2]))
	df.close()

	return CasesDict

# Postprocessing a bunch of CFL3D tests with variable AOA in each test ----------------------------
def AerodynamicPerformanceByCFL3D(RawData={}, TestDir='', Degree=2, Delta=1e-6):
	AeroPerform={}

	if RawData=={} and TestDir!='':
		RawData=PostprocessCFL3DTest(TestDir)

	Data=[]
	for key in sorted(RawData.keys()):
		d=[key, RawData[key][0], RawData[key][1], RawData[key][2]]
		Data.append(d)

	LiftAlphaPts=[]
	DragAlphaPts=[]
	MomentumAlphaPts=[]
	LiftDragRatioAlphaPts=[]
	DragLiftPts=[]
	for i in range(len(Data)):
		LiftAlphaPts.append([Data[i][1], Data[i][0]])
		DragAlphaPts.append([Data[i][2], Data[i][0]])
		MomentumAlphaPts.append([Data[i][3], Data[i][0]])
		LiftDragRatioAlphaPts.append([Data[i][1]/Data[i][2], Data[i][0]])
		DragLiftPts.append([Data[i][2], Data[i][1]])

	LiftAlpha=verb.verb_geom_NurbsCurve.byPoints(LiftAlphaPts, Degree)
	DragAlpha=verb.verb_geom_NurbsCurve.byPoints(DragAlphaPts, Degree)
	MomentumAlpha=verb.verb_geom_NurbsCurve.byPoints(MomentumAlphaPts, Degree)
	LiftDragRatioAlpha=verb.verb_geom_NurbsCurve.byPoints(LiftDragRatioAlphaPts, Degree)
	DragLift=verb.verb_geom_NurbsCurve.byPoints(DragLiftPts, Degree)

	Parameter=0
	MaxLift=[0, 0]
	MaxLiftDragRatio=[0, 0]
	while Parameter<=1:
		liftalpha=LiftAlpha.point(Parameter)
		if liftalpha[0]>MaxLift[0]:
			MaxLift=liftalpha

		liftdragratioalpha=LiftDragRatioAlpha.point(Parameter)
		if liftdragratioalpha[0]>MaxLiftDragRatio[0]:
			MaxLiftDragRatio=liftdragratioalpha
		
		Parameter+=Delta

	AeroPerform.update({'MaxLift         ': MaxLift         })
	AeroPerform.update({'MaxLiftDragRatio': MaxLiftDragRatio})

	return AeroPerform

# Postprocessing a bunch of CFL3D tests with variable AOA in each test ----------------------------
def PostprocessCFL3DProject(WorkDir=sys.argv[1]):
	with open(WorkDir+'/DataProcessed.dat', 'w') as df:
		Tests=TopLevelSubDir(WorkDir)
		for Test in Tests:
			df.write(Test)
			df.write('\n')
			CasesDict=PostprocessCFL3DTest(Test)
			TestPerform=AerodynamicPerformanceByCFL3D(RawData=CasesDict)
			for key in TestPerform.keys():
				df.write("%s:\t% 9.6e\t@\t% 9.2f\n" % 
					(key, TestPerform[key][0], TestPerform[key][1]))
			for key in sorted(CasesDict.keys()):
				df.write("%9.2f\t% 9.6e\t% 9.6e\t% 9.6e\n" % 
					(key, CasesDict[key][0], CasesDict[key][1], CasesDict[key][2]))

	df.close()

	return True
#==================================================================================================

#============================ Main Program ========================================================
PostprocessCFL3DProject()
#==================================================================================================