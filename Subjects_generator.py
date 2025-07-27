import csv
import random

subjects_needed = 0
fd_subjects = []
hd_subjects = []
FD_Final = []
HD_Final = []
dataset = 30

faculty_types = ["x1", "x2", "x3"]

course = random.choices(faculty_types, weights = [0.75, 1, 1.5], cum_weights = None, k=dataset)
if course.count("x1") % 2 != 0:
    course.append("x1")
    course.remove("x2")
if course.count("x3") % 2 != 0:
    course.append("x3")
    course.remove("x2")

subjects_needed = 0.5*course.count("x1") + course.count("x2") + 1.5*course.count("x3")
    
FD_req = subjects_needed * 8/12
HD_req = subjects_needed * 4/12
FD_req = int(FD_req)
HD_req = int(HD_req)
diff = subjects_needed - FD_req - HD_req
FD_req += int(diff)
course_dict = {"FDCDC" : [], "FDELE" : [], "HDCDC" : [], "HDELE" : []}

with open("FD.csv", "r") as file:
    csvreader = csv.reader(file)
    for fd in csvreader:
        fd_subjects.append(fd)

FD_buffer = random.sample(fd_subjects, k = FD_req)

for i in FD_buffer:
    FD_Final.append(f"{i[0]} - {i[1]}")

course_dict["FDCDC"] = random.sample(FD_Final, k = int(FD_req/2))

for i in FD_Final:
    if i not in course_dict["FDCDC"]:
        course_dict["FDELE"].append(i)

with open("HD.csv", "r") as file:
    csvreader = csv.reader(file)
    for hd in csvreader:
        hd_subjects.append(hd)

HD_buffer = random.sample(hd_subjects, k = int(HD_req))

for i in HD_buffer:
    HD_Final.append(f"{i[0]} - {i[1]}")

course_dict["HDCDC"] = random.sample(HD_Final, k = int(HD_req/2))

for i in HD_Final:
    if i not in course_dict["HDCDC"]:
        course_dict["HDELE"].append(i)
