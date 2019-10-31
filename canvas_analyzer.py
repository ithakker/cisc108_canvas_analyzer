"""
Project 4C
Canvas Analyzer
CISC108 Honors
Fall 2019

Access the Canvas Learning Management System and process learning analytics.

Edit this file to implement the project.
To test your current solution, run the `test_my_solution.py` file.
Refer to the instructions on Canvas for more information.

"I have neither given nor received help on this assignment."
author: Ishaan Thakker
"""
__version__ = 7

# 1) main
import canvas_requests
import matplotlib.pyplot as plt
import datetime
def main(user_name):
    user = canvas_requests.get_user(user_name)
    print_user_info(user)
    courses = canvas_requests.get_courses(user_name)
    courses = filter_available_courses(courses)
    print_courses(courses)
    course_ids = get_course_ids(courses)
    course_id = choose_course(course_ids)
    submissions = canvas_requests.get_submissions(user_name, course_id)
    summarize_points(submissions)
    summarize_groups(submissions)
    plot_scores(submissions)
    plot_grade_trends(submissions)


# 2) print_user_info
def print_user_info(user):
    print("Name: " + user["name"])
    print("Title: " + user["title"])
    print("Primary Email: " + user["primary_email"])
    print("Bio: " + user["bio"])

user = {"Name": "Hermione Granger",
            "Title": "Student",
            "Primary Email": "hgranger@hogwarts.edu",
            "Bio": "Interested in Magic, Learning, and House Elf Rights"}

# 3) filter_available_courses
def filter_available_courses(courses: [dict])->[dict]:
    new = []
    for course in courses:
        if course["workflow_state"] == "available":
            new.append(course)
    return new
# 4) print_courses
def print_courses(courses: [dict])->str:
    for course in courses:
        print("\t", course["id"], ":", course["name"])


# 5) get_course_ids
def get_course_ids(courses: [dict])->[int]:
    course_ids = []
    for course in courses:
        course_ids.append(course["id"])
    return course_ids


# 6) choose_course
numbers=[52,15,23,24]
def choose_course(numbers: [int])->int:
    value=input("Enter course id: ")
    value=int(value)
    while value not in numbers:
        value=int(input("Enter a course id: "))
    return value
# 7) summarize_points
def summarize_points(submissions: [dict]):
    possible = 0
    score = 0
    for submission in submissions:
        if submission["score"] is not None:
            points_possible = submission["assignment"]["points_possible"]
            group_weight = submission["assignment"]["group"]["group_weight"]
            possible += points_possible * group_weight
            score += submission["score"] * group_weight
    print("Points possible so far: " , possible)
    print("Points obtained: " , score)
    print("Current grade: " , round(100 * score/possible))



# 8) summarize_groups
def summarize_groups(submissions: [dict]):
    group_score = {}
    group_points = {}
    for submission in submissions:
        if submission["score"] is not None:
            group_name = submission["assignment"]["group"]["name"]
            if group_name not in group_score:
                group_score[group_name] = 0
                group_points[group_name] = 0
            group_score[group_name] += submission["score"]
            group_points[group_name] += submission["assignment"]["points_possible"]
    for name in group_score:
        score, points = group_score[name], group_points[name]
        print("*", name, ":", round(100 * score/points))

# 9) plot_scores
def plot_scores(submissions: [dict]):
    percent_of_scores = []
    for submission in submissions:
        if submission["assignment"]["points_possible"] and submission["score"] != None:
            percent_of_score = 100 * submission["score"] / submission["assignment"]["points_possible"]
            percent_of_scores.append(percent_of_score)
    plt.hist(percent_of_scores)
    plt.title("Distribution of Grades")
    plt.xlabel("Grades")
    plt.ylabel("Number of Assignments")
    plt.show()

def parse_date(date):
    return datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")



# 10) plot_grade_trends
def plot_grade_trends(submissions):
    weighted_score = 0
    max_weighted_score = 0
    ungraded_max = 0
    running_low = []
    running_high = []
    running_max = []
    for submission in submissions:
        weighted_modifier = submission["assignment"]["group"]["group_weight"]
        score = 0
        if submission["score"]:
            score = submission["score"]
        weighted_score += score * weighted_modifier
        points_possible = submission["assignment"]["points_possible"]
        if not submission["graded_at"]:
            ungraded_max += points_possible * weighted_modifier
        else:
            ungraded_max += score * weighted_modifier
        max_weighted_score += points_possible * weighted_modifier
        running_low.append(100 * weighted_score)
        running_max.append(100 * max_weighted_score)
        running_high.append(100 * ungraded_max)
    print(running_max)
    print(max_weighted_score)
    running_high = [s / max_weighted_score for s in running_high]
    running_low = [s / max_weighted_score for s in running_low]
    running_max = [s / max_weighted_score for s in running_max]
    running_dates = []
    for submission in submissions:
        running_dates.append(parse_date(submission["assignment"]["due_at"]))
    plt.plot(running_dates, running_high, label="Highest", linestyle="--")
    plt.plot(running_dates, running_low, label="Lowest", linestyle="--")
    plt.plot(running_dates, running_max, label="Maximum")
    plt.title("Grade Trend")
    plt.ylabel("Grade")
    plt.show()





# Keep any function tests inside this IF statement to ensure
# that your `test_my_solution.py` does not execute it.
if __name__ == "__main__":
    main('hermione')
    # main('ron')
    # main('harry')
    
    # https://community.canvaslms.com/docs/DOC-10806-4214724194
    # main('YOUR OWN CANVAS TOKEN (You know, if you want)')