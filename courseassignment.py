import csv
import Subjects_generator


class CourseAssignmentVariable():
    """Creates a Faculty Variable."""
    CATEGORIES = {"x1": {"max_load": 0.5}, "x2": {"max_load": 1}, "x3": {"max_load": 1.5}}

    def __init__(self, faculty_id, category, preferences):
        """Create a new course assignment variable for faculty."""
        self.faculty_id = faculty_id
        self.category = category
        self.max_load = self.CATEGORIES.get(category, {}).get("max_load", 0)
        self.preferences = {}
        self.update_preferences(preferences)

    def __hash__(self):
        return hash((self.faculty_id, self.category, tuple(self.preferences.items())))

    def __eq__(self, other):
        return (
            (self.faculty_id == other.faculty_id) and
            (self.category == other.category) and
            (self.preferences == other.preferences)
        )
        
    def update_preferences(self, preferences):
        """Update preferences based on the input."""
        for key, value in preferences.items():
            if key.startswith("Preference"):
                buffer = key
                key = value
                value = buffer
                self.preferences[key] = value


class Courseassignment():
    """Takes Input from Input CSV File and Creates Objects of CourseAssignmentVariable also defines Overlaps and Neighbors between Faculty Objects."""
    
    def __init__(self, data_file):
        self.faculty_list = []
        self.courses = set()
        with open(data_file, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                faculty = CourseAssignmentVariable(row['FacultyID'], row['Category'], row)
                for i in range(12):
                    self.courses.add(row[f"Preference {i+1}"])
                self.faculty_list.append(faculty)
            
        self.overlaps = dict()
        for v1 in self.faculty_list:
            for v2 in self.faculty_list:
                if v1 == v2:
                    continue
                preferences1 = v1.preferences
                preferences2 = v2.preferences
                intersection = set(preferences1).intersection(preferences2)
                if not intersection:
                    self.overlaps[v1, v2] = None
                else:
                    intersection = intersection.pop()
                    self.overlaps[v1, v2] = intersection

    def neighbors(self, var):
        return set(
            v for v in self.faculty_list
            if v != var and self.overlaps[v, var]
        )