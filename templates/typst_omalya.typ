#import "@preview/basic-resume:0.2.8": *

// Put your personal information here, replacing mine
#let name = "Omalya Vidushini"
#let location = "Katubedda, Moratuwa"
#let email = "omalya.21@cse.mrt.ac.lk"
#let github = "https://github.com/OmalyaV"
#let linkedin = "https://linkedin.com/in/omalya-vidushini"
#let phone = "+94702104088"
#let personal-site = ""

#show: resume.with(
  author: name,
  // All the lines below are optional.
  // For example, if you want to to hide your phone number:
  // feel free to comment those lines out and they will not show.
  location: location,
  email: email,
  github: github,
  linkedin: linkedin,
  phone: phone,
  personal-site: personal-site,
  accent-color: "#26428b",
  font: "New Computer Modern",
  paper: "us-letter",
  author-position: left,
  personal-info-position: left,
)

/*
* Lines that start with == are formatted into section headings
* You can use the specific formatting functions if needed
* The following formatting functions are listed below
* #edu(dates: "", degree: "", gpa: "", institution: "", location: "", consistent: false)
* #work(company: "", dates: "", location: "", title: "")
* #project(dates: "", name: "", role: "", url: "")
* certificates(name: "", issuer: "", url: "", date: "")
* #extracurriculars(activity: "", dates: "")
* There are also the following generic functions that don't apply any formatting
* #generic-two-by-two(top-left: "", top-right: "", bottom-left: "", bottom-right: "")
* #generic-one-by-two(left: "", right: "")
*/
== Education

#edu(
  institution: "University of Moratuwa",
  location: "",
  dates: dates-helper(start-date: "2022-01", end-date: "Present"),
  degree: "BSc. Engineering (Hons) (Computer Science and Engineering - Data Science & Engineering)"
)
- Current CGPA: 3.71

#edu(
  institution: "Badulla Central College",
  location: "",
  dates: dates-helper(start-date: "2018-01", end-date: "2020-12"),
  degree: "G.C.E. A/Ls (Physical Science)"
)
- 3Aâ€™s - Island Rank 179

#edu(
  institution: "Badulla Viharamahadevi Girlsâ€™ College",
  location: "",
  dates: dates-helper(start-date: "2008-01", end-date: "2017-12"),
  degree: "G.C.E. O/Ls (General Education)"
)
- 9Aâ€™s
== Work Experience
        
#work(
  title: "Software Engineering Intern",
  location: "",
  company: "LSEG Technology",
  dates: dates-helper(start-date: "2024-12", end-date: "Present"),
)
- 
== Projects
        
#project(
  name: "AI-Enhanced Mental Health Journaling (EmoAI)",
  dates: dates-helper(start-date: "2024-07", end-date: "2024-12"),
  url: ""
)
- Uses NLP to analyze emotional states, helping psychological professionals monitor their patients.
- *Skills*: Python, Flask, React, Firebase, TensorFlow, Git
        
#project(
  name: "You Drink We Drive",
  dates: dates-helper(start-date: "2024-06", end-date: "2024-12"),
  url: ""
)
- Replaced a WordPress site with a dynamic website for a safe ride service targeting intoxicated clients.
- *Skills*: React, Spring Boot, MySQL, Hibernate ORM, Git
        
#project(
  name: "Interactive Data Preprocessing VS Code Extension",
  dates: dates-helper(start-date: "2024-05", end-date: ""),
  url: ""
)
- A VS Code extension enabling interactive data cleaning and visualization.
- *Skills*: JavaScript, Python, HTML, CSS, Azure, Git, GitHub Actions
        
#project(
  name: "Web Application for a Banking System (NEXUS Trust Bank)",
  dates: dates-helper(start-date: "2023-08", end-date: "2023-12"),
  url: ""
)
- Built a transaction-based web app for banking features including loans and inter-account transactions.
- *Skills*: React, Node.js, MySQL, Express.js, DigitalOcean, Git
        
#project(
  name: "Mobile App for Interplanetary Travelling (INFIX)",
  dates: dates-helper(start-date: "2023-08", end-date: "2023-08"),
  url: ""
)
- An imaginary concept app allowing users to book trips and share travel memories.
- *Skills*: React Native, Node.js, Express.js, PostgreSQL, Prisma, Git
== Skills

- *Programming Languages*: Python,Java,JavaScript,C++
- *Web Development*: Node.js/TypeScript,React,Express.js,Spring Boot
- *Databases*: MySQL,PostgreSQL,SQLite,Prisma ORM,Hibernate ORM,MongoDB,Firestore
- *Machine Learning*: Scikit-learn,TensorFlow,MLFlow,DagsHub
- *Tools*: Git,GitHub,GitHub Desktop

