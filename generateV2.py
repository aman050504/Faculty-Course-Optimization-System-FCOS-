import sys
from copy import deepcopy
import random

from courseassignment import *


class AssignmentCreator():
    def __init__(self, courseassignment):
        """Creates Domains Assigning each Faculty to Courses and Available Course Load in there Preferences."""
        self.courseassignment = courseassignment
        self.domains = {
            faculty: {
                course: 1
                for course in faculty.preferences.copy()
            }
            for faculty in self.courseassignment.faculty_list
        }
        self.backtrack_count = 0

    def valid_data_check(self):
        """Checks if the Input Data given is Valid or not."""
        total_load = 0
        for faculty in self.courseassignment.faculty_list:
            total_load += faculty.max_load
        if(len(self.courseassignment.courses) != total_load):
            print("Invalid Data")
            return 0
        return 1
        
    def save(self, assignment, filename):
        """Outputs the Assignment onto a Text File."""
        with open(filename, "a") as file:  # Use "a" for append mode
            for faculty in assignment:
                file.write(f"{faculty.faculty_id}, Max Load: {faculty.max_load}, Available Load: {self.available_load(faculty, assignment)}, ")
                for course_dict in assignment[faculty]:
                    course, load = list(course_dict.keys())[0], list(course_dict.values())[0]
                    file.write(f"{faculty.preferences[course]}: {course} -> {load}, ")
                file.write("\n")
            file.write(f"Backtrack Count: {self.backtrack_count}\n\n")

    def solve(self):
        print("Generating Assignment...")
        return self.backtrack(dict(), self.domains)

    def available_load(self, faculty, assignment):
        """Returns the Current Available Course Load for Every Faculty."""
        load_available = faculty.max_load
        for course in assignment[faculty]:
            load_available -= sum(list(course.values()))

        return load_available

    def enforce_node_consistency(self, faculty, course, assignment, domains):
        """Removes the Recently Assigned Course from the Faculty."""
        if course in list(domains[faculty].keys()):
            del domains[faculty][course]

        if self.available_load(faculty, assignment) == 0:
            del domains[faculty]

    def enforce_arc_consistency(self, faculty, course, assignment, domains):
        """Removes or Reduces Course Load from Neighboring Faculties."""
        courses_to_remove = []
        course_load = 0
        for assigned_courses in assignment[faculty]:
            for course_check, course_load_check in assigned_courses.items():
                if course_check == course:
                    course_load = course_load_check
                    
        for neighbor in self.courseassignment.neighbors(faculty):
            if neighbor in domains:
                if course in list(domains[neighbor].keys()):
                    domains[neighbor][course] -= course_load
                    if (domains[neighbor][course] == 0):
                        courses_to_remove.append((neighbor, course))

        for neighbor, course in courses_to_remove:
            if neighbor in domains and course in domains[neighbor]:
                del domains[neighbor][course]
                if not domains[neighbor]:
                    del domains[neighbor]
    
    def select_unassigned_faculty(self, assignment, domains):
        """Returns Faculty that are Unassigned or not Fully Assigned."""
        unassigned_faculty = None
        for faculty in random.sample(list(domains), len(domains)):
            if faculty not in assignment:
                if unassigned_faculty is None or len(domains[faculty]) < len(domains[unassigned_faculty]):
                    unassigned_faculty = faculty
                else:
                    if len(self.courseassignment.neighbors(faculty)) > len(self.courseassignment.neighbors(unassigned_faculty)):
                        unassigned_faculty = faculty
            else:
                load_available = self.available_load(faculty, assignment)
                if load_available >= 0.5:
                    if unassigned_faculty is None or len(domains[faculty]) < len(domains[unassigned_faculty]):
                        unassigned_faculty = faculty
                    else:
                        if len(self.courseassignment.neighbors(faculty)) > len(self.courseassignment.neighbors(unassigned_faculty)):
                            unassigned_faculty = faculty

        return unassigned_faculty

    def backtrack(self, assignment, domains):
        """Recursively Checks and Assigns possible Courses to Faculties."""
        all_faculties_assigned = all(
            faculty in assignment and abs(self.available_load(faculty, assignment)) < 1e-10
            for faculty in self.domains
        )
        if all_faculties_assigned:
            return assignment

        faculty = self.select_unassigned_faculty(assignment, domains)
        if faculty is not None:
            for course, course_load_available in domains[faculty].items():
                if course_load_available > 0:
                    new_assignment = deepcopy(assignment)
                    new_domains = deepcopy(domains)

                    if faculty not in new_assignment:
                        new_assignment[faculty] = []

                    if self.available_load(faculty, new_assignment) != 0:
                        if course_load_available == 0.5:
                            new_assignment[faculty].append({course: 0.5})
                        else:
                            new_assignment[faculty].append({course: min(1, self.available_load(faculty, new_assignment))})
                    else:
                        break

                    self.enforce_arc_consistency(faculty, course, new_assignment, new_domains)
                    self.enforce_node_consistency(faculty, course, new_assignment, new_domains)
                    result = self.backtrack(new_assignment, new_domains)
                    if result is not None:
                        return result
        self.backtrack_count += 1
        if self.backtrack_count % 10000 == 0:
            print(f"Backtrack Count: {self.backtrack_count}")
        if (len(assignment) <= len(self.courseassignment.faculty_list) - 5) or (self.backtrack_count == 100000):
            self.backtrack_count = 0
            print("Recalibrating...")
            return self.backtrack(dict(), self.domains)
        return None
                    

def main():

    if len(sys.argv) != 3:
        sys.exit("Usage: python3 generate.py preferences [output]")

    preferences_file = sys.argv[1]
    output = sys.argv[2]

    courseassignment = Courseassignment(preferences_file)
    assignmentcreator = AssignmentCreator(courseassignment)
    validity_check = assignmentcreator.valid_data_check()
    if validity_check == 0:
        sys.exit()
    assignment = assignmentcreator.solve()

    if assignment is None:
        print("No Possible Assignment.")
    else:
        assignmentcreator.save(assignment, output)


if __name__ == "__main__":
    main()