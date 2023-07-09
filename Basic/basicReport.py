#!/usr/bin/python3
#######################################################################################
# basicReport.py - v1.1.0
#   Fixed by: W Sherman
#   Last Updated: July 6th, 2021
######################################################################################

import os
import sys
import time

req = ['numpy','pandas','matplotlib']
try:
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.patches as pat
    from matplotlib.backends.backend_pdf import PdfPages
except ImportError as error:
    print('\n')
    print(error.__class__.__name__ )
    print('Failure to import needed dependancies: needed module not found. ' )
    print('\n')
    time.sleep(1)
    print('Installing needed software in 10sec... (Press ctrl & Z to abort install)')
    time.sleep(10) 
    for i in req:
        try:
            os.system('python3 pip install --upgrade pip')
            os.system('pip3 install {}'.format(i))
        except error:
            print('Error installing dependencies... ')
            quit()
except Exception as exception:
    # Output unexpected Exceptions.
    print(exception, False)
    print(exception.__class__.__name__ + ": " + exception.message)


# Debug flag to print out courses not added to course list (0 = off, 1 = on)
DEBUG = 0


#========================================================================================
# Functions defined to setup matplot prowIN output 
#========================================================================================
#setup calendar background
def calendarSetup(titleString):

    fig1 = plt.figure(figsize = (12, 9))
    ax1 = fig1.add_subplot(1, 1, 1)
    
    for i in range(7):
        ax1.plot([i, i], [0, 30], color = "Black", linewidth = 3)
    for i in range(24):
        ax1.plot([0, 7], [i, i], color = "Black", linewidth=0.5)
        ax1.plot([0, 7], [i+0.5, i+0.5], linestyle = "dotted", color = "Black", linewidth=0.5)
            
    ax1.set_xlim([0, 7])
    ax1.set_ylim([21, 7])
    ax1.set_title(titleString)
    ax1.set_xticks(np.arange(0.5, 7, 1.0))
    ax1.set_xticklabels(["Mon", "Tues", "Wed", "Thur", "Fri", "Sat", "Sun"])
    ax1.set_yticks(np.arange(7, 21.1, 1))
    ax1.set_yticklabels(["7:00 am", "8:00 am", "9:00 am", "10:00 am", "11:00 am", \
                         "12 noon", "1:00 pm", "2:00 pm", "3:00 pm", "4:00 pm", \
                         "5:00 pm", "6:00 pm", "7:00 pm", "8:00 pm", "9:00 pm"])
    return fig1, ax1

#plot courses on the background we just defined 
def plotCourses(CourseList, TestAxis, InstructorList):
    #define colors for plotting
    ColorList = ["CornflowerBlue", "Olive", "Chartreuse", "Gold", "GoldenRod", \
                 "Thistle", "PapayaWhip", "Black", "DarkBlue", "DimGray", \
                 "Yellow", "Silver", "Snow", "Pink", "Teal", \
                 "SlateBlue", "IndianRed", "DarkGreen", "DeepPink", "LightGreen", \
                 "LightSkyBlue", "MediumOrchid", "Orange", "Purple", "Maroon","Salmon","DarkRed"]
    FontColors = ["Black", "White", "Black", "Black", "White", \
                  "Black", "Black", "White", "White", "White", \
                  "Black", "Black", "Black", "Black", "White", \
                  "White", "Black", "White", "White", "Black", \
                  "Black", "Black", "Black", "White", "White","Black","White"]

    concurCourses = np.zeros((7, 14*60+1), dtype="int")
    plottedCourses = np.zeros((7, 14*60+1), dtype="int")
    legendInstructors = []
    
    for day in range(7):
        for timeSlot in np.arange(7.0, 21 + 1.0/60.0, 1.0/60.0):
            count = 0
            for course in CourseList:
                if (course.DAYSBOOL[day] and course.BeginTime <= timeSlot and course.EndTime >= timeSlot):
                    count = count + 1
            concurCourses[day, int((timeSlot - 7) * 60)] = count
    
    #plot each course on its respective graph
    for course in CourseList:
        if (course.BeginTime != None and course.EndTime != None):
            beginTIndex = int((course.BeginTime - 7) * 60)
            endTIndex   = int((course.EndTime - 7) * 60)
        
            for day in range(7):
                if (course.DAYSBOOL[day]):
                    boxSize = 1.0 / float(concurCourses[day, beginTIndex:endTIndex].max())
                    if (not (course.INST in legendInstructors)):
                        TestAxis.add_patch(pat.Rectangle((day + boxSize * plottedCourses[day, beginTIndex:endTIndex].max(), course.BeginTime), \
                                                     boxSize, course.EndTime-course.BeginTime, label=course.INST.split(",")[0], \
                                                     ec = "Black", fc = ColorList[InstructorList.index(course.INST)]))
                        legendInstructors.append(course.INST)
                    else:
                        TestAxis.add_patch(pat.Rectangle((day + boxSize * plottedCourses[day, beginTIndex:endTIndex].max(), course.BeginTime), \
                                                     boxSize, course.EndTime-course.BeginTime, \
                                                     ec = "Black", fc = ColorList[InstructorList.index(course.INST)]))

                    classString = course.DEPT+str(course.COURSE)+"\n"+course.BUILDING+str(course.ROOM)
                    TestAxis.text(day + boxSize * plottedCourses[day, beginTIndex:endTIndex].max() + 0.5 * boxSize, \
                                  (course.BeginTime + course.EndTime) / 2.0, \
                                  classString, color=FontColors[InstructorList.index(course.INST)], horizontalalignment="center", \
                                  verticalalignment="center", fontsize=6, fontweight="bold")
                    plottedCourses[day, beginTIndex:endTIndex] = plottedCourses[day, beginTIndex:endTIndex] + 1
    
    TestAxis.legend(loc="lower right")

