#import "@preview/basic-resume:0.2.8": *

// Personal Information
#let full-name = "Omalya Vidushini"

#show: resume.with(
  author: full-name,
  author-position: center,
  accent-color: "#26428b",
  font: "New Computer Modern",
  paper: "us-letter"
)

#grid(
  columns: (1fr, 1fr, 1fr),
  align(center)[
    phone: #link("tel:+94702104088") \
    address: Katubedda, Moratuwa
  ],
  align(center)[
    #link("mailto:omalya.21@cse.mrt.ac.lk") \
    #link("") 
  ],
  align(center)[
    #link("https://github.com/OmalyaV")[GitHub] \
    #link("https://linkedin.com/in/omalya-vidushini")[LinkedIn] 
  ]
)

#linebreak()

== Overview

#lorem(100)

#linebreak()

== Education

#edu(
  institution: "University of Moratuwa",
  location: "",
  dates: dates-helper(start-date: "Jan 2022", end-date: "Present"),
  degree: "BSc. Engineering (Hons) (Computer Science and Engineering - Data Science & Engineering)"
)
- Current CGPA: 3.71

#edu(
  institution: "Badulla Central College",
  location: "",
  dates: dates-helper(start-date: "Jan 2018", end-date: "Dec 2020"),
  degree: "G.C.E. A/Ls (Physical Science)"
)
- 3A's - Island Rank 179

#edu(
  institution: "Badulla Viharamahadevi Girls' College",
  location: "",
  dates: dates-helper(start-date: "Jan 2008", end-date: "Dec 2017"),
  degree: "G.C.E. O/Ls (General Education)"
)
- 9A's

#linebreak()

== Work Experience

#work(
  title: "Software Engineering Intern",
  location: "",
  company: "LSEG Technology",
  dates: dates-helper(start-date: "Dec 2024", end-date: "Present"),
)

#linebreak()

== Projects

#link("")[🔗]
#project(
  name: "AI-Enhanced Mental Health Journaling (EmoAI)",
  dates: dates-helper(start-date: "Jul 2024", end-date: "Dec 2024")
)
- Uses NLP to analyze emotional states, helping psychological professionals monitor their patients.
  - *Skills*: Python, Flask, React, Firebase, TensorFlow, Git

#link("")[🔗]
#project(
  name: "You Drink We Drive",
  dates: dates-helper(start-date: "Jun 2024", end-date: "Dec 2024")
)
- Replaced a WordPress site with a dynamic website for a safe ride service targeting intoxicated clients.
  - *Skills*: React, Spring Boot, MySQL, Hibernate ORM, Git

#link("")[🔗]
#project(
  name: "Interactive Data Preprocessing VS Code Extension",
  dates: dates-helper(start-date: "May 2024", end-date: "Present")
)
- A VS Code extension enabling interactive data cleaning and visualization.
  - *Skills*: JavaScript, Python, HTML, CSS, Azure, Git, GitHub Actions

#link("")[🔗]
#project(
  name: "Web Application for a Banking System (NEXUS Trust Bank)",
  dates: dates-helper(start-date: "Aug 2023", end-date: "Dec 2023")
)
- Built a transaction-based web app for banking features including loans and inter-account transactions.
  - *Skills*: React, Node.js, MySQL, Express.js, DigitalOcean, Git

#link("")[🔗]
#project(
  name: "Mobile App for Interplanetary Travelling (INFIX)",
  dates: dates-helper(start-date: "Aug 2023", end-date: "Aug 2023")
)
- An imaginary concept app allowing users to book trips and share travel memories.
  - *Skills*: React Native, Node.js, Express.js, PostgreSQL, Prisma, Git

#linebreak()

== Skills
- *Programming Languages*: Python, Java, JavaScript, C++
- *Web Development*: Node.js/TypeScript, React, Express.js, Spring Boot
- *Databases*: MySQL, PostgreSQL, SQLite, Prisma ORM, Hibernate ORM, MongoDB, Firestore
- *Machine Learning*: Scikit-learn, TensorFlow, MLFlow, DagsHub
- *Tools*: Git, GitHub, GitHub Desktop

#linebreak()

== Achievements

#certificates(
  name: "IEEEXtreme 2024",
  date: "2024"
)
- Country Rank 19

#certificates(
  name: "InspiHer V 2.0",
  date: "2024"
)
- Finalist Rank 5 - SLTC WIE club

#certificates(
  name: "IEEEXtreme 2023",
  date: "2023"
)
- Country Rank 34

#certificates(
  name: "MoraXTreme 2022",
  date: "2022"
)
- Rank 112

#certificates(
  name: "ML Olympiad",
  date: ""
)
- Public Rank 87

#certificates(
  name: "Home Credit - Credit Risk Model Stability",
  date: ""
)
- Public Rank

#certificates(
  name: "National Mathematics Competition",
  date: "2016"
)
- Qualified in 2016

#certificates(
  name: "All Island Drama Competition",
  date: "2015"
)
- Participant in 2015 & 2016

#certificates(
  name: "National Mathematics and Science Olympiad",
  date: "2012"
)
- Participated