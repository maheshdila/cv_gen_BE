#import "@preview/basic-resume:0.2.8": *

// Personal Information
#let full-name = "Ramindu Abeygunawardane"

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
    phone: #link("tel:+94 76 980 7626") \
    address: Galle, Sri Lanka
  ],
  align(center)[
    #link("mailto:ramindu.21@cse.mrt.ac.lk") \
    #link("https://www.google.com/") 
  ],
  align(center)[
    #link("https://github.com/RaminduA")[GitHub] \
    #link("https://www.linkedin.com/in/Ramindu-Abeygunawardane/")[LinkedIn] 
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
  dates: dates-helper(start-date: "Aug 2022", end-date: "Present"),
  degree: "BSc. Engineering (Hons) (Data Science and Engineering)"
)
- Current CGPA: 3.209

#edu(
  institution: "Institute of Java and Software Engineering",
  location: "",
  dates: dates-helper(start-date: "Dec 2020", end-date: "Present"),
  degree: "Diploma in Software Engineering"
)

#edu(
  institution: "Mahinda College",
  location: "",
  dates: dates-helper(start-date: "Jan 2018", end-date: "Dec 2020"),
  degree: "G.C.E. A/L (Physical Science)"
)
- 3A's

#edu(
  institution: "Mahinda College",
  location: "",
  dates: dates-helper(start-date: "Jan 2006", end-date: "Dec 2016"),
  degree: "G.C.E. O/L (General Education)"
)
- 9A's

#linebreak()

== Work Experience

#work(
  title: "Trainee Software Engineer",
  location: "",
  company: "ZeroBeta Private Limited",
  dates: dates-helper(start-date: "Dec 2024", end-date: "Present"),
)

#work(
  title: "Fullstack Developer (Freelance)",
  location: "",
  company: "Self-employed",
  dates: dates-helper(start-date: "Jan 2023", end-date: "Present"),
)

#linebreak()

== Projects

#link("https://www.google.com/")[🔗]
#project(
  name: "Dr. Derm - AI-based Skincare App",
  dates: dates-helper(start-date: "Jul 2024", end-date: "Present")
)
- Developed ML models with Fast API and T4-GPU for skin condition analysis using large datasets; built a Flutter UI for real-time results.
  - *Skills*: Python, Fast API, Node.js, TensorFlow, T4-GPU, Flutter, Firebase

#link("https://www.google.com/")[🔗]
#project(
  name: "Godadamu LMS",
  dates: dates-helper(start-date: "May 2024", end-date: "Present")
)
- Developed a scalable LMS platform with authentication, course management, and email notification using AWS EC2 and GitHub Actions.
  - *Skills*: Node.js, TypeScript, Express.js, EJS, Nodemailer, GitHub Actions, AWS EC2

#link("https://www.google.com/")[🔗]
#project(
  name: "MARTY Mart - Single Vendor E-Commerce Site",
  dates: dates-helper(start-date: "Sep 2023", end-date: "Nov 2023")
)
- Built a Spring Boot-based e-commerce site with layered architecture and MySQL for data management.
  - *Skills*: Java, Spring Boot, JPA, Lombok, MySQL

#linebreak()

== Skills
- *Programming Languages*: Java, Python, JavaScript, C++, Dart
- *Machine Learning / AI Frameworks*: TensorFlow, PyTorch, Keras, Scikit-learn
- *Data Analysis*: Pandas, NumPy, SQL, Hadoop
- *Deep Learning*: CNNs, RNNs, LSTMs
- *Cloud Platforms*: AWS, Google Cloud, Firebase
- *Dev Tools*: Jupyter Notebook, Google Colab, Kaggle, Fast API
- *Other Technologies*: RESTful APIs, Matplotlib, Seaborn

#linebreak()

== Achievements

#certificates(
  name: "Bronze Medal - Sri Lanka Physics Olympiad",
  date: "2019"
)
- 2019

#certificates(
  name: "Honourable Mention - Sri Lanka Mathematics Olympiad",
  date: "2017"
)
- 2017

#certificates(
  name: "Second Prize - Open Mathematical Olympiad for University Students",
  date: "2022"
)
- IUHD

#linebreak()

== Certifications

#link("https://www.google.com/")[🔗]
#certificates(
  name: "AWS Academy Machine Learning Foundations",
  issuer: "AWS Academy",
  date: "2024-02"
)

#linebreak()

== References
        
#grid(
  columns: (1fr, 1fr),
  align(left)[
    *Prof. Dulani Meedeniya* \
    _Senior Lecturer_, \
    _University of Moratuwa_ \
    email: #link("mailto:dulanim@cse.mrt.ac.lk") \
    phone: #link("tel:+94 71 393 5801") \
  ],
  align(left)[
    *Dr. H.H.S.R. Samarasiri* \
    _Senior Lecturer_, \
    _University of Moratuwa_ \
    email: #link("mailto:supems@uom.lk") \
    phone: #link("tel:+94 77 362 8983") \
  ]
)