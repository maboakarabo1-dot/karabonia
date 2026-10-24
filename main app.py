"""
Karabonia - your path from study to work (hackathon version, built with Python + Flet)

Seven tools in one app (plus a Jargon Quiz and a 'What is stopping you?' check):
  1. Learn    - plain-language explanations of education and work terms
  2. Path     - pick where you are now and tick off your next steps
  3. Request  - write a professional workplace-placement request
  4. Tracker  - keep track of who you contacted and when to follow up
  5. Ready    - a quick work-readiness check with ONE clear next step
  6. Scam?    - paste a job advert or message and check it for scam warning signs
  7. Profile  - turn skills and informal experience into a credible profile

HOW TO RUN (VS Code terminal):
    flet run counter        <- when this file is counter/src/main.py

IMPORTANT: The explanations and checklists are a first draft written for learning.
Check each one with your college or an official source, and rewrite it in your own
words before you submit. Use fictional examples in your demo, never real private details.
"""
import json
import os
import random

import flet as ft

# ---------------------------------------------------------------------------
# Colours (the Karabonia look)
# ---------------------------------------------------------------------------
DEEP = "#4A1D6B"   # dark purple: headings, gradient start
TEAL = "#C2185B"   # strong pink: buttons, selected items
MINT = "#F8D7E8"   # soft pink: chips, backgrounds
SAND = "#F48FB1"   # medium pink: accents
PLUM = "#7B3FA0"   # purple: accents, gradient end
SOFT = "#FBF5FA"   # near-white pink: page background
INK = "#1F2933"
GREY = "#5B6770"
WHITE = "#FFFFFF"
RED = "#D64545"

# ---------------------------------------------------------------------------
# WELCOME SCREEN CONTENT: edit here later. Add a feature = add one line to WELCOME_POINTS.
# ---------------------------------------------------------------------------
WELCOME_TITLE = "Welcome!"
WELCOME_TAGLINE = "Your path from study to work starts here"
WELCOME_POINTS = [
    (ft.Icons.MENU_BOOK, "Understand education and work jargon in plain language"),
    (ft.Icons.ROUTE, "Find what is stopping you and get your next step"),
    (ft.Icons.EDIT_NOTE, "Write a professional placement request"),
    (ft.Icons.ASSIGNMENT, "Track who you contacted and when to follow up"),
    (ft.Icons.CHECKLIST, "Check how work-ready you are"),
    (ft.Icons.SHIELD, "Spot job scams before they cost you"),
    (ft.Icons.BADGE, "Turn your skills and informal experience into a profile"),
]

LAST_CHECKED = "not yet"  # change this to the date you really check each term with your college

# ---------------------------------------------------------------------------
# Files where the app saves things (no names, ID numbers or passwords)
# ---------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
SUGGESTIONS_FILE = os.path.join(HERE, "suggestions.txt")
COUNTS_FILE = os.path.join(HERE, "search_counts.json")
TRACKER_FILE = os.path.join(HERE, "tracker.json")
PROFILE_FILE = os.path.join(HERE, "profile.json")
WELCOME_IMG = os.path.join(HERE, "assets", "welcome.png")  # optional AI illustration

# ---------------------------------------------------------------------------
# CHECKLISTS shown inside some term cards
# ---------------------------------------------------------------------------
CHECKLISTS = {
    "cv": (
        "CV checklist",
        [
            "Contact details and a professional email address",
            "A 2 to 3 line profile about who you are",
            "Education: qualification, college and year",
            "Workplace training or volunteering",
            "Skills, such as digital and communication",
            "Two references, with their permission",
            "One to two pages, no spelling mistakes, saved as a PDF",
        ],
    ),
    "opportunity": (
        "Is this opportunity real?",
        [
            "Real employers do not ask you to pay to apply or to be interviewed",
            "Check the company on its official website and match the contact details",
            "Be careful with recruiters who only use WhatsApp or free email",
            "Do not send your ID or bank details until you have confirmed the company and role",
            "If it sounds too good to be true, ask your college or someone you trust",
        ],
    ),
    "logbook": (
        "Logbook entry checklist",
        [
            "Write in your own words, not a copy of your task list",
            "Say what you did, what you learned and what you would do better",
            "Add evidence if your college asks for it",
            "Get your supervisor to sign and date regularly",
            "Keep a backup copy or photos of every page",
        ],
    ),
}

# ---------------------------------------------------------------------------
# TERMS. Each card has: group, means, matters, next, ask (what to ask your college).
# Optional: checklist (a key from CHECKLISTS) and source.
# ---------------------------------------------------------------------------
GROUPS = ["Qualifications", "Practical experience", "Finding work", "Skills & business"]

