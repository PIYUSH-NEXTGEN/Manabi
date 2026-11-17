"""Seed the 22 Web Dev hackathon briefs from webdev_projects.md.

Thirteen hackathon projects already exist as resume briefs. Their curated
summaries, approaches, and build guides are reused here so the two tracks do
not drift. Each row gets a hackathon-specific team plan and pitch kit.
"""

from copy import deepcopy

from app.seed.runner import seed_problems
from app.seed.seed_webdev_projects import PROBLEMS as RESUME_PROBLEMS
from app.seed.webdev_hackathon_details import NEW_PROJECTS
from app.seed.webdev_hackathon_kits import KITS
from app.seed.webdev_plain import apply_plain_language


# Project numbers match the section numbers in webdev_projects.md. The list is
# the hackathon table in the same order.
PROJECT_NUMBERS = [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    10,
    11,
    12,
    13,
    14,
    15,
    19,
    22,
    27,
    28,
    29,
    31,
    32,
    33,
]

RESUME_TITLES = {
    1: "Offline-First Field Data Collection PWA with Conflict-Free Sync",
    2: "Civic Issue Tracker with Duplicate Detection",
    4: "Open-Source Contribution Finder",
    5: "Disaster Response Resource Coordination Hub",
    6: "Export Readiness Assistant for Small Businesses",
    10: "Universal QR Payment Router",
    11: "Click-and-Collect Shopping Platform with Live In-Store Inventory",
    14: "Paperless Scholarship Disbursement System",
    27: "Satellite Pass Predictor & Live Sky Tracker",
    28: "Mission Trajectory Playground",
    29: "Molecule Explorer & Drug-Likeness Checker",
    31: "Epidemic Spread Simulator on Contact Networks",
    32: "Quantum Tunneling Lab",
}

_RESUME_BY_TITLE = {problem["title"]: problem for problem in RESUME_PROBLEMS}

# The resume summaries explain a long build. Hackathon readers need a short,
# plain-language statement they can scan before joining a team. Keys follow
# the order of PROJECT_NUMBERS.
PROBLEM_STATEMENTS_BY_POSITION = {
    1: (
        "Build a mobile-friendly web app for field teams who often work "
        "without internet. They should be able to fill forms, add photos and "
        "mark GPS points offline, then sync everything when the connection "
        "returns.\n\n"
        "The hard part is handling two people editing the same record without "
        "losing either person's work."
    ),
    2: (
        "Build a public website where residents report local problems like "
        "potholes, broken streetlights or missed garbage pickup. Each report "
        "includes a photo and location, and similar reports are grouped so "
        "staff see one real issue instead of many duplicates.\n\n"
        "Staff can assign the issue, track a service deadline and update its "
        "status."
    ),
    3: (
        "Build a platform where people swap skills instead of money. Each "
        "person lists what they can teach and what they want to learn, and "
        "the app finds a fair match, schedules a session and collects "
        "feedback after it ends.\n\n"
        "Two-way swaps should work first, with a small number of three-way "
        "swaps when no direct pair exists."
    ),
    4: (
        "Build a search tool that helps new developers find a good first "
        "open-source issue. It should filter GitHub issues by language and "
        "topic, then explain why a repository is beginner-friendly.\n\n"
        "Use signals like recent activity, a contribution guide and how "
        "quickly maintainers respond, and show the reason behind every score."
    ),
    5: (
        "Build a shared board where disaster responders and community "
        "members post needs and offers such as food, water, shelter, medical "
        "help or transport. The app should match nearby needs with offers "
        "and keep a clear record of what was delivered.\n\n"
        "It should still work when the network drops, and contact details "
        "should only be visible to the people who need them."
    ),
    6: (
        "Build a guided tool that helps a small business prepare its first "
        "export. The user chooses a product and a country, and the app shows "
        "a checklist of documents, rules and duties.\n\n"
        "Every item should link to an official source and show the date it "
        "was last checked, so the user can trust what they see."
    ),
    7: (
        "Build one simple workspace for a small nonprofit to manage "
        "volunteers, shifts, donors, pledges, receipts and the people it "
        "serves. Staff, volunteers and finance should each see only what "
        "their role allows.\n\n"
        "The app should also produce a basic impact report from the work "
        "that was actually recorded."
    ),
    8: (
        "Build a dashboard that turns a nonprofit's CSV program data into "
        "clear impact numbers, trends and a map of underserved areas. The "
        "goal is to help a small team decide where to spend limited "
        "resources without hiring a data analyst.\n\n"
        "Show data quality and coverage beside every conclusion so the team "
        "knows how much to trust it."
    ),
    9: (
        "Build a web app that reads a payment QR code, identifies its format "
        "and sends the user to the right payment app or a clearly labelled "
        "sandbox checkout. It should show the parsed merchant, amount and "
        "currency before routing.\n\n"
        "Never store real card data, and reject broken or ambiguous codes "
        "with a clear reason."
    ),
    10: (
        "Build an online catalogue where shoppers can see which local store "
        "has an item in stock, reserve it and pick it up in person. Store "
        "staff should be able to update stock quickly by scanning a barcode.\n\n"
        "The main challenge is keeping online stock accurate when two "
        "shoppers try to reserve the last unit at the same time."
    ),
    11: (
        "Build an online store that shows an environmental score for each "
        "product and suggests greener alternatives. It should also estimate "
        "the carbon footprint of a cart and flag sustainable packaging.\n\n"
        "Be honest when data is missing or uncertain, and explain where each "
        "score comes from."
    ),
    12: (
        "Build an interactive map that lets non-experts compare NASA "
        "satellite images of the same place over time. Add a time slider and "
        "a side-by-side comparison so change is easy to see.\n\n"
        "Write short plain-language notes that explain what each layer shows "
        "and what it cannot show."
    ),
    13: (
        "Build a secure portal where students submit scholarship "
        "applications and staff review, approve and record payments. Every "
        "step must be limited to the right role and saved in an audit trail.\n\n"
        "Students should see their own status and any rejection reason "
        "without having to email the office."
    ),
    14: (
        "Build an app that lets a traveller share a live trip with trusted "
        "contacts for a limited time. Contacts should be alerted if the "
        "traveller leaves the expected route, stops for too long or misses a "
        "check-in.\n\n"
        "The traveller must be able to stop sharing immediately, and "
        "location history should be deleted when the share expires."
    ),
    15: (
        "Build a shared pixel canvas where many people can place pixels in "
        "real time. Add a cooldown timer, abuse limits, live cursors and a "
        "replay of the canvas history.\n\n"
        "The server should be the source of truth so every pixel can be "
        "explained and abusive art can be moderated."
    ),
    16: (
        "Build a browser app that uses a webcam to measure how much a crowd "
        "is moving, then changes the music and visuals based on that energy. "
        "Process frames locally and do not use face recognition.\n\n"
        "Show a clear panel that explains the measured energy and why the "
        "music changed."
    ),
    17: (
        "Build a browser tool that tells a user when bright satellites like "
        "the ISS will pass overhead. It should show only passes the user can "
        "actually see, draw the path on a globe and sky chart, and display "
        "how old the orbital data is.\n\n"
        "Explain why a high pass can still be invisible if the observer or "
        "the satellite is in daylight."
    ),
    18: (
        "Build an interactive sandbox for comparing spacecraft transfers "
        "between orbits. The user should see the fuel cost of each burn and "
        "watch the chosen path run through a real physics simulation.\n\n"
        "Show simulation error and assumptions so the result is educational, "
        "not just a nice animation."
    ),
    19: (
        "Build a browser tool where a user enters or draws a molecule and "
        "sees it in 3D. It should calculate basic drug-likeness properties "
        "locally using a real chemistry library.\n\n"
        "Explain each Lipinski rule in plain language instead of just "
        "showing pass or fail."
    ),
    20: (
        "Build an educational simulator that spreads a disease through a "
        "network of households, schools and workplaces. Users should be able "
        "to add interventions like vaccination or school closure and see how "
        "the outbreak changes.\n\n"
        "Compare the result with a simple model and keep the assumptions "
        "visible so nobody mistakes it for a real forecast."
    ),
    21: (
        "Build an interactive lab where a user draws a potential barrier and "
        "launches a wave packet at it. The app should animate the wave, "
        "calculate how much tunnels through and show the reflected part.\n\n"
        "Compare the result with the known answer for a simple barrier and "
        "warn when the simulation is outside tolerance."
    ),
    22: (
        "Build an earthquake map from live USGS data with filters for "
        "region, time, depth and magnitude. Add a statistics view that "
        "estimates the Gutenberg-Richter b-value and shows its uncertainty.\n\n"
        "Warn when the data is too incomplete or too small to trust, and "
        "show the data timestamp beside every result."
    ),
}

PROBLEM_STATEMENTS = {
    project_number: PROBLEM_STATEMENTS_BY_POSITION[position]
    for position, project_number in enumerate(PROJECT_NUMBERS, start=1)
}


def _base_problem(number: int) -> dict:
    if number in NEW_PROJECTS:
        return deepcopy(NEW_PROJECTS[number])

    problem = deepcopy(_RESUME_BY_TITLE[RESUME_TITLES[number]])
    problem.pop("resume_kit", None)
    return problem


def _compose(number: int) -> dict:
    problem = _base_problem(number)
    problem["source_id"] = f"manabi-web-hackathon-{PROJECT_NUMBERS.index(number) + 1:03d}"
    problem["goal"] = "hackathon"
    problem["summary"] = PROBLEM_STATEMENTS[number]
    problem["source_note"] = "Curated web development hackathon brief."
    problem["team_plan"] = deepcopy(KITS[number]["team_plan"])
    problem["pitch_guide"] = deepcopy(KITS[number]["pitch_guide"])
    return problem


PROBLEMS = apply_plain_language(
    [_compose(number) for number in PROJECT_NUMBERS]
)


if __name__ == "__main__":
    import sys

    seed_problems(PROBLEMS, update="--update" in sys.argv)
