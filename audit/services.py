import re

COURSE_REGEX_PATTERN = "([0-9]{2}-[0-9]{3})\s+(\w+)\s+\'([0-9]{2})\s+"\
                       "([\w+|\*])\s+([0-9]+\.[0])"
course_regex = re.compile(COURSE_REGEX_PATTERN)


def parse_audit(audit):
    lines = audit.split("\n")

    courses_taken = []

    for line in lines:
        match = course_regex.search(line)
        if match:
            [course_id, season, year, grade, unit] = match.groups()
            courses_taken.append({
                "course_id": course_id,
                "season": season,
                "year": year,
                "grade": grade,
                "unit": unit
            })

    return courses_taken