TERMS = {
    # ----- Qualifications -----
    "nated": {
        "group": "Qualifications",
        "means": "Report 191, the older N1 to N6 college programmes that are being replaced by occupational qualifications.",
        "matters": "The final date to complete a National N Diploma is 30 June 2029, so timing matters.",
        "next": "Write down your last registration and completion dates.",
        "ask": "What are my last registration and completion dates?",
        "source": "Source: DHET Government Gazette No. 49518 (N1-N3) and Tshwane North TVET College (2029 date)",
    },
    "national n diploma": {
        "group": "Qualifications",
        "means": "The qualification you receive after passing your N4 to N6 subjects and completing the required workplace experience.",
        "matters": "It is the proof of your qualification when you apply for jobs or further study.",
        "next": "Track your subjects and your workplace hours in one place.",
        "ask": "Exactly what do I still need to receive my diploma?",
    },
    "nqf": {
        "group": "Qualifications",
        "means": "The National Qualifications Framework, which places qualifications in South Africa on levels.",
        "matters": "It helps employers and institutions compare your qualification with others.",
        "next": "Find the NQF level of your qualification and write it on your CV.",
        "ask": "What NQF level is my qualification?",
    },
    "saqa": {
        "group": "Qualifications",
        "means": "The South African Qualifications Authority, which looks after the NQF and helps verify qualifications.",
        "matters": "Employers and institutions may check that your qualification is registered and real.",
        "next": "Keep your certificate and statement of results safe, and know your qualification's official name.",
        "ask": "Is my qualification registered, and what is its official title?",
    },
    "qcto": {
        "group": "Qualifications",
        "means": "The Quality Council for Trades and Occupations, the body that looks after the new occupational qualifications.",
        "matters": "These qualifications are replacing the older NATED programmes at TVET colleges.",
        "next": "Find out which occupational qualification matches your field.",
        "ask": "Which occupational qualification replaces my programme?",
    },
    "statement of results": {
        "group": "Qualifications",
        "means": "An official document that lists your subjects and marks.",
        "matters": "Employers and institutions ask for it as proof of what you passed.",
        "next": "Find out how to get a certified copy and keep a scan.",
        "ask": "How do I get a certified or replacement statement of results?",
    },
    "tvet college": {
        "group": "Qualifications",
        "means": "A Technical and Vocational Education and Training college, a public college that teaches job-focused skills.",
        "matters": "TVET colleges offer N-programmes and occupational qualifications that lead to work.",
        "next": "Visit the student support office if you are unsure about your programme.",
        "ask": "Who can help me with my practical training questions?",
    },
    "nsfas": {
        "group": "Qualifications",
        "means": "The National Student Financial Aid Scheme, which helps eligible students pay for study.",
        "matters": "It can cover fees and costs for students at public universities and TVET colleges.",
        "next": "Check the requirements and deadlines each year and keep your documents ready.",
        "ask": "What are the NSFAS deadlines and documents for my year?",
    },
    # ----- Practical experience -----
    "logbook": {
        "group": "Practical experience",
        "means": "The record of your workplace training, signed and dated by your workplace supervisor.",
        "matters": "Your college checks it to confirm you did the required workplace hours before it gives your diploma.",
        "next": "Make sure every entry is complete, signed and dated.",
        "ask": "What evidence do you accept, and how often must entries be signed?",
        "checklist": "logbook",
    },
    "in-service training": {
        "group": "Practical experience",
        "means": "Workplace experience you must complete, on top of your N-subjects, to earn your National N Diploma.",
        "matters": "Without it, you can finish N6 but still not qualify for the diploma.",
        "next": "Find a placement early, agree the tasks with your supervisor, and start your logbook on day one.",
        "ask": "How much workplace experience do I need, and what counts?",
    },
    "work-integrated learning": {
        "group": "Practical experience",
        "means": "Learning that combines your studies with structured experience in a real workplace. You may see it called WIL.",
        "matters": "Many qualifications need it, and employers value it.",
        "next": "Ask how your qualification organises its workplace learning.",
        "ask": "Does my qualification include WIL, and how is it assessed?",
    },
    "workplace placement": {
        "group": "Practical experience",
        "means": "The organisation where you do your practical training.",
        "matters": "You often have to find it yourself, and it must be approved by your college.",
        "next": "Make a list of organisations in your field, then use the Request tab to write to them.",
        "ask": "What makes a workplace acceptable for my practical training?",
    },
    "weekly summary": {
        "group": "Practical experience",
        "means": "A short write-up, in your own words, of what you did and learned during the week.",
        "matters": "Evaluators want a clear story of your learning, not a copy of your task list.",
        "next": "Write what you did, what you learned and one thing you would do better.",
        "ask": "Can I see an example of a good weekly summary?",
    },
    "evidence": {
        "group": "Practical experience",
        "means": "Proof of your work, such as signed forms, documents or photos, if your college asks for it.",
        "matters": "It backs up what you wrote in your logbook.",
        "next": "Keep copies as you go instead of collecting them at the end.",
        "ask": "Which evidence do you accept?",
    },
    "supervisor sign-off": {
        "group": "Practical experience",
        "means": "Your workplace supervisor signing to confirm that your logbook entries are true.",
        "matters": "Unsigned entries may not be accepted.",
        "next": "Get entries signed and dated regularly, not all at the end.",
        "ask": "Who may sign as my supervisor, and what must they write?",
    },
    "internship": {
        "group": "Practical experience",
        "means": "A period of workplace experience, usually for a graduate or student, to learn on the job.",
        "matters": "It helps you get the experience many employers ask for.",
        "next": "Apply early, tailor your CV, and check the opportunity is real.",
        "ask": "Does an internship count towards my qualification?",
        "checklist": "opportunity",
    },
    "learnership": {
        "group": "Practical experience",
        "means": "A structured programme that combines classroom learning with paid work experience at a company.",
        "matters": "It can lead to a qualification and often to a job.",
        "next": "Look for learnerships advertised by companies and SETAs, and prepare your CV and ID documents.",
        "ask": "Can a learnership replace or count towards my practical training?",
        "checklist": "opportunity",
    },
    "seta": {
        "group": "Practical experience",
        "means": "A Sector Education and Training Authority, which oversees skills training in a particular industry.",
        "matters": "SETAs often fund and advertise learnerships and skills programmes.",
        "next": "Find the SETA linked to your field and check its website for opportunities.",
        "ask": "Which SETA is linked to my qualification?",
    },
    # ----- Finding work -----
    "cv": {
        "group": "Finding work",
        "means": "A short document that lists your education, skills and work experience.",
        "matters": "It is usually the first thing an employer reads when you apply.",
        "next": "Keep it to one or two pages and add your workplace training.",
        "ask": "Does the college offer help with CVs?",
        "checklist": "cv",
    },
    "cover letter": {
        "group": "Finding work",
        "means": "A short letter that introduces you and explains why you are right for a role.",
        "matters": "It shows you read the advert and care about the job.",
        "next": "Write three short paragraphs: who you are, why this job, and how to reach you.",
        "ask": "Can someone check my cover letter?",
    },
    "vacancy": {
        "group": "Finding work",
        "means": "An open job or opportunity that an organisation has advertised.",
        "matters": "Reading it carefully shows you what the employer really wants.",
        "next": "Check the requirements and the closing date before you apply.",
        "ask": "Where does the college advertise vacancies?",
        "checklist": "opportunity",
    },
    "reference": {
        "group": "Finding work",
        "means": "A person, such as a lecturer or supervisor, who can confirm your character or work.",
        "matters": "Employers often phone or email your references before they decide.",
        "next": "Ask permission first, then give each person your CV and the role you are applying for.",
        "ask": "Will a lecturer or supervisor act as my reference?",
    },
    "interview": {
        "group": "Finding work",
        "means": "A conversation where an employer learns about you and decides if you fit the role.",
        "matters": "Preparation can make the difference between an offer and no reply.",
        "next": "Practise answering: tell me about yourself, why this job, and a time you solved a problem.",
        "ask": "Does the college run interview practice?",
    },
    # ----- Skills & business -----
    "transferable skills": {
        "group": "Skills & business",
        "means": "Skills that are useful in many jobs, such as communication, teamwork and problem-solving.",
        "matters": "They help you when you have little work experience.",
        "next": "Write down three examples of when you used each skill.",
        "ask": "Which skills did my practical training build?",
    },
    "portfolio": {
        "group": "Skills & business",
        "means": "A collection of your work, certificates and evidence that shows what you can do.",
        "matters": "It proves your skills when you have no long work history.",
        "next": "Save your best work, certificates and logbook evidence in one folder.",
        "ask": "What can I put in my portfolio from my studies?",
    },
    "business plan": {
        "group": "Skills & business",
        "means": "A document that explains your business idea, your customers, your costs and how you will earn.",
        "matters": "It helps you think clearly and ask for support or funding.",
        "next": "Start with one page: the idea, who will buy, what it costs, and how much you will charge.",
        "ask": "Is there a youth business support programme near me?",
    },
}

# ---------------------------------------------------------------------------
# MORE TERMS (same format). Add, change or delete any of these.
# ---------------------------------------------------------------------------
def _t(group, means, matters, nxt, ask):
    return {"group": group, "means": means, "matters": matters, "next": nxt, "ask": ask}


Q, P, F, S = "Qualifications", "Practical experience", "Finding work", "Skills & business"

