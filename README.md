# Faculty-Course-Optimization-System-FCOS-

An intelligent system for solving the complex problem of assigning courses to university faculty members. FCOS uses a graph-optimization-based approach to create fair and balanced schedules that respect faculty preferences and departmental constraints.

## 📜 About The Project

In any academic department, assigning courses to faculty is a significant logistical challenge. The process must account for individual teaching loads, course preferences, and the specific needs of the curriculum. FCOS is designed to automate and optimize this process, transforming it from a manual puzzle into a solvable, data-driven problem.

This project models the course assignment task as a **Constraint Satisfaction Problem (CSP)**. It provides a robust and efficient solution by leveraging a backtracking search algorithm enhanced with powerful heuristics and consistency-checking techniques. The primary goal is to maximize the number of courses assigned while aligning with faculty preferences and adhering to all specified rules.

---

## ✨ Key Features

* **Constraint-Based Logic:** Ensures that every assignment respects the predefined rules, including faculty course loads and preference lists.
* **Flexible Course Sharing:** A course can be assigned to a single faculty member (1.0 load) or shared between two (0.5 load each), allowing for more versatile scheduling solutions.
* **Advanced Backtracking Algorithm:** Employs a sophisticated backtracking search to navigate the complex space of possible assignments and find a valid solution.
* **Intelligent Heuristics:** Utilizes **Minimum Remaining Values (MRV)** and **Degree** heuristics to prioritize assignments, drastically improving search efficiency.
* **Consistency Enforcement:** Implements **Node Consistency** and **Arc Consistency** to prune the search space, reducing computation time and preventing dead-ends.
* **Automated Test Data Generation:** Includes scripts to generate realistic faculty data and preference lists, facilitating robust testing and validation.

---

## ⚙️ How It Works: The Methodology

FCOS tackles the assignment problem by defining it as a Constraint Satisfaction Problem (CSP) with the following components:

* **Variables:** The faculty members who need course assignments.
* **Domains:** The set of preferred courses for each faculty member.
* **Constraints:** The rules that govern a valid assignment:
    1.  A faculty member can only be assigned a course from their preference list.
    2.  The total load of assigned courses cannot exceed the faculty member's maximum load, which is determined by their category (`x1`: 0.5, `x2`: 1.0, `x3`: 1.5).

The system uses an optimized backtracking algorithm to find a solution that satisfies all constraints.

1.  **Selection:** The algorithm selects an unassigned faculty member, prioritizing those with the fewest remaining course options (MRV heuristic).
2.  **Assignment:** It attempts to assign a course from the faculty's preference list.
3.  **Consistency Check:** After each potential assignment, the system enforces arc consistency. This means it updates the domains of "neighboring" faculty (those who also have the assigned course in their preferences) to reflect the new state. This pruning step is critical for efficiency.
4.  **Recursion & Backtracking:** If an assignment is consistent, the algorithm moves to the next faculty member. If it leads to a dead-end where no valid assignment can be made, it **backtracks** to the previous step and tries a different course.
5.  **Recalibration:** To avoid getting stuck in computationally expensive search paths, the algorithm will restart the search process if the backtrack count exceeds a certain threshold (e.g., 100,000 attempts), often finding a solution much faster on the subsequent run.

---

## 💻 System Requirements

* Python 3.x

---

## 🚀 Getting Started

Follow these steps to get the project running on your local machine.

1.  **Clone the Repository**
    ```sh
    git clone [https://github.com/your-username/Faculty-Course-Optimization-System-FCOS-.git](https://github.com/your-username/Faculty-Course-Optimization-System-FCOS-.git)
    cd Faculty-Course-Optimization-System-FCOS-
    ```

2.  **Ensure Files are in Place**
    The project requires the following files to be in the root directory:
    * `generateV2.py` (the main solver)
    * `courseassignment.py`
    * `FD.csv` (list of First Degree courses)
    * `HD.csv` (list of Higher Degree courses)
    * An input CSV with faculty preferences (e.g., `50_Faculty.csv`).

---

## ▶️ How to Run the System

Execute the main solver from your terminal. The script requires two arguments: the path to the input faculty data file and a name for the output file where the results will be saved.

**Command:**
```sh
python3 generateV2.py <path_to_input_data.csv> <output_file.txt>
```

**Example:**
```sh
python3 generateV2.py 50_Faculty.csv assignment_results.txt
```

The system will then process the data and write the complete, valid course assignment to `assignment_results.txt`. If no solution can be found, it will report "No Possible Assignment."

---

## 📂 File Descriptions

* `generateV2.py`: The main executable script. It contains the advanced backtracking solver with node and arc consistency.
* `generate.py`: A simpler version of the solver with a basic backtracking implementation.
* `courseassignment.py`: A helper script that defines the classes and data structures for `CourseAssignmentVariable` (faculty) and `Courseassignment` (the overall problem structure).
* `Subjects_generator.py`: A script to generate a pool of courses needed for a given number of faculty.
* `preference_assignment.py`: A script that uses `Subjects_generator.py` to create a complete faculty preference CSV file for testing.
* `FD.csv` / `HD.csv`: Data files containing lists of First Degree and Higher Degree courses, respectively.
* `50_Faculty.csv`: An example input file containing preference data for 50 faculty members.
* `Graph_Optimization_240909_154212.pdf`: The detailed research paper and report for this project.

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## ✍️ Authors

* **Alankrit Singh**
* **Divyanshu Singh**
* **Aman Sisodiya**
* **Manan Jain**
