import csv
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
import matplotlib.patches as mpatches

#==============================================================
# This program runs off Banner report ZSSR0001 (class schedule)
# Ask Cathi to run it amd email it to me, save as a .csv file
# Then change the file name on line 157 of this code.
#==============================================================
# Plot the list of courses provided, 
#==============================================================
def plotCourses(CourseList, TestAxis, InstructorList):
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
            for record in CourseList:
                if (record.Days[day] and record.BeginTime <= timeSlot and record.EndTime >= timeSlot):
                    count = count + 1
            concurCourses[day, int((timeSlot - 7) * 60)] = count
    
    for record in CourseList:
        if (record.BeginTime != None and record.EndTime != None):
            beginTIndex = int((record.BeginTime - 7) * 60)
            endTIndex   = int((record.EndTime - 7) * 60)
        
            for day in range(7):
                if (record.Days[day]):
                    boxSize = 1.0 / float(concurCourses[day, beginTIndex:endTIndex].max())
                    if (not (record.Instructor in legendInstructors)):
                        TestAxis.add_patch(Rectangle((day + boxSize * plottedCourses[day, beginTIndex:endTIndex].max(), record.BeginTime), \
                                                     boxSize, record.EndTime-record.BeginTime, label=record.Instructor.split(",")[0], \
                                                     ec = "Black", fc = ColorList[InstructorList.index(record.Instructor)]))
                        legendInstructors.append(record.Instructor)
                    else:
                        TestAxis.add_patch(Rectangle((day + boxSize * plottedCourses[day, beginTIndex:endTIndex].max(), record.BeginTime), \
                                                     boxSize, record.EndTime-record.BeginTime, \
                                                     ec = "Black", fc = ColorList[InstructorList.index(record.Instructor)]))

                    classString = record.Department+str(record.Course)+"\n"+record.Building+str(record.Room)
                    TestAxis.text(day + boxSize * plottedCourses[day, beginTIndex:endTIndex].max() + 0.5 * boxSize, \
                                  (record.BeginTime + record.EndTime) / 2.0, \
                                  classString, color=FontColors[InstructorList.index(record.Instructor)], horizontalalignment="center", \
                                  verticalalignment="center", fontsize=6, fontweight="bold")
                    plottedCourses[day, beginTIndex:endTIndex] = plottedCourses[day, beginTIndex:endTIndex] + 1
    
    TestAxis.legend(loc="lower right")
    
    
#==============================================================
# Set up the base calendar.  Return the figure and axis references.
#==============================================================
def calendarSetup(titleString):

    fig1 = figure(figsize = (12, 9))
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


#==============================================================
# Set up a class to keep track of each class' important data
#==============================================================
class classRecord:
    def __init__(self, standardList):
        self.Term        = standardList[1]
        self.CRN         = int(standardList[2])
        
        if(standardList[3][-1] == "L"):
            self.Department = standardList[3][0:-4]
            self.Course     = int(standardList[3][-4:-1])
            self.LabSection = True
        else:
            self.Department = standardList[3][0:-3]
            self.Course     = int(standardList[3][-3:])
            self.LabSection = False

        self.Section     = int(standardList[4])
        self.CourseTitle = standardList[5]
        self.Instructor  = standardList[14]
        
        self.dayCodes = ["M", "T", "W", "R", "F", "S", "U"]
        self.Days        = [False, False, False, False, False, False, False]
        for i in range(7):
            try:
                if (standardList[8] != "TBA"):
                    if (self.dayCodes[i] in standardList[8]):
                        self.Days[i] = True
            except:
                self.Days[i] = False
        
        if (standardList[9] != ""):
            splitTimes = standardList[9].split()
            if (splitTimes[0] != "TBA"):
                self.BeginTime = int(splitTimes[0][0:-2]) + (int(splitTimes[0][-2:]) / 60.0)
            else:
                self.BeginTime = None
            if (splitTimes[1] != "TBA"):
                self.EndTime = int(splitTimes[1][0:-2]) + (int(splitTimes[1][-2:]) / 60.0)
            else:
                self.EndTime = None
        else:
            self.BeginTime = None
            self.EndTime = None

        if(standardList[10] != ""):
            splitLocation = standardList[10].split()
            self.Building = splitLocation[0]

            if(len(splitLocation) > 1):
                if(splitLocation[1] != "WEB"):
                    self.Room = int(splitLocation[1])
                else:
                    self.Room = None
            else:
                self.Room = None
        else:
            self.Building = None
            self.Room = None 
               

#==============================================================
# Open file and read it in... then make new objects for each class
#==============================================================
#fileRead = open("Spring2015-schedule-8Sep2014.csv")
fileRead = open("bannerSample.csv")
#*******NOTE*******
# If the program crashes, try removing the comment files from the spreadsheet above
# They are listed without an instructor and cause the InstructorList list index to go out of range.

fileTable = csv.reader(fileRead)