TERMS.update({
    # ----- Qualifications -----
    "n4 to n6": _t(Q,
        "The three advanced levels of the older NATED programmes at TVET colleges, with N6 the highest.",
        "Passing your N4 to N6 subjects is the study part of the National N Diploma.",
        "Keep every statement of results and note which level you are on.",
        "Which subjects do I still need to pass at my level?"),
    "occupational qualification": _t(Q,
        "A qualification designed with industry that combines theory, practical skills and workplace learning.",
        "These qualifications are replacing the older NATED programmes.",
        "Find out which one matches your field.",
        "Which occupational qualification matches my programme, and when can I start it?"),
    "certificate": _t(Q,
        "A document that shows you completed a course or qualification.",
        "Employers and colleges ask for it as proof.",
        "Keep the original safe and make certified copies.",
        "How do I get a certified copy or a replacement if I lose my certificate?"),
    "qualification requirements": _t(Q,
        "Everything you must complete to earn a qualification, such as subjects, marks, practical hours and workplace experience.",
        "Missing one requirement can delay your certificate.",
        "Ask for the full list in writing and tick each item off.",
        "Can I get a list of everything I still need to complete my qualification?"),
    # ----- Practical experience -----
    "workplace experience": _t(P,
        "Time spent working in a real workplace to practise what you studied.",
        "Many qualifications and employers need it.",
        "Look for placements, internships, learnerships or volunteering, and keep records of your hours.",
        "What counts as workplace experience for my qualification?"),
    "apprenticeship": _t(P,
        "A way to learn a trade by working under an experienced person while you study, ending with a trade test.",
        "It leads to a recognised trade qualification.",
        "Look at employers and SETAs that offer apprenticeships in your trade.",
        "Does the college link students to apprenticeships?"),
    "volunteering": _t(P,
        "Working without pay to help an organisation or your community.",
        "It builds skills, references and experience while you look for work.",
        "Pick an organisation near you, agree what you will do, and ask for a reference letter.",
        "Can volunteering count towards my practical requirements?"),
    "workplace supervisor": _t(P,
        "The person at your workplace who guides you and signs your logbook.",
        "Their signature confirms your hours and tasks.",
        "Agree your tasks and a regular sign-off day in your first week.",
        "What must my supervisor include when they sign my logbook?"),
    # ----- Finding work -----
    "eligibility criteria": _t(F,
        "The requirements you must meet to apply, such as qualifications, experience or location.",
        "Applications that do not meet them are usually rejected.",
        "Read the advert and tick off each requirement before you apply.",
        "Can the college career office help me check whether I qualify for this vacancy?"),
    "application deadline": _t(F,
        "The last date and time an employer accepts applications.",
        "Late applications are usually not considered.",
        "Put the date in your phone calendar and apply a few days early.",
        "Does the college share vacancy closing dates?"),
    "shortlisting": _t(F,
        "When an employer picks the applicants it will interview from everyone who applied.",
        "A CV that matches the advert helps you get shortlisted.",
        "Match your CV and cover letter to the requirements in the advert.",
        "Can someone at the college review my CV before I apply?"),
    "entry-level job": _t(F,
        "A job that does not need much previous work experience.",
        "It is a common first step into a career.",
        "Search for entry-level or junior roles and apply every week.",
        "Does the college career office list entry-level jobs?"),
    "application follow-up": _t(F,
        "Contacting an employer after you apply to confirm they received it and to show you are interested.",
        "It shows you are serious and can keep you in mind.",
        "Wait about a week, then send a short, polite email or call.",
        "Does the college have tips for following up on applications?"),
    # ----- Skills & business -----
    "digital literacy": _t(S,
        "Being able to use computers, email, the internet and apps with confidence.",
        "Most applications and jobs need it.",
        "Practise email, documents and online forms.",
        "Does the college offer computer or digital skills training?"),
    "communication skills": _t(S,
        "Speaking, listening and writing clearly so that people understand you.",
        "Employers look for them in every kind of job.",
        "Practise explaining your studies in 30 seconds and write clear, short emails.",
        "Does the college run communication or presentation workshops?"),
    "problem-solving": _t(S,
        "Finding practical solutions when something goes wrong.",
        "It shows employers you can work without constant help.",
        "Write down one problem you solved at placement and how you did it.",
        "Does the college career office help students describe their skills?"),
    "teamwork": _t(S,
        "Working with others to reach a shared goal.",
        "Most workplaces depend on it.",
        "Think of an example from school, church or a community project.",
        "Does the college career office help students describe their skills?"),
    "time management": _t(S,
        "Planning your time so that tasks are finished on time.",
        "Missed deadlines hurt applications and workplace training.",
        "Use a weekly planner and put every deadline in your phone.",
        "Does the college offer study or time-management support?"),
    "networking": _t(S,
        "Building contacts who can share advice and opportunities.",
        "Many placements and jobs come through people you know.",
        "Tell lecturers, family and past supervisors what work you are looking for.",
        "Does the college have employer contacts or career events?"),
    "workplace readiness": _t(S,
        "Having the skills, documents and habits an employer expects from a new worker.",
        "It is what the Ready check in this app measures.",
        "Take the Ready check and work on your first next step.",
        "Which work-readiness programmes does the college offer?"),
    "upskilling": _t(S,
        "Learning new skills to improve your job chances.",
        "Short courses can add to your CV while you look for work.",
        "Pick one skill and finish one short course.",
        "Does the college offer short courses or link to free ones?"),
    "entrepreneurship": _t(S,
        "Starting and running your own business.",
        "It can create income when jobs are hard to find.",
        "Write your idea in one sentence and test it with a small first sale.",
        "Does the college or a youth agency offer business support?"),
    "business idea": _t(S,
        "A product or service you could offer to solve a problem.",
        "Good ideas start with a real problem that people have.",
        "Write the problem, who has it and how you would solve it, in three sentences.",
        "Is there a youth business support programme near me?"),
    "target market": _t(S,
        "The group of people most likely to buy from you.",
        "Knowing them keeps your marketing and your prices realistic.",
        "Describe your ideal customer in one paragraph.",
        "Is there a youth business support programme near me?"),
    "startup costs": _t(S,
        "The money you need to spend before your business can start earning.",
        "Knowing them tells you how much you must save or raise.",
        "List every item you need and its price.",
        "Is there a youth business support programme near me?"),
    "profit": _t(S,
        "The money left after you subtract your costs from what you earned.",
        "A business that makes no profit cannot last.",
        "Write down your costs and your price to see your profit on each sale.",
        "Is there a youth business support programme near me?"),
    "cash flow": _t(S,
        "The money coming into and going out of your business over time.",
        "A business can look profitable and still fail if the cash runs out.",
        "Write down every rand in and out each week.",
        "Is there a youth business support programme near me?"),
    "customer service": _t(S,
        "How you treat and help the people who buy from you.",
        "Good service brings customers back and recommends you to others.",
        "Reply quickly and politely, and ask for feedback.",
        "Is there a youth business support programme near me?"),
    "marketing": _t(S,
        "Telling people about your product or service so they want to buy it.",
        "Even a good business needs customers who know about it.",
        "Start with free options: word of mouth, a WhatsApp status and social media.",
        "Is there a youth business support programme near me?"),
    "funding": _t(S,
        "Money to start or grow a business or to study, such as grants, loans or bursaries.",
        "Many young people cannot start without it.",
        "Ask a youth agency such as the NYDA what support exists and what it requires.",
        "Does the college know of funding for students or young founders?"),
})


# ---------------------------------------------------------------------------
# MY PATH: pick a stage, get a checklist of next steps
# ---------------------------------------------------------------------------
STAGES = {
    "I've just finished matric": [
        "Explore your options: TVET college, university, learnership or work.",
        "Check study-funding dates, for example NSFAS.",
        "Make sure your ID and certificates are ready.",
        "Build a simple CV.",
        "Look at youth opportunity platforms such as SAYouth.mobi.",
    ],
    "I'm in N4 or N5": [
        "Know your subjects and exam dates for this year.",
        "Ask your college for your last registration and completion dates (NATED is being phased out).",
        "Keep copies of every statement of results.",
        "Start thinking early about where you could do your workplace training.",
        "Start a simple CV.",
    ],
    "I'm finishing N6": [
        "Confirm which subjects you still need to pass.",
        "Ask your college how much workplace experience you need.",
        "Start looking for a workplace placement now.",
        "Keep a record of your workplace hours.",
        "Save your supervisor's contact details.",
    ],
    "I'm doing my workplace training (logbook)": [
        "Agree your tasks with your supervisor.",
        "Write a weekly summary in your own words.",
        "Collect evidence of your work if your college asks for it.",
        "Get your entries signed and dated regularly.",
        "Keep a backup copy or photos of your logbook pages.",
    ],
    "I've submitted my logbook": [
        "Confirm in writing that your college received it.",
        "Ask what must be fixed, and by when.",
        "Keep copies of everything you submitted.",
        "Follow up politely every week.",
        "While you wait, update your CV and apply for jobs or learnerships.",
    ],
    "I'm looking for work or a placement": [
        "Have your CV ready and up to date.",
        "Prepare certified copies of your ID and qualifications.",
        "Make a list of organisations and SETAs in your field.",
        "Write a placement request and send it (see the Request tab).",
        "Track every message in the Tracker tab and follow up.",
    ],
    "I want to start a small business": [
        "Write your business idea in one sentence.",
        "Say who will buy it (your customers).",
        "List what you need to start and what it will cost.",
        "Test it with three real people before spending big money.",
        "Keep a record of money in and money out.",
        "Ask about free youth business support in your area.",
    ],
}

# ---------------------------------------------------------------------------
# READY: each question has a tip if the answer is "no"
# ---------------------------------------------------------------------------
READINESS = [
    ("I have an up-to-date CV.", "Write a one-page CV with your education, skills and workplace training."),
    ("I have certified copies of my ID and qualifications.", "Ask your college or a police station how to get documents certified."),
    ("I know how much workplace experience my qualification needs.", "Ask your college for the exact requirement, in writing."),
    ("I have a workplace supervisor or placement contact.", "Write a placement request and send it to three organisations (see the Request tab)."),
    ("My logbook is up to date and signed.", "Update your entries this week and ask your supervisor to sign them."),
    ("I have a working email address and data to apply online.", "Create a professional email address and budget some data for applications."),
]

STATUSES = ["Planned", "Contacted", "Follow up", "Replied", "Placed"]
STATUS_COLOURS = {
    "Planned": MINT,
    "Contacted": SAND,
    "Follow up": "#F2C14E",
    "Replied": "#9AD1C9",
    "Placed": "#7BC47F",
}

