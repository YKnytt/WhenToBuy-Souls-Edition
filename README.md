\# 🎮 WHEN TO BUY — Souls Edition



\### Steam Price Intelligence + Machine Learning for FromSoftware Games



\*\*WhenToBuy — Souls Edition\*\* is an interactive price-intelligence application that uses historical Steam pricing data and machine learning to help answer a simple question:



> \*\*Should I buy this game now, or is there evidence that waiting could lead to a lower price?\*\*



The project combines data cleaning, time-series feature engineering, machine learning, and an interactive Streamlit interface into a single end-to-end application.



\---



\## 🎯 The Problem



Gamers often know they want a game, but deciding \*\*when to purchase it\*\* can be difficult.



A current price by itself does not provide much context. A $59.99 price could mean something very different if:



\- The historical low is $35.99

\- The game has gone on sale several times recently

\- The current price has remained unchanged for months

\- Similar price patterns have historically been followed by another discount



WhenToBuy transforms historical pricing behavior into features that can be used to estimate whether a lower price may occur within the next 30 days.



\---



\## 🎮 Supported Games



The current application includes six FromSoftware titles:



\- Elden Ring

\- Elden Ring Nightreign

\- Dark Souls II

\- Dark Souls III

\- Dark Souls Remastered

\- Sekiro: Shadows Die Twice



Additional games were used during data exploration and development.



\---



\## 🧠 How It Works



The project follows an end-to-end machine learning pipeline:



```text

Steam Price History

&#x20;       ↓

Data Cleaning

&#x20;       ↓

Daily Price Dataset

&#x20;       ↓

Feature Engineering

&#x20;       ↓

Chronological Train/Test Split

&#x20;       ↓

Game-Specific ML Model

&#x20;       ↓

Saved Model

&#x20;       ↓

Streamlit Application

&#x20;       ↓

Customer-Facing Prediction

