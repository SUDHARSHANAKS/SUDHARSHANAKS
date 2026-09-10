import json
import urllib.request
from datetime import datetime

USERNAME = "IswWYKpcly"

QUERY = """
query userProfileCalendar($username: String!, $year: Int) {
    matchedUser(username: $username) {
        userCalendar(year: $year) {
            activeYears
            streak
            totalActiveDays
            submissionCalendar
        }
    }
}
"""

def get_calendar():
    current_year = datetime.now().year

    payload = json.dumps({
        "query": QUERY,
        "variables": {
            "username": USERNAME,
            "year": current_year
        }
    }).encode("utf-8")

    request = urllib.request.Request(
        "https://leetcode.com/graphql",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
    )

    with urllib.request.urlopen(request) as response:
        data = json.loads(response.read().decode("utf-8"))

    return data["data"]["matchedUser"]["userCalendar"]


def generate_svg(calendar):
    submissions = json.loads(calendar["submissionCalendar"])

    width = 900
    height = 180

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{width}" height="{height}" viewBox="0 0 {width} {height}">

<rect width="100%" height="100%" fill="#0d1117"/>

<text x="20" y="30"
font-family="Arial"
font-size="20"
font-weight="bold"
fill="#ffffff">
LeetCode Activity
</text>
'''

    # Calendar configuration
    start_x = 20
    start_y = 50
    cell = 12
    gap = 3

    # Generate 365 days
    from datetime import timedelta

    today = datetime.now().date()
    start_date = today - timedelta(days=364)

    for i in range(365):
        date = start_date + timedelta(days=i)

        timestamp = int(
            datetime(
                date.year,
                date.month,
                date.day
            ).timestamp()
        )

        count = submissions.get(str(timestamp), 0)

        if count == 0:
            color = "#161b22"
        elif count <= 2:
            color = "#0e4429"
        elif count <= 5:
            color = "#006d32"
        elif count <= 10:
            color = "#26a641"
        else:
            color = "#39d353"

        week = i // 7
        day = i % 7

        x = start_x + week * (cell + gap)
        y = start_y + day * (cell + gap)

        svg += f'''
<rect x="{x}" y="{y}"
width="{cell}" height="{cell}"
rx="2"
fill="{color}">
<title>{date}: {count} submissions</title>
</rect>
'''

    svg += "</svg>"

    return svg


calendar = get_calendar()
svg = generate_svg(calendar)

with open("assets/leetcode-activity.svg", "w", encoding="utf-8") as file:
    file.write(svg)

print("LeetCode activity updated successfully!")
print("Active days:", calendar["totalActiveDays"])
print("Current streak:", calendar["streak"])