#========================================================================
# Class to create course objects for each row in dataframe
#========================================================================
class classRecord:
    def __init__(self,index,dept,ssts,crn,course,sec,days,time,loc,inst):
        self.ACTIVE = ssts
        self.CRN = crn
        self.SEC = sec
        self.COURSE = course
        self.INST = inst

        if(course[-1]== 'L'):
            self.DEPT = dept
            self.COURSE = course[-4:-1]
            self.LabSec = True
        else:
            self.DEPT = dept
            self.COURSE = course[-3:]
            self.LABSEC = False

        self.dayCodes = ['M','T','W','R','F','S','U']
        self.DAYSBOOL = np.zeros(7, dtype=bool)
        for i in range(7):
            try:
                if(days != 'TBA'):
                    if(self.dayCodes[i] in days):
                        self.DAYSBOOL[i] = True
            except:
                self.DAYSBOOL[i] = False

        if time != '' and pd.isna(time) != True:
            splitTime = time.split()
            if splitTime[0] != 'TBA':
                self.BeginTime = int(splitTime[0][0:-2]) + (int(splitTime[0][-2:]) / 60.0)
                self.EndTime = int(splitTime[1][0:-2]) + (int(splitTime[1][-2:]) / 60.0) 
            else:
                self.BeginTime = None
                self.EndTime = None
        else:
            self.BeginTime = None
            self.EndTime = None
        
        if loc != '' and pd.isna(loc) != True:
            splitLoc = loc.split()
            self.BUILDING = splitLoc[0]

            if splitLoc[0] != 'TBA' and splitLoc[0] != 'WEB' and len(splitLoc)>1:
                self.ROOM = int(splitLoc[1])
            else:
                self.ROOM = None
        else:
            self.BUILDING = None
            self.ROOM = None


#========================================================================
# Import csv into pandas dataframe and make class objects out of each row
#========================================================================
#Take in csv file path from user and notify if not found
try:
    csv = sys.argv[1] 
except IndexError:
    csv = input('No CSV file path was found, enter CSV file path now: ')
    print('\n')

print('Input CSV path: {}'.format(csv))

df = pd.read_csv(csv)

courseList = []

for i in range(0,len(df)):
    courseList.append(classRecord(i,df.at[i,'DEPT'],df.at[i,'SSTS'],df.at[i,'CRN'],df.at[i,'COURSE'],df.at[i,'SEC'],df.at[i,'DAYS'],df.at[i,'TIME'],df.at[i,'LOCATION'],df.at[i,'INSTRUCTOR']))

print(len(courseList))


#========================================================================
# Sort course objects into their respective groupings
#========================================================================
InstructorList = []

BLYCourses = []
Level101_102Courses = []
Level121_122Courses = []
Level300Courses = []
Level400Courses = []
Level500Courses = []
Level300and400Courses = []
Core_Courses = []

ELSCB18Courses = []
ELSCB43Courses = []
ELSCB45Courses = []
ELSCB119Courses = []
ELSCB131Courses = []
ELSCB139Courses = []
ELSCB142Courses = []
ELSCB144Courses = []
ELSCB211Courses = []
ELSCB219Courses = []
ELSCB225Courses = []
ELSCB226Courses = []
ELSCB237Courses = []
ELSCB240Courses = []
ELSCB241Courses = []
LSLH3Courses = []

