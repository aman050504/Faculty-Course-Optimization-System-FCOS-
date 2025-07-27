import Subjects_generator
import random
import csv


preference_dict = dict()


for faculty_num in range(Subjects_generator.dataset):
    faculty_id = "Faculty" + str(faculty_num+1)
    pref_order = []
    for i in random.sample(Subjects_generator.course_dict["FDCDC"], k = 4):
        pref_order.append(f"FDCDC - {i}")
    for i in (random.sample(Subjects_generator.course_dict["FDELE"], k = 4)):
        pref_order.append(f"FDELE - {i}")
    for i in (random.sample(Subjects_generator.course_dict["HDCDC"], k = 2)):
        pref_order.append(f"HDCDC - {i}")
    for i in (random.sample(Subjects_generator.course_dict["HDELE"], k = 2)):
        pref_order.append(f"HDELE - {i}")
    random.shuffle(pref_order)
    preference_dict[faculty_id] = [Subjects_generator.course[faculty_num], pref_order]


with open("Faculty_data.csv", "w", newline = "") as file:
    writer = csv.writer(file)
    headings = ["FacultyID", "Category", "Preference 1", "Preference 2", "Preference 3", "Preference 4", "Preference 5", "Preference 6", "Preference 7", "Preference 8", "Preference 9", "Preference 10", "Preference 11", "Preference 12"]
    writer.writerow(headings)
    
    for faculty_id, preference_info in preference_dict.items():
        write = [faculty_id, preference_info[0]]
        write.extend(preference_info[1])
        writer.writerow(write)
