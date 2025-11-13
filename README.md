---
title: Resumate Resume Text Classifier
emoji: 📄
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: "1.29.0"  # replace with your Streamlit version
app_file: ui/Overview.py   # path to your main app file
pinned: false
---
# Resumate

<div align="center">

<img src="https://i.postimg.cc/gJgcPvkZ/Chat-GPT-Image-May-8-2025-04-32-36-PM.png" width="150px">

**BERT-based resume text classification app**

------

<p align="center">
<a href="#About">About</a> •
  <a href="#features">Features</a> •
<a href="#Installation">Installation</a> 


</div>

![version](https://img.shields.io/badge/version-v1.0.0-blue)

## About
A Python application that uses a BERT-based model to classify PDF resumes into 7 categories: Education (Edu), Personal Information (PI), Experience (Exp), Objective (Obj), Summary (Sum), Skills (Skill), and Qualifications/Certifications (QC). Features a Streamlit web interface for easy use.

## Features
- **PDF Resume Processing**: Extracts text from uploaded PDF files
- **BERT Classification**: Uses transformer models for accurate text classification
- **Interactive UI**: Simple web interface built with Streamlit
- **7-Category System**: Clear labeling of resume components

## Installation
#### Prerequisites: 
- **Python 3.8 or higher**
- pip package manager



#### Install dependencies:

```shell
pip install -r requirements.txt
```

#### Run the app using:

```shell
streamlit run app.py
```


## In the web browser
- Upload a PDF resume file
- View the extracted text
- See classification results
- Optionally download results as JSON



