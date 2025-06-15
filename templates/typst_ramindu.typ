#import "@preview/basic-resume:0.2.8": *
        
// Personal Information"
#let full-name = "Ramindu Abeygunawardane"
#let address = "Galle, Sri Lanka"
#let email = "ramindu.21@cse.mrt.ac.lk"
#let github = "https://github.com/RaminduA"
#let linkedin = "https://www.linkedin.com/in/Ramindu-Abeygunawardane/"
#let phone = "+94 76 980 7626"
#let portfolio = ""

#show: resume.with(
  author: full-name,
  location: address,
  email: email,
  github: github,
  linkedin: linkedin,
  phone: phone,
  personal-site: portfolio,
  accent-color: "#26428b",
  font: "New Computer Modern",
  paper: "us-letter",
  author-position: center,
  personal-info-position: left,
)

== Overview

Enthusiastic Data Science and Engineering student with practical experience in AI and ML fields, specializing in Python and TensorFlow. Skilled in building and optimizing machine learning algorithms for real-world applications, with a focus on data analysis and management. Eager to contribute to ML model development for real-world applications and leverage hands-on experience.

== Education

#edu(
  institution: "University of Moratuwa",
  location: "",
  dates: dates-helper(start-date: "2022-08", end-date: "Present"),
  degree: "BSc. Engineering (Hons) (Data Science and Engineering)"
)
  - Current CGPA: 3.209

#edu(
  institution: "Institute of Java and Software Engineering",
  location: "",
  dates: dates-helper(start-date: "2020-12", end-date: "Present"),
  degree: "Diploma in Software Engineering "
)

#edu(
  institution: "Mahinda College",
  location: "",
  dates: dates-helper(start-date: "2018-01", end-date: "2020-12"),
  degree: "G.C.E. A/L (Physical Science)"
)
  - 3A's

#edu(
  institution: "Mahinda College",
  location: "",
  dates: dates-helper(start-date: "2006-01", end-date: "2016-12"),
  degree: "G.C.E. O/L (General Education)"
)
  - 9A's

== Work Experience
        
#work(
  title: "Trainee Software Engineer",
  location: "",
  company: "ZeroBeta Private Limited",
  dates: dates-helper(start-date: "2024-12", end-date: "Present"),
)
        
#work(
  title: "Fullstack Developer (Freelance)",
  location: "",
  company: "Self-employed",
  dates: dates-helper(start-date: "2023-01", end-date: "Present"),
)

== Projects
        
#project(
  name: "Dr. Derm - AI-based Skincare App",
  dates: dates-helper(start-date: "2024-07", end-date: "Present"),
  url: ""
)
- Developed ML models with Fast API and T4-GPU for skin condition analysis using large datasets; built a Flutter UI for real-time results.
  - *Skills*: Python, Fast API, Node.js, TensorFlow, T4-GPU, Flutter, Firebase
        
#project(
  name: "Godadamu LMS",
  dates: dates-helper(start-date: "2024-05", end-date: "Present"),
  url: ""
)
- Developed a scalable LMS platform with authentication, course management, and email notification using AWS EC2 and GitHub Actions.
  - *Skills*: Node.js, TypeScript, Express.js, EJS, Nodemailer, GitHub Actions, AWS EC2
        
#project(
  name: "MARTY Mart - Single Vendor E-Commerce Site",
  dates: dates-helper(start-date: "2023-09", end-date: "2023-11"),
  url: ""
)
- Built a Spring Boot-based e-commerce site with layered architecture and MySQL for data management.
  - *Skills*: Java, Spring Boot, JPA, Lombok, MySQL

== Skills
- *Programming Languages*: Java, Python, JavaScript, C++, Dart
- *Machine Learning / AI Frameworks*: TensorFlow, PyTorch, Keras, Scikit-learn
- *Data Analysis*: Pandas, NumPy, SQL, Hadoop
- *Deep Learning*: CNNs, RNNs, LSTMs
- *Cloud Platforms*: AWS, Google Cloud, Firebase
- *Dev Tools*: Jupyter Notebook, Google Colab, Kaggle, Fast API
- *Other Technologies*: RESTful APIs, Matplotlib, Seaborn

== Certifications
        
#certificates(
  name: "AWS Academy Machine Learning Foundations",
  issuer: "AWS Academy",
  date: "2024-02",
  url: ""
)