classList = []

count = 0
for line in fileTable:
    if (count == 0):
        line.append("A")
    else:
        newClass = classRecord(line[1:])
        if( line[2] == "A"):
            classList.append(newClass)
    count = count + 1
    
fileRead.close()


#==============================================================
# Sort the objects into the appropriate bins
#==============================================================

InstructorList = []

BLYCourses = []
Level101_102Courses = []
Level121_122Courses = []
Level300Courses = []
Level400Courses = []
Level500Courses = []
Level300and400Courses = []
Core_Courses = []

LSCB18Courses = []
LSCB43Courses = []
LSCB45Courses = []
LSCB119Courses = []
LSCB131Courses = []
LSCB139Courses = []
LSCB142Courses = []
LSCB144Courses = []
LSCB211Courses = []
LSCB219Courses = []
LSCB225Courses = []
LSCB226Courses = []
LSCB237Courses = []
LSCB240Courses = []
LSCB241Courses = []
LSLH3Courses = []

for record in classList:
    if (not (record.Instructor in InstructorList)):
        InstructorList.append(record.Instructor)
    if (record.Department == "BLY"):
        BLYCourses.append(record)
    if (float(record.Course) >= 101 and float(record.Course) <= 102):
        Level101_102Courses.append(record)
    if (float(record.Course) >= 121 and float(record.Course) <= 122):
        Level121_122Courses.append(record)
    if (float(record.Course) >= 305 and float(record.Course) < 400):
        Level300Courses.append(record)
    if (float(record.Course) >= 400 and float(record.Course) < 500):
        Level400Courses.append(record)
    if (float(record.Course) >= 500 and float(record.Course) < 600):
        Level500Courses.append(record)
    if (float(record.Course) >= 305 and float(record.Course) < 500):
        Level300and400Courses.append(record)
    if (float(record.Course) >= 301 and float(record.Course) < 304):
        Core_Courses.append(record)
        
    if (record.Building == "LSCB" and record.Room == 18):
        LSCB18Courses.append(record)
    if (record.Building == "LSCB" and record.Room == 43):
        LSCB43Courses.append(record)
    if (record.Building == "LSCB" and record.Room == 45):
        LSCB45Courses.append(record)
    if (record.Building == "LSCB" and record.Room == 119):
        LSCB119Courses.append(record)
    if (record.Building == "LSCB" and record.Room == 131):
        LSCB131Courses.append(record)
    if (record.Building == "LSCB" and record.Room == 139):
        LSCB139Courses.append(record)
    if (record.Building == "LSCB" and record.Room == 142):
        LSCB142Courses.append(record)
    if (record.Building == "LSCB" and record.Room == 144):
        LSCB144Courses.append(record)
    if (record.Building == "LSCB" and record.Room == 211):
        LSCB211Courses.append(record)
    if (record.Building == "LSCB" and record.Room == 219):
        LSCB219Courses.append(record)
    if (record.Building == "LSCB" and record.Room == 225):
        LSCB225Courses.append(record)
    if (record.Building == "LSCB" and record.Room == 226):
        LSCB226Courses.append(record)
    if (record.Building == "LSCB" and record.Room == 237):
        LSCB237Courses.append(record)
    if (record.Building == "LSCB" and record.Room == 240):
        LSCB240Courses.append(record)
    if (record.Building == "LSCB" and record.Room == 241):
        LSCB241Courses.append(record)
    if (record.Building == "LSLH" and record.Room == 3):
        LSLH3Courses.append(record)

#==============================================================
# Set up the plotting
#==============================================================

TestFig1, TestAxis1 = calendarSetup("BLY Courses")
plotCourses(BLYCourses, TestAxis1, InstructorList)
TestFig1.savefig("all BLY Courses.png")
plt.close(TestFig1)

TestFig1, TestAxis1 = calendarSetup("BLY 100 lecture Courses")
plotCourses(Level101_102Courses, TestAxis1, InstructorList)
TestFig1.savefig("BLY 101-102 Courses.png")
plt.close(TestFig1)

TestFig1, TestAxis1 = calendarSetup("BLY 100 lecture Courses")
plotCourses(Level121_122Courses, TestAxis1, InstructorList)
TestFig1.savefig("BLY 121-122 Courses.png")
plt.close(TestFig1)

TestFig1, TestAxis1 = calendarSetup("300 level Courses")
plotCourses(Level300Courses, TestAxis1, InstructorList)
TestFig1.savefig("300 Level Courses.png")
plt.close(TestFig1)

TestFig1, TestAxis1 = calendarSetup("400 level Courses")
plotCourses(Level400Courses, TestAxis1, InstructorList)
TestFig1.savefig("400 Level Courses.png")
plt.close(TestFig1)

TestFig1, TestAxis1 = calendarSetup("500 level Courses")
plotCourses(Level500Courses, TestAxis1, InstructorList)
TestFig1.savefig("500 Level Courses.png")
plt.close(TestFig1)