DEMO_ENTRIES = [
    {"org": "Example Municipality HR (demo)", "contacted": "12 Oct", "follow_up": "19 Oct", "status": "Contacted"},
    {"org": "Sample Primary School Office (demo)", "contacted": "14 Oct", "follow_up": "21 Oct", "status": "Follow up"},
    {"org": "Demo Accounting Firm (demo)", "contacted": "", "follow_up": "", "status": "Planned"},
]

# ---------------------------------------------------------------------------
# SCAM CHECK: rules that look for common job-scam warning signs (runs offline)
# ---------------------------------------------------------------------------
RED_FLAGS = [
    ("Asks you to pay",
     ["registration fee", "application fee", "admin fee", "processing fee", "training fee", "starter pack", "deposit", "pay to"],
     "Real employers do not charge you to apply or be interviewed."),
    ("Wants your ID or bank details",
     ["bank details", "banking details", "copy of your id", "send your id", "card number", "otp", "pin number"],
     "Never send these before you have confirmed the company and the role."),
    ("Too good to be true",
     ["guaranteed", "easy money", "quick money", "no experience", "per day", "per week", "earn up to", "daily income"],
     "High pay for little work is a classic scam sign."),
    ("WhatsApp or inbox only",
     ["whatsapp only", "whatsapp us", "message us on whatsapp", "inbox us", "dm us"],
     "Real companies have an official website and email address."),
    ("Pressure to act fast",
     ["limited slots", "limited spots", "act now", "hurry", "today only", "last chance", "urgent"],
     "Scammers rush you so you do not check."),
    ("Recruit-your-friends income",
     ["recruit", "downline", "refer friends", "invite friends", "commission for every"],
     "Earning mainly from bringing in others is a pyramid-style scheme."),
    ("Free email address",
     ["@gmail.com", "@yahoo.com", "@hotmail.com"],
     "Check if the company also has an official website and email."),
]


def scan_advert(text):
    t = text.lower()
    return [(title, advice) for title, words, advice in RED_FLAGS if any(w in t for w in words)]


# ---------------------------------------------------------------------------
# SKILLS PROFILE options
# ---------------------------------------------------------------------------
SKILL_OPTIONS = [
    "Communication", "Teamwork", "Problem-solving", "Computer and digital skills",
    "Time management", "Customer service", "Writing and admin",
    "Selling and marketing", "Leadership", "Working under pressure",
]
EXP_TYPES = [
    "Workplace training", "Volunteering", "Small business",
    "Community or church project", "School or study project",
]


# ---------------------------------------------------------------------------
# Small helpers for saving and loading
# ---------------------------------------------------------------------------
def read_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)


def record_search(term):
    counts = read_json(COUNTS_FILE, {})
    counts[term] = counts.get(term, 0) + 1
    write_json(COUNTS_FILE, counts)


def popular_terms(limit=4):
    counts = read_json(COUNTS_FILE, {})
    ranked = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return [t for t, _ in ranked[:limit] if t in TERMS]


def find_matches(query):
    """Exact match first, then terms that contain the search words."""
    if query in TERMS:
        return [query]
    return [t for t in TERMS if query in t or t in query]


def save_profile(profile):
    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(profile, f)


def clear_profile():
    try:
        os.remove(PROFILE_FILE)
    except FileNotFoundError:
        pass


# ---------------------------------------------------------------------------
# Small building blocks for the screens
# ---------------------------------------------------------------------------
def card(content):
    return ft.Container(content=content, bgcolor=WHITE, border_radius=16, padding=16)


def part(title, text, colour):
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(title.upper(), size=11, weight=ft.FontWeight.BOLD, color=DEEP),
                ft.Text(text, size=14, color=INK),
            ],
            spacing=2,
        ),
        bgcolor=SOFT,
        border_radius=10,
        padding=10,
        border=ft.Border(left=ft.BorderSide(5, colour)),
    )


def chip(label, on_click, colour=MINT, selected=False):
    return ft.Container(
        content=ft.Text(label, size=13, weight=ft.FontWeight.W_600, color=WHITE if selected else DEEP),
        bgcolor=TEAL if selected else colour,
        border_radius=20,
        padding=ft.Padding(left=12, right=12, top=7, bottom=7),
        on_click=on_click,
    )


def check_row(label, on_change=None):
    """A tick box with text that wraps. Tapping the text also ticks the box."""
    box = ft.Checkbox(value=False, active_color=TEAL)

    def changed(e):
        if on_change:
            on_change(e)

    box.on_change = changed

    def toggle(e):
        box.value = not box.value
        changed(e)
        box.update()

    row = ft.Row(
        [
            box,
            ft.Container(
                content=ft.Text(label, size=14, color=INK),
                expand=True,
                on_click=toggle,
                padding=ft.Padding(left=0, right=0, top=10, bottom=10),
            ),
        ],
        vertical_alignment=ft.CrossAxisAlignment.START,
        spacing=4,
    )
    return box, row


def note(text):
    return ft.Text(text, size=11, color=GREY, text_align=ft.TextAlign.CENTER)