notCaught = []

typeList = [BLYCourses,Level101_102Courses,Level121_122Courses,Level300Courses,Level400Courses,
    Level500Courses,Level300and400Courses,Core_Courses,ELSCB18Courses,ELSCB43Courses,ELSCB45Courses,
    ELSCB119Courses,ELSCB131Courses,ELSCB139Courses,ELSCB142Courses,ELSCB144Courses,ELSCB211Courses,
    ELSCB219Courses,ELSCB225Courses,ELSCB226Courses,ELSCB237Courses,ELSCB240Courses,ELSCB241Courses,
    LSLH3Courses]

figTitles = ["BLY Courses","BLY 100-102 Courses","BLY 121-122 Courses","300 Level Courses",
    "400 Level Courses","500 Level Courses","300-400 Level Courses","Core_Courses","LSCB 18 Courses",
    "LSCB 43 Courses","LSCB 45 Courses","LSCB 119 Courses","LSCB 131 Courses","LSCB 139 Courses",
    "LSCB 142 Courses","LSCB 144 Courses","LSCB 211 Courses","LSCB 219 Courses","LSCB 225 Courses",
    "LSCB 226 Courses","LSCB 237 Courses","LSCB 240 Courses","LSCB 241 Courses","LSLH 3 Courses"]

for course in courseList:
    if (not (course.INST in InstructorList) and pd.isna(course.INST) != True):
        InstructorList.append(course.INST)
    if (course.DEPT == "BLY"):
        BLYCourses.append(course)
    if (float(course.COURSE) >= 101 and float(course.COURSE) <= 102):
        Level101_102Courses.append(course)
    if (float(course.COURSE) >= 121 and float(course.COURSE) <= 122):
        Level121_122Courses.append(course)
    if (float(course.COURSE) >= 305 and float(course.COURSE) < 400):
        Level300Courses.append(course)
    if (float(course.COURSE) >= 400 and float(course.COURSE) < 500):
        Level400Courses.append(course)
    if (float(course.COURSE) >= 500 and float(course.COURSE) < 600):
        Level500Courses.append(course)
    if (float(course.COURSE) >= 306 and float(course.COURSE) < 500):
        Level300and400Courses.append(course)
    if (float(course.COURSE) >= 300 and float(course.COURSE) < 306):
        Core_Courses.append(course)
        
    if course.BUILDING == 'ELSCB':
        if (course.ROOM == 18):
            ELSCB18Courses.append(course)
        if (course.ROOM == 43):
            ELSCB43Courses.append(course)
        if (course.ROOM == 45):
            ELSCB45Courses.append(course)
        if (course.ROOM == 119):
            ELSCB119Courses.append(course)
        if (course.ROOM == 131):
            ELSCB131Courses.append(course)
        if (course.ROOM == 139):
            ELSCB139Courses.append(course)
        if (course.ROOM == 142):
            ELSCB142Courses.append(course)
        if (course.ROOM == 144):
            ELSCB144Courses.append(course)
        if (course.ROOM == 211):
            ELSCB211Courses.append(course)
        if (course.ROOM == 219):
            ELSCB219Courses.append(course)
        if (course.ROOM == 225):
            ELSCB225Courses.append(course)
        if (course.ROOM == 226):
            ELSCB226Courses.append(course)
        if (course.ROOM == 237):
            ELSCB237Courses.append(course)
        if (course.ROOM == 240):
            ELSCB240Courses.append(course)
        if (course.ROOM == 241):
            ELSCB241Courses.append(course)
    elif course.BUILDING == 'LSLH':
        if (course.ROOM == 3):
            LSLH3Courses.append(course)
    else:
        notCaught.append(course.CRN)


if DEBUG:
    print(notCaught)


#========================================================================
# Make PDF and the save each figure to a new page
#========================================================================
with PdfPages("CourseReport.pdf") as pdf:
    for i in range(len(typeList)):
        TestFig1, TestAxis1 = calendarSetup(figTitles[i])
        plotCourses(typeList[i],TestAxis1, InstructorList)
        pdf.savefig(TestFig1)
        plt.close(TestFig1)

    for Instructor in InstructorList:
        shortInstructor = Instructor.split(",")[0]
        tempList = []
        for course in courseList:
            if (Instructor == course.INST):
                tempList.append(course)
        TestFig1, TestAxis1 = calendarSetup(shortInstructor + " Courses")
        plotCourses(tempList, TestAxis1, InstructorList)
        pdf.savefig(TestFig1)
        plt.close(TestFig1)