TestFig1, TestAxis1 = calendarSetup("300-400 level Courses")
plotCourses(Level300and400Courses, TestAxis1, InstructorList)
TestFig1.savefig("300-400 Level Courses.png")
plt.close(TestFig1)

TestFig1, TestAxis1 = calendarSetup("Core_Courses")
plotCourses(Core_Courses, TestAxis1, InstructorList)
TestFig1.savefig("Core_Courses.png")
plt.close(TestFig1)

TestFig4, TestAxis4 = calendarSetup("LSCB18 Courses")
plotCourses(LSCB18Courses, TestAxis4, InstructorList)
TestFig4.savefig("LSCB 18 Courses.png")
plt.close(TestFig4)

TestFig4, TestAxis4 = calendarSetup("LSCB43 Courses")
plotCourses(LSCB43Courses, TestAxis4, InstructorList)
TestFig4.savefig("LSCB 43 Courses.png")
plt.close(TestFig4)

TestFig4, TestAxis4 = calendarSetup("LSCB45 Courses")
plotCourses(LSCB45Courses, TestAxis4, InstructorList)
TestFig4.savefig("LSCB 45 Courses.png")
plt.close(TestFig4)

TestFig4, TestAxis4 = calendarSetup("LSCB119 Courses")
plotCourses(LSCB119Courses, TestAxis4, InstructorList)
TestFig4.savefig("LSCB 119 Courses.png")
plt.close(TestFig4)

TestFig4, TestAxis4 = calendarSetup("LSCB131 Courses")
plotCourses(LSCB131Courses, TestAxis4, InstructorList)
TestFig4.savefig("LSCB 131 Courses.png")
plt.close(TestFig4)

TestFig4, TestAxis4 = calendarSetup("LSCB139 Courses")
plotCourses(LSCB139Courses, TestAxis4, InstructorList)
TestFig4.savefig("LSCB 139 Courses.png")
plt.close(TestFig4)

TestFig4, TestAxis4 = calendarSetup("LSCB142 Courses")
plotCourses(LSCB142Courses, TestAxis4, InstructorList)
TestFig4.savefig("LSCB 142 Courses.png")
plt.close(TestFig4)

TestFig4, TestAxis4 = calendarSetup("LSCB144 Courses")
plotCourses(LSCB144Courses, TestAxis4, InstructorList)
TestFig4.savefig("LSCB 144 Courses.png")
plt.close(TestFig4)

TestFig4, TestAxis4 = calendarSetup("LSCB211 Courses")
plotCourses(LSCB211Courses, TestAxis4, InstructorList)
TestFig4.savefig("LSCB 211 Courses.png")
plt.close(TestFig4)

TestFig4, TestAxis4 = calendarSetup("LSCB219 Courses")
plotCourses(LSCB219Courses, TestAxis4, InstructorList)
TestFig4.savefig("LSCB 219 Courses.png")
plt.close(TestFig4)

TestFig4, TestAxis4 = calendarSetup("LSCB225 Courses")
plotCourses(LSCB225Courses, TestAxis4, InstructorList)
TestFig4.savefig("LSCB 225 Courses.png")
plt.close(TestFig4)

TestFig4, TestAxis4 = calendarSetup("LSCB226 Courses")
plotCourses(LSCB226Courses, TestAxis4, InstructorList)
TestFig4.savefig("LSCB 226 Courses.png")
plt.close(TestFig4)

TestFig4, TestAxis4 = calendarSetup("LSCB237 Courses")
plotCourses(LSCB237Courses, TestAxis4, InstructorList)
TestFig4.savefig("LSCB 237 Courses.png")
plt.close(TestFig4)

TestFig4, TestAxis4 = calendarSetup("LSCB240 Courses")
plotCourses(LSCB240Courses, TestAxis4, InstructorList)
TestFig4.savefig("LSCB 240 Courses.png")
plt.close(TestFig4)

TestFig4, TestAxis4 = calendarSetup("LSCB241 Courses")
plotCourses(LSCB241Courses, TestAxis4, InstructorList)
TestFig4.savefig("LSCB 241 Courses.png")
plt.close(TestFig4)


TestFig4, TestAxis4 = calendarSetup("LSLH3 Courses")
plotCourses(LSLH3Courses, TestAxis4, InstructorList)
TestFig4.savefig("LSLH 3 Courses.png")
plt.close(TestFig4)


for Instructor in InstructorList:
    shortInstructor = Instructor.split(",")[0]
    tempList = []
    for record in classList:
        if (Instructor == record.Instructor):
            tempList.append(record)
    TestFig4, TestAxis4 = calendarSetup(shortInstructor + " Courses")
    plotCourses(tempList, TestAxis4, InstructorList)
    TestFig4.savefig(shortInstructor+"Courses.png")
    plt.close(TestFig4)
    

#plt.show()