# ---------------------------------------------------------------------------
# The app
# ---------------------------------------------------------------------------
def main(page: ft.Page):
    page.title = "Karabonia"
    page.padding = 0
    page.bgcolor = SOFT
    page.theme = ft.Theme(color_scheme_seed=TEAL)
    page.window.width = 390   # phone-sized window on your laptop
    page.window.height = 760

    clipboard = ft.Clipboard()
    page.services.append(clipboard)

    # =====================================================================
    # TOOL 1: LEARN (Jargon Buster)
    # =====================================================================
    state = {"group": "All"}
    search_box = ft.TextField(label="Type a word, e.g. logbook", expand=True)
    result_area = ft.Column(spacing=12)
    popular_row = ft.Row(wrap=True, spacing=8, run_spacing=8)
    popular_card = card(ft.Column([ft.Text("Most searched", weight=ft.FontWeight.BOLD, color=DEEP), popular_row], spacing=8))
    group_row = ft.Row(wrap=True, spacing=8, run_spacing=8)
    word_row = ft.Row(wrap=True, spacing=8, run_spacing=8)
    thanks_text = ft.Text("", color=DEEP, weight=ft.FontWeight.W_600, visible=False)
    suggest_box = ft.TextField(label="Suggest a term", expand=True)

    def refresh_popular():
        top = popular_terms()
        popular_row.controls = [chip(t, lambda e, t=t: show_term(t), SAND) for t in top]
        popular_card.visible = len(top) > 0

    def refresh_words():
        names = ["All"] + GROUPS
        group_row.controls = [chip(g, lambda e, g=g: pick_group(g), MINT, selected=(g == state["group"])) for g in names]
        words = [t for t in sorted(TERMS) if state["group"] == "All" or TERMS[t]["group"] == state["group"]]
        word_row.controls = [chip(t, lambda e, t=t: show_term(t)) for t in words]

    def pick_group(g):
        state["group"] = g
        refresh_words()
        page.update()

    def save_suggestion(term):
        term = term.strip()[:60]
        if term:
            with open(SUGGESTIONS_FILE, "a", encoding="utf-8") as f:
                f.write(term + "\n")
            thanks_text.value = "Thank you! Your suggestion was received."
            thanks_text.visible = True
        page.update()

    def send_suggestion(e):
        save_suggestion(suggest_box.value or "")
        suggest_box.value = ""
        page.update()

    def term_card(key):
        t = TERMS[key]
        items = [
            ft.Text(key.title(), size=20, weight=ft.FontWeight.BOLD, color=DEEP),
            ft.Text(t["group"], size=12, color=GREY),
            part("What it means", t["means"], TEAL),
            part("Why it matters", t["matters"], SAND),
            part("What to do next", t["next"], PLUM),
            part("Ask your college", t["ask"], "#4A90B8"),
        ]
        if t.get("checklist"):
            title, steps = CHECKLISTS[t["checklist"]]
            rows = [check_row(s)[1] for s in steps]
            items.append(
                ft.Container(
                    content=ft.Column([ft.Text(f"Do this next: {title}", weight=ft.FontWeight.BOLD, color=DEEP)] + rows, spacing=0),
                    bgcolor=SOFT,
                    border_radius=10,
                    padding=10,
                )
            )
        source = t.get("source", "Source: confirm with your college")
        items.append(ft.Text(f"{source}. Draft. Last checked: {LAST_CHECKED}.", size=11, color=GREY))
        return card(ft.Column(items, spacing=10))

    def not_found_card(q):
        return card(
            ft.Column(
                [
                    ft.Text(f'We don\'t have "{q}" yet.', weight=ft.FontWeight.BOLD, color=INK),
                    ft.Text("Want it explained? Tap the button and we will add it.", color=INK),
                    ft.Button("Suggest this term", bgcolor=TEAL, color=WHITE, on_click=lambda e: save_suggestion(q)),
                ],
                spacing=8,
            )
        )

    def run_search(q):
        q = q.strip().lower()
        thanks_text.value = ""
        thanks_text.visible = False
        result_area.controls.clear()
        if q:
            matches = find_matches(q)
            if matches:
                for key in matches:
                    record_search(key)
                    result_area.controls.append(term_card(key))
            else:
                result_area.controls.append(not_found_card(q))
        refresh_popular()
        page.update()

    def show_term(key):
        search_box.value = key
        run_search(key)

    search_box.on_submit = lambda e: run_search(search_box.value or "")

    def learn_view():
        refresh_popular()
        refresh_words()
        return ft.Column(
            [
                card(ft.Row([search_box, ft.Button("Search", bgcolor=TEAL, color=WHITE, on_click=lambda e: run_search(search_box.value or ""))], spacing=8)),
                thanks_text,
                result_area,
                popular_card,
                card(ft.Column([ft.Text("Browse by topic", weight=ft.FontWeight.BOLD, color=DEEP), group_row, word_row], spacing=10)),
                card(ft.Column([ft.Text("Missing a word?", weight=ft.FontWeight.BOLD, color=DEEP), ft.Row([suggest_box, ft.Button("Send", bgcolor=TEAL, color=WHITE, on_click=send_suggestion)], spacing=8)], spacing=8)),
                quiz_card,
                note("Draft explanations. Always confirm important details with your college."),
            ],
            spacing=12,
        )

    # =====================================================================
    # TOOL 2: MY PATH
    # =====================================================================
    path_progress = ft.ProgressBar(value=0, color=TEAL, bgcolor=MINT, height=8)
    path_count = ft.Text("Choose where you are above to see your steps.", color=DEEP, weight=ft.FontWeight.W_600)
    path_list = ft.Column(spacing=0)
    path_boxes = []

    def update_path_progress(e=None):
        total = len(path_boxes)
        done = sum(1 for b in path_boxes if b.value)
        path_progress.value = (done / total) if total else 0
        path_count.value = f"{done} of {total} steps done" if total else "Choose where you are above to see your steps."
        page.update()

    def apply_stage(stage):
        path_boxes.clear()
        rows = []
        for step in STAGES.get(stage, []):
            box, row = check_row(step, update_path_progress)
            path_boxes.append(box)
            rows.append(row)
        path_list.controls = rows
        update_path_progress()

    def choose_stage(e):
        apply_stage(e.control.value)

    stage_dropdown = ft.Dropdown(
        label="Where are you now?",
        options=[ft.DropdownOption(key=s, text=s) for s in STAGES],
        on_select=choose_stage,
        expand=True,
    )

    def path_view():
        return ft.Column(
            [
                diag_card,
                card(
                    ft.Column(
                        [
                            ft.Text("Your next steps", size=20, weight=ft.FontWeight.BOLD, color=DEEP),
                            ft.Text("Pick where you are and tick off each step as you do it.", color=INK),
                            ft.Row([stage_dropdown]),
                        ],
                        spacing=10,
                    )
                ),
                card(ft.Column([path_count, path_progress, path_list], spacing=10)),
                note("Draft steps. Confirm requirements with your college."),
            ],
            spacing=12,
        )

    # =====================================================================
    # TOOL 4: TRACKER (built before Request because Request can add to it)
    # =====================================================================
    entries = read_json(TRACKER_FILE, [])
    tracker_list = ft.Column(spacing=10)
    org_box = ft.TextField(label="Organisation", expand=True)
    contacted_box = ft.TextField(label="Date contacted", hint_text="e.g. 20 Oct", expand=True)
    follow_box = ft.TextField(label="Follow up on", hint_text="e.g. 27 Oct", expand=True)
    status_dd = ft.Dropdown(label="Status", value="Planned", options=[ft.DropdownOption(key=s, text=s) for s in STATUSES], expand=True)
    tracker_msg = ft.Text("", color=DEEP, weight=ft.FontWeight.W_600, visible=False)

    def save_entries():
        write_json(TRACKER_FILE, entries)

    def next_status(i):
        cur = entries[i]["status"]
        entries[i]["status"] = STATUSES[(STATUSES.index(cur) + 1) % len(STATUSES)] if cur in STATUSES else "Planned"
        save_entries()
        render_tracker()
        page.update()

    def delete_entry(i):
        entries.pop(i)
        save_entries()
        render_tracker()
        page.update()

    def render_tracker():
        cards = []
        for i, en in enumerate(entries):
            when = []
            if en.get("contacted"):
                when.append(f"Contacted: {en['contacted']}")
            if en.get("follow_up"):
                when.append(f"Follow up: {en['follow_up']}")
            cards.append(
                card(
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(en["org"], weight=ft.FontWeight.BOLD, color=INK, expand=True),
                                    ft.Container(
                                        content=ft.Text(en["status"], size=12, weight=ft.FontWeight.W_600, color=INK),
                                        bgcolor=STATUS_COLOURS.get(en["status"], MINT),
                                        border_radius=12,
                                        padding=ft.Padding(left=10, right=10, top=4, bottom=4),
                                    ),
                                ],
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            ft.Text("   ".join(when) if when else "No dates yet", size=13, color=GREY),
                            ft.Row(
                                [
                                    ft.Button("Next status", bgcolor=TEAL, color=WHITE, on_click=lambda e, i=i: next_status(i)),
                                    ft.TextButton("Delete", on_click=lambda e, i=i: delete_entry(i)),
                                ],
                                spacing=8,
                            ),
                        ],
                        spacing=6,
                    )
                )
            )
        if not cards:
            cards = [card(ft.Text("No organisations yet. Add one above, or use the example data to see how it works.", color=GREY))]
        tracker_list.controls = cards

    def add_entry(org, contacted="", follow_up="", status="Planned"):
        org = (org or "").strip()[:80]
        if not org:
            return False
        entries.append({"org": org, "contacted": (contacted or "").strip()[:20], "follow_up": (follow_up or "").strip()[:20], "status": status})
        save_entries()
        return True

    def on_add_entry(e):
        if add_entry(org_box.value, contacted_box.value, follow_box.value, status_dd.value or "Planned"):
            org_box.value = contacted_box.value = follow_box.value = ""
            tracker_msg.value = "Added."
        else:
            tracker_msg.value = "Type the organisation's name first."
        tracker_msg.visible = True
        render_tracker()
        page.update()

    def load_demo(e):
        for d in DEMO_ENTRIES:
            if not any(x["org"] == d["org"] for x in entries):
                entries.append(dict(d))
        save_entries()
        tracker_msg.value = "Example (fictional) organisations added."
        tracker_msg.visible = True
        render_tracker()
        page.update()

    def clear_all(e):
        entries.clear()
        save_entries()
        tracker_msg.value = "Cleared."
        tracker_msg.visible = True
        render_tracker()
        page.update()

    def tracker_view():
        render_tracker()
        return ft.Column(
            [
                card(
                    ft.Column(
                        [
                            ft.Text("My organisations", size=20, weight=ft.FontWeight.BOLD, color=DEEP),
                            ft.Text("Keep track of who you contacted and when to follow up. Use organisation names only, no private details.", color=INK, size=13),
                            ft.Row([org_box]),
                            ft.Row([contacted_box, follow_box], spacing=8),
                            ft.Row([status_dd]),
                            ft.Row([ft.Button("Add", bgcolor=TEAL, color=WHITE, on_click=on_add_entry), ft.TextButton("Use example data", on_click=load_demo), ft.TextButton("Clear all", on_click=clear_all)], spacing=8, wrap=True),
                            tracker_msg,
                        ],
                        spacing=8,
                    )
                ),
                tracker_list,
            ],
            spacing=12,
        )

    # =====================================================================
    # TOOL 3: REQUEST (placement request writer)
    # =====================================================================
    name_box = ft.TextField(label="Your name")
    qual_box = ft.TextField(label="Your qualification", hint_text="e.g. N6 Public Management")
    college_box = ft.TextField(label="Your college")
    to_org_box = ft.TextField(label="Organisation you are writing to")
    contact_box = ft.TextField(label="Contact person (optional)")
    from_box = ft.TextField(label="Available from", hint_text="e.g. 1 November", expand=True)
    period_box = ft.TextField(label="Period needed", hint_text="e.g. 6 months", expand=True)
    message_box = ft.TextField(label="Your message", multiline=True, min_lines=10, max_lines=18, read_only=True, visible=False)
    request_msg = ft.Text("", color=DEEP, weight=ft.FontWeight.W_600, visible=False)
    copy_button = ft.Button("Copy message", bgcolor=TEAL, color=WHITE, visible=False)
    track_button = ft.TextButton("Add to my tracker", visible=False)

    def build_message():
        who = (contact_box.value or "").strip()
        greeting = f"Dear {who}," if who else "Dear Sir/Madam,"
        name = (name_box.value or "[your name]").strip()
        qual = (qual_box.value or "[your qualification]").strip()
        college = (college_box.value or "[your college]").strip()
        org = (to_org_box.value or "[organisation]").strip()
        start = (from_box.value or "[start date]").strip()
        period = (period_box.value or "[period required by my college]").strip()
        return (
            f"Subject: Request for workplace placement - {qual}\n\n"
            f"{greeting}\n\n"
            f"My name is {name}. I have completed {qual} at {college}, and I am looking for a workplace "
            f"placement to complete the practical part of my qualification.\n\n"
            f"I would be grateful for the opportunity to join {org} for {period}. "
            f"I am available from {start}, and I have attached my CV.\n\n"
            f"Thank you for your time and consideration.\n\n"
            f"Kind regards,\n{name}\n[phone number]\n[email address]"
        )

    def create_message(e):
        message_box.value = build_message()
        message_box.visible = True
        copy_button.visible = True
        track_button.visible = bool((to_org_box.value or "").strip())
        request_msg.value = "Read it, fix the [brackets], then copy it."
        request_msg.visible = True
        page.update()

    async def copy_message(e):
        try:
            await clipboard.set(message_box.value or "")
            request_msg.value = "Copied! Paste it into your email."
        except Exception:
            request_msg.value = "Press and hold the message to select and copy it."
        request_msg.visible = True
        page.update()

    def add_from_request(e):
        if add_entry(to_org_box.value, "", "", "Planned"):
            request_msg.value = "Added to your tracker as Planned."
        else:
            request_msg.value = "Type the organisation's name first."
        request_msg.visible = True
        page.update()

    copy_button.on_click = copy_message
    track_button.on_click = add_from_request

    def request_view():
        return ft.Column(
            [
                card(
                    ft.Column(
                        [
                            ft.Text("Placement request", size=20, weight=ft.FontWeight.BOLD, color=DEEP),
                            ft.Text("Fill in the boxes and Karabonia writes a professional message you can send.", color=INK, size=13),
                            name_box, qual_box, college_box, to_org_box, contact_box,
                            ft.Row([from_box, period_box], spacing=8),
                            ft.Button("Write my message", bgcolor=TEAL, color=WHITE, on_click=create_message),
                        ],
                        spacing=8,
                    )
                ),
                card(ft.Column([request_msg, message_box, ft.Row([copy_button, track_button], spacing=8, wrap=True)], spacing=8)),
                note("Before you send: attach your CV and check the company is real."),
            ],
            spacing=12,
        )

    # =====================================================================
    # TOOL 5: READY (readiness check with ONE next step)
    # =====================================================================
    score_text = ft.Text("Tick what is true for you.", size=18, weight=ft.FontWeight.BOLD, color=DEEP)
    score_bar = ft.ProgressBar(value=0, color=SAND, bgcolor=MINT, height=10)
    next_step_text = ft.Text("", size=14, color=INK)
    next_step_card = ft.Container(
        content=ft.Column([ft.Text("YOUR NEXT STEP", size=11, weight=ft.FontWeight.BOLD, color=DEEP), next_step_text], spacing=2),
        bgcolor="#FFF1E3",
        border_radius=10,
        padding=12,
        border=ft.Border(left=ft.BorderSide(5, SAND)),
        visible=False,
    )
    ready_boxes = []
    ready_rows = []

    def update_readiness(e=None):
        total = len(READINESS)
        score = sum(1 for b in ready_boxes if b.value)
        score_bar.value = score / total
        if score == total:
            score_text.value = f"{score} of {total}: you are work-ready!"
        elif score >= total - 1:
            score_text.value = f"{score} of {total}: nearly work-ready!"
        elif score >= total // 2:
            score_text.value = f"{score} of {total}: a good start."
        else:
            score_text.value = f"{score} of {total}: let's start with the basics."
        missing = [tip for (q, tip), b in zip(READINESS, ready_boxes) if not b.value]
        if missing:
            next_step_text.value = missing[0]
        else:
            next_step_text.value = "Start applying, and track every message in the Tracker tab."
        next_step_card.visible = True
        page.update()

    for q, _tip in READINESS:
        box, row = check_row(q, update_readiness)
        ready_boxes.append(box)
        ready_rows.append(row)

    def ready_view():
        return ft.Column(
            [
                card(ft.Column([ft.Text("Work Readiness Check", size=20, weight=ft.FontWeight.BOLD, color=DEEP)] + ready_rows, spacing=4)),
                card(ft.Column([score_text, score_bar, next_step_card], spacing=10)),
            ],
            spacing=12,
        )

    # =====================================================================
    # TOOL 6: SCAM CHECK
    # =====================================================================
    scam_box = ft.TextField(label="Paste the advert or message here", multiline=True, min_lines=6, max_lines=12)
    scam_result = ft.Column(spacing=10)

    def check_advert(e):
        text = (scam_box.value or "").strip()[:3000]
        scam_result.controls.clear()
        if not text:
            items = [ft.Text("Paste an advert or message first.", color=INK)]
        else:
            hits = scan_advert(text)
            if hits:
                if len(hits) >= 3:
                    level, colour = "HIGH RISK", RED
                elif len(hits) == 2:
                    level, colour = "MEDIUM RISK", SAND
                else:
                    level, colour = "BE CAREFUL", "#F2C14E"
                items = [ft.Text(f"{level}: {len(hits)} warning sign(s)", size=18, weight=ft.FontWeight.BOLD, color=INK)]
                items += [part(title, advice, colour) for title, advice in hits]
                items.append(ft.Text("Do not send money, ID or bank details. Ask your college or someone you trust.", size=13, color=INK))
            else:
                items = [
                    ft.Text("No common warning signs found", size=18, weight=ft.FontWeight.BOLD, color=INK),
                    ft.Text("That does not prove it is real. Check the company's official website and contact details yourself.", size=13, color=INK),
                ]
        scam_result.controls.append(card(ft.Column(items, spacing=10)))
        page.update()

    def scam_view():
        return ft.Column(
            [
                card(
                    ft.Column(
                        [
                            ft.Text("Is this opportunity real?", size=20, weight=ft.FontWeight.BOLD, color=DEEP),
                            ft.Text("Paste a job advert or WhatsApp message and Karabonia checks it for scam warning signs.", color=INK, size=13),
                            scam_box,
                            ft.Button("Check it", bgcolor=TEAL, color=WHITE, on_click=check_advert),
                        ],
                        spacing=8,
                    )
                ),
                scam_result,
                note("This is a guide, not a guarantee. Always verify with the company directly."),
            ],
            spacing=12,
        )

    # =====================================================================
    # TOOL 7: SKILLS PROFILE
    # =====================================================================
    skill_boxes, skill_rows = [], []
    for s in SKILL_OPTIONS:
        b, r = check_row(s)
        skill_boxes.append(b)
        skill_rows.append(r)

    exp_items = []
    exp_type_dd = ft.Dropdown(label="Type of experience", options=[ft.DropdownOption(key=x, text=x) for x in EXP_TYPES], expand=True)
    exp_text = ft.TextField(label="What did you do?", hint_text="e.g. Sold goods at community events")
    exp_proof = ft.TextField(label="Proof you can show (optional)", hint_text="e.g. signed logbook, reference letter")
    exp_list = ft.Column(spacing=8)
    prof_out = ft.TextField(label="Your profile", multiline=True, min_lines=8, max_lines=16, read_only=True, visible=False)
    prof_msg = ft.Text("", color=DEEP, weight=ft.FontWeight.W_600, visible=False)
    prof_copy = ft.Button("Copy profile", bgcolor=TEAL, color=WHITE, visible=False)

    def render_exp():
        rows = []
        for i, x in enumerate(exp_items):
            line = f"{x['type']}: {x['what']}" + (f"  (Proof: {x['proof']})" if x["proof"] else "")
            rows.append(
                ft.Row(
                    [
                        ft.Text(line, size=13, color=INK, expand=True),
                        ft.TextButton("Remove", on_click=lambda e, i=i: remove_exp(i)),
                    ]
                )
            )
        exp_list.controls = rows

    def remove_exp(i):
        exp_items.pop(i)
        render_exp()
        page.update()

    def add_exp(e):
        what = (exp_text.value or "").strip()[:120]
        if not what:
            prof_msg.value = "Type what you did first."
        else:
            exp_items.append({"type": exp_type_dd.value or "Experience", "what": what, "proof": (exp_proof.value or "").strip()[:80]})
            exp_text.value = ""
            exp_proof.value = ""
            prof_msg.value = "Added."
        prof_msg.visible = True
        render_exp()
        page.update()

    def build_profile(e):
        name = (name_box.value or "").strip() or "[your name]"
        skills = [s for s, b in zip(SKILL_OPTIONS, skill_boxes) if b.value]
        lines = [
            "About me",
            f"I am {name}, a young South African ready to move from study to work.",
            "",
            "My skills",
            ", ".join(skills) if skills else "[tick your skills above]",
            "",
            "My experience",
        ]
        if exp_items:
            for x in exp_items:
                lines.append(f"- {x['type']}: {x['what']}" + (f" (Evidence: {x['proof']})" if x["proof"] else ""))
        else:
            lines.append("[add your experience above]")
        lines += ["", "I can provide references and evidence on request."]
        prof_out.value = "\n".join(lines)
        prof_out.visible = True
        prof_copy.visible = True
        n_proof = sum(1 for x in exp_items if x["proof"])
        prof_msg.value = f"{len(skills)} skills, {len(exp_items)} experiences, {n_proof} with proof. Proof makes your profile more credible."
        prof_msg.visible = True
        page.update()

    async def copy_profile(e):
        try:
            await clipboard.set(prof_out.value or "")
            prof_msg.value = "Copied! Paste it into your CV or message."
        except Exception:
            prof_msg.value = "Press and hold the text to copy it."
        prof_msg.visible = True
        page.update()

    prof_copy.on_click = copy_profile

    def skills_view():
        return ft.Column(
            [
                card(
                    ft.Column(
                        [
                            ft.Text("My Skills Profile", size=20, weight=ft.FontWeight.BOLD, color=DEEP),
                            ft.Text("Turn what you can do into a profile employers can trust. Informal experience counts.", color=INK, size=13),
                            ft.Text("1. Tick your skills", weight=ft.FontWeight.BOLD, color=DEEP),
                        ]
                        + skill_rows,
                        spacing=4,
                    )
                ),
                card(
                    ft.Column(
                        [
                            ft.Text("2. Add your experience", weight=ft.FontWeight.BOLD, color=DEEP),
                            ft.Row([exp_type_dd]),
                            exp_text,
                            exp_proof,
                            ft.Button("Add", bgcolor=TEAL, color=WHITE, on_click=add_exp),
                            exp_list,
                        ],
                        spacing=8,
                    )
                ),
                card(
                    ft.Column(
                        [
                            ft.Text("3. Build your profile", weight=ft.FontWeight.BOLD, color=DEEP),
                            ft.Button("Create my profile", bgcolor=PLUM, color=WHITE, on_click=build_profile),
                            prof_msg,
                            prof_out,
                            prof_copy,
                        ],
                        spacing=8,
                    )
                ),
                note("Only list true things. Never include ID numbers or private details."),
            ],
            spacing=12,
        )

    # =====================================================================
    # JARGON QUIZ (bottom of the Learn tab)
    # =====================================================================
    quiz = {"score": 0, "n": 0, "answer": ""}
    quiz_q = ft.Text("", size=16, weight=ft.FontWeight.BOLD, color=INK)
    quiz_opts = ft.Column(spacing=8)
    quiz_fb = ft.Text("", size=14, color=INK)
    quiz_score = ft.Text("Score: 0 / 0", color=DEEP, weight=ft.FontWeight.W_600)

    def pick(o):
        quiz["n"] += 1
        if o == quiz["answer"]:
            quiz["score"] += 1
            quiz_fb.value = "Correct! " + TERMS[o]["matters"]
        else:
            quiz_fb.value = f"Not quite. It is {quiz['answer'].title()}. " + TERMS[quiz["answer"]]["matters"]
        quiz_score.value = f"Score: {quiz['score']} / {quiz['n']}"
        quiz_opts.controls = []
        page.update()

    def next_question(e=None):
        key = random.choice(list(TERMS))
        options = [key] + random.sample([k for k in TERMS if k != key], 2)
        random.shuffle(options)
        quiz["answer"] = key
        quiz_q.value = "Which term means: " + TERMS[key]["means"]
        quiz_fb.value = ""
        quiz_opts.controls = [
            ft.Button(o.title(), bgcolor=MINT, color=DEEP, on_click=lambda e, o=o: pick(o)) for o in options
        ]
        if e is not None:
            page.update()

    next_question()
    quiz_card = card(
        ft.Column(
            [
                ft.Text("Test yourself", weight=ft.FontWeight.BOLD, color=DEEP),
                quiz_q, quiz_opts, quiz_fb,
                ft.Row([quiz_score, ft.TextButton("Next question", on_click=next_question)], spacing=12),
            ],
            spacing=8,
        )
    )

    # =====================================================================
    # WHAT IS STOPPING YOU? (diagnostic, top of the Path tab)
    # =====================================================================
    PERSONAS = {
        "I've just finished matric": "I've just finished matric",
        "I'm studying at a college or university": "I'm in N4 or N5",
        "I have a qualification but need experience or work": "I'm looking for work or a placement",
        "I want to create my own opportunity": "I want to start a small business",
    }
    PERSONA_FOCUS = {
        "I've just finished matric": "Explore your options: college, learnership, work or your own idea.",
        "I'm studying at a college or university": "Understand your requirements early and plan your workplace training.",
        "I have a qualification but need experience or work": "Understand logbooks and workplace requirements, explore entry-level roles, find your skills gaps.",
        "I want to create my own opportunity": "Explore small-business ideas and practical skills that can earn an income.",
    }
    BLOCKERS = {
        "I don't know my options": (
            "Unclear options",
            "Write down three options (study, learnership, work or your own business) and one question to ask about each.",
            "Learn tab: search 'learnership' or 'nsfas'"),
        "I have no workplace experience": (
            "No experience yet",
            "Write a placement request and send it to three organisations this week.",
            "Request tab, then Tracker"),
        "I don't understand the requirements": (
            "Unclear requirements",
            "Search 'logbook' or 'in-service training' and take the 'Ask your college' question to your college.",
            "Learn tab"),
        "My CV or profile is not ready": (
            "Profile not ready",
            "Tick your skills, add one experience (informal counts) and copy your profile into your CV.",
            "Profile tab"),
        "I don't know which opportunities are real": (
            "Scam worry",
            "Paste the advert into the Scam? tab before you reply, pay or send any documents.",
            "Scam? tab"),
        "I want my own income but don't know how": (
            "No income idea yet",
            "Write your business idea in one sentence and test it with three real people.",
            "Learn tab: search 'business idea'"),
        "I lack money, data or transport": (
            "Money, data or transport",
            "Use Karabonia offline, and ask your college and a youth agency such as NYDA about support.",
            "Learn tab: search 'funding'"),
    }
    diag_persona = ft.Dropdown(label="Which is closest to you?", options=[ft.DropdownOption(key=k, text=k) for k in PERSONAS], expand=True)
    diag_block = ft.Dropdown(label="What is stopping you most?", options=[ft.DropdownOption(key=k, text=k) for k in BLOCKERS], expand=True)
    diag_result = ft.Column(spacing=10)

    def run_diag(e):
        p, b = diag_persona.value, diag_block.value
        if not p or not b:
            diag_result.controls = [ft.Text("Pick one option in each box first.", color=INK)]
            page.update()
            return
        title, step, where = BLOCKERS[b]
        diag_result.controls = [
            part("Your focus", PERSONA_FOCUS[p], TEAL),
            part("What is stopping you", title, SAND),
            part("Your next practical step", step, PLUM),
            part("Where to go in Karabonia", where, "#4A90B8"),
        ]
        stage_dropdown.value = PERSONAS[p]
        apply_stage(PERSONAS[p])   # fills the checklist below

    diag_card = card(
        ft.Column(
            [
                ft.Text("What is stopping you?", size=20, weight=ft.FontWeight.BOLD, color=DEEP),
                ft.Text("Answer two questions and get one practical next step.", color=INK, size=13),
                ft.Row([diag_persona]),
                ft.Row([diag_block]),
                ft.Button("Find my next step", bgcolor=PLUM, color=WHITE, on_click=run_diag),
                diag_result,
            ],
            spacing=8,
        )
    )

    # =====================================================================
    # PAGE LAYOUT: header + body + bottom menu
    # =====================================================================
    greeting_text = ft.Text("", size=14, weight=ft.FontWeight.BOLD, color=WHITE)

    header = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [ft.Icon(ft.Icons.LOCAL_FLORIST, color=WHITE, size=28), ft.Text("Karabonia", size=30, weight=ft.FontWeight.BOLD, color=WHITE)],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=8,
                ),
                ft.Text("Your path from study to work", size=13, color=MINT),
                greeting_text,
                ft.TextButton("Switch user", on_click=lambda e: show_welcome(), style=ft.ButtonStyle(color=MINT)),
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding(left=16, right=16, top=18, bottom=6),
        alignment=ft.Alignment.CENTER,
        gradient=ft.LinearGradient(begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT, colors=[DEEP, TEAL, PLUM]),
    )

    views = [learn_view(), path_view(), request_view(), tracker_view(), ready_view(), scam_view(), skills_view()]
    body = ft.Container(content=ft.Column([views[0]], scroll=ft.ScrollMode.AUTO, expand=True), expand=True, padding=16)

    def on_nav(e):
        body.content = ft.Column([views[e.control.selected_index]], scroll=ft.ScrollMode.AUTO, expand=True)
        page.update()

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.MENU_BOOK, label="Learn"),
            ft.NavigationBarDestination(icon=ft.Icons.ROUTE, label="Path"),
            ft.NavigationBarDestination(icon=ft.Icons.EDIT_NOTE, label="Request"),
            ft.NavigationBarDestination(icon=ft.Icons.ASSIGNMENT, label="Tracker"),
            ft.NavigationBarDestination(icon=ft.Icons.CHECKLIST, label="Ready"),
            ft.NavigationBarDestination(icon=ft.Icons.SHIELD, label="Scam?"),
            ft.NavigationBarDestination(icon=ft.Icons.BADGE, label="Profile"),
        ],
        on_change=on_nav,
        selected_index=0,
    )

    # =====================================================================
    # WELCOME SCREEN: shown every time the app opens. Saves only a first name and stage on this device.
    # =====================================================================
    main_layout = ft.Column([header, body], spacing=0, expand=True)
    nav_bar = page.navigation_bar

    def show_main(profile):
        name = (profile.get("name") or "").strip()
        stage = profile.get("stage") or ""
        greeting_text.value = f"Welcome, {name}!" if name else "Welcome, guest!"
        if name:
            name_box.value = name          # pre-fill the Request form
        if stage in STAGES:
            stage_dropdown.value = stage   # pre-fill the Path tab
            apply_stage(stage)
        nav_bar.selected_index = 0
        body.content = ft.Column([views[0]], scroll=ft.ScrollMode.AUTO, expand=True)
        page.clean()
        page.navigation_bar = nav_bar
        page.add(main_layout)
        page.update()

    def show_welcome():
        clear_profile()
        wname = ft.TextField(label="Your first name (optional)", autofocus=True, border_radius=14)
        wstage = ft.Dropdown(
            label="Where are you now?",
            options=[ft.DropdownOption(key=st, text=st) for st in STAGES],
            expand=True,
            border_radius=14,
        )

        def on_start(e):
            profile = {"name": (wname.value or "").strip()[:30], "stage": wstage.value or ""}
            save_profile(profile)
            show_main(profile)

        def on_guest(e):
            show_main({"name": "", "stage": ""})

        def blob(w, h, left=None, top=None, right=None, bottom=None, opacity=0.18, colour=WHITE):
            return ft.Container(
                width=w, height=h, left=left, top=top, right=right, bottom=bottom,
                bgcolor=ft.Colors.with_opacity(opacity, colour),
                border_radius=max(w, h),
            )

        art = (
            ft.Image(src="welcome.png", width=140, height=140)
            if os.path.exists(WELCOME_IMG)
            else ft.Icon(ft.Icons.LOCAL_FLORIST, color=WHITE, size=72)
        )

        # Top section: soft shapes on a purple-to-pink gradient, curved at the bottom
        hero = ft.Container(
            height=340,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            border_radius=ft.BorderRadius(top_left=0, top_right=0, bottom_left=56, bottom_right=56),
            gradient=ft.LinearGradient(begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT, colors=[DEEP, PLUM, TEAL]),
            content=ft.Stack(
                [
                    blob(220, 220, left=-70, top=-60, opacity=0.14),
                    blob(140, 140, right=-40, top=30, opacity=0.18, colour=SAND),
                    blob(90, 90, left=30, bottom=40, opacity=0.20, colour=MINT),
                    blob(160, 110, right=-30, bottom=-20, opacity=0.16),
                    blob(36, 36, right=70, top=24, opacity=0.35),
                    blob(22, 22, left=110, top=70, opacity=0.30, colour=SAND),
                    ft.Container(
                        left=0, right=0, top=44,
                        content=ft.Column(
                            [
                                art,
                                ft.Text(WELCOME_TITLE, size=44, weight=ft.FontWeight.BOLD, color=WHITE),
                                ft.Text("Karabonia", size=26, weight=ft.FontWeight.W_600, color=MINT),
                                ft.Text(WELCOME_TAGLINE, size=14, color=WHITE, text_align=ft.TextAlign.CENTER),
                            ],
                            spacing=4,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ),
                ]
            ),
        )

        # Middle: the sign-in style card (name + stage)
        form = ft.Container(
            padding=ft.Padding(left=16, right=16, top=20, bottom=0),
            content=card(
                ft.Column(
                    [
                        ft.Text("Let's get to know you", size=20, weight=ft.FontWeight.BOLD, color=DEEP),
                        wname,
                        ft.Row([wstage]),
                        ft.Row([ft.Button("Take me to Karabonia", bgcolor=TEAL, color=WHITE, height=50, expand=True, on_click=on_start)]),
                        ft.Row([ft.TextButton("Continue as guest", on_click=on_guest)], alignment=ft.MainAxisAlignment.CENTER),
                    ],
                    spacing=12,
                )
            ),
        )

        # Bottom: what the student gets (built from WELCOME_POINTS)
        point_rows = [
            ft.Row(
                [
                    ft.Container(content=ft.Icon(icon, color=TEAL, size=20), bgcolor=MINT, border_radius=20, padding=8),
                    ft.Text(text, size=14, color=INK, expand=True),
                ],
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
            for icon, text in WELCOME_POINTS
        ]
        gives = ft.Container(
            padding=ft.Padding(left=16, right=16, top=4, bottom=24),
            content=card(
                ft.Column(
                    [ft.Text("What Karabonia gives you", size=18, weight=ft.FontWeight.BOLD, color=DEEP)] + point_rows
                    + [note("Judges: use any name, or continue as guest. Only a first name and your stage are saved, on this device only. Never enter ID numbers or passwords.")],
                    spacing=12,
                )
            ),
        )

        page.clean()
        page.navigation_bar = None
        page.add(
            ft.Column(
                [hero, form, gives],
                spacing=0,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            )
        )
        page.update()

    show_welcome()


ft.run(main, assets_dir=os.path.join(HERE, "assets"))