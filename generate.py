import sys
import copy
import random

from courseassignment import *


class AssignmentCreator():
    def __init__(self, courseassignment):
        """Creates Domains Assigning each Faculty to Courses in there Preferences."""
        self.courseassignment = courseassignment
        self.domains = {
            faculty: {
                course
                for course in faculty.preferences.copy()
            }
            for faculty in self.courseassignment.faculty_list
        }
        self.backtrack_count = 0
    
    def save(self, assignment, filename):
        """Outputs the Assignment onto a Text File."""
        with open(filename, "a") as file:  # Use "a" for append mode
            for faculty in assignment:
                file.write(f"Faculty {faculty.faculty_id} {faculty.max_load}: ")
                for course_dict in assignment[faculty]:
                    course, load = list(course_dict.keys())[0], list(course_dict.values())[0]
                    file.write(f"{faculty.preferences[course]}, {course} -> {load}, ")
                file.write("\n")
            file.write(f"{self.backtrack_count}\n")
     
    def solve(self):
        return self.backtrack(dict())

    def available_load(self, faculty, assignment):
        """Returns the Current Available Course Load for Every Faculty."""
        load_available = faculty.max_load
        for course in assignment[faculty]:
            load_available -= sum(list(course.values()))

        return load_available

    def course_load(self, course, assignment):
        """Returns the Amount of Course Load Already Assigned."""
        load = 0
        for faculty in assignment:
            for courses in assignment[faculty]:
                if course in list(courses.keys()):
                    load += courses[course]

        return load

    def select_unassigned_faculty(self, assignment):
        """Returns Faculty that are Unassigned or not Fully Assigned."""
        unassigned_faculty = None
    
        for faculty in random.sample(list(self.domains), len(self.domains)):
        #for faculty in self.domains:
            if faculty not in assignment:
                if unassigned_faculty is None:
                    unassigned_faculty = faculty
                    break
                else:
                    if len(self.courseassignment.neighbors(faculty)) > len(self.courseassignment.neighbors(unassigned_faculty)):
                        unassigned_faculty = faculty
                        break
            else:
                load_available = self.available_load(faculty, assignment)
                if load_available >= 0.5:
                    if unassigned_faculty is None:
                        unassigned_faculty = faculty
                        break
                    else:
                        if len(self.courseassignment.neighbors(faculty)) > len(self.courseassignment.neighbors(unassigned_faculty)):
                            unassigned_faculty = faculty
                            break
        
        return unassigned_faculty

    def backtrack(self, assignment):
        """Recursively Checks and Assigns possible Courses to Faculties."""
        all_faculties_assigned = all(
            faculty in assignment and abs(self.available_load(faculty, assignment)) < 1e-10
            for faculty in self.domains
        )
        if all_faculties_assigned:
            return assignment
        
        faculty = self.select_unassigned_faculty(assignment)
        if faculty is not None:
            for course in faculty.preferences:
                if self.course_load(course, assignment) < 1:
                    new_assignment = assignment.copy()
                    
                    if faculty not in new_assignment:
                        new_assignment[faculty] = []
                        
                    if self.available_load(faculty, new_assignment) != 0:
                        if self.course_load(course, assignment) == 0.5:
                            new_assignment[faculty].append({course: 0.5})
                        else:
                            new_assignment[faculty].append({course: min(1, self.available_load(faculty, new_assignment))})
                    else:
                        break
                        
                    result = self.backtrack(new_assignment)
                    if result is not None:
                        return result
        self.backtrack_count += 1
        return None
        

def main():

    if len(sys.argv) != 3:
        sys.exit("Usage: python3 generate.py preferences [output]")

    preferences_file = sys.argv[1]
    output = sys.argv[2]

    courseassignment = Courseassignment(preferences_file)
    assignmentcreator = AssignmentCreator(courseassignment)
    assignment = assignmentcreator.solve()

    if assignment is None:
        print("No Possible Assignment.")
    else:
        assignmentcreator.save(assignment, output)


if __name__ == "__main__":
    main()