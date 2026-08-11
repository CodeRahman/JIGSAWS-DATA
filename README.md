# Human Skill Estimation from Kinematic Motion

Machine learning-based estimation of human skill from kinematic movement features, developed during the **NSF REU SITE: HUMANS MOVE** program at the **University of Wyoming**.

This project investigates whether general characteristics of human motion can be used to estimate skill, with the long-term goal of supporting adaptive shared-autonomy systems in assistive robotics.

---

## Overview

Assistive robotic systems often provide a fixed or manually selected level of assistance. A system capable of estimating a user's skill from their movement could eventually adapt its behavior according to the user's current ability.

This project focuses on the **skill-estimation component** of that broader problem.

Using the **JHU-ISI Gesture and Skill Assessment Working Set (JIGSAWS)**, I developed an end-to-end machine learning pipeline to:

- Process robotic kinematic data
- Extract interpretable movement features
- Analyze relationships between motion and skill
- Train regression models to predict skill scores
- Evaluate generalization to unseen subjects
- Investigate which movement characteristics contribute most to prediction

---

## Research Question

> **Can task-independent characteristics of human movement be used to estimate skill using machine learning?**

A secondary question is whether such a skill estimator could eventually serve as an input to an adaptive shared-autonomy system.

---

## Research Pipeline

```text
JIGSAWS Kinematic Data
        │
        ▼
Data Processing
        │
        ▼
Feature Extraction
        │
        ├── Speed
        ├── Acceleration
        ├── Jerk
        ├── Idle Behavior
        └── Duration
        │
        ▼
Exploratory Data Analysis
        │
        ▼
Machine Learning Regression
        │
        ▼
Subject-Independent Evaluation
        │
        ▼
Estimated Skill Score
```

---

## Dataset

The project uses the **JIGSAWS dataset**, which contains robotic surgical activity collected using the da Vinci Surgical System.

Three tasks were analyzed:

| Task | Trials |
|---|---:|
| Knot Tying | 36 |
| Needle Passing | 28 |
| Suturing | 39 |
| **Total** | **103** |

Although JIGSAWS originates from robot-assisted surgery, this project emphasizes **general characteristics of movement** rather than surgical trajectory-specific features.

### Prediction Target

Skill estimation is formulated as a regression problem using the **Global Rating Scale (GRS) Total Score**.

The GRS consists of six dimensions:

- Respect for tissue
- Suture/needle handling
- Time and motion
- Flow of operation
- Overall performance
- Quality of final product

Each component is scored from 1 to 5, giving a total score between **6 and 30**.

---

## Feature Engineering

Features were extracted independently from the left and right manipulators.

### Speed

- Mean speed
- Median speed
- Maximum speed
- Speed standard deviation

### Acceleration

- Mean acceleration
- Median acceleration
- Maximum acceleration
- Acceleration standard deviation

### Jerk / Smoothness

- Mean jerk
- Median jerk
- Maximum jerk
- Jerk standard deviation

### Idle Behavior

- Idle time
- Idle ratio

### Trial-Level Information

- Trial duration

The final modeling dataset contains **29 engineered movement features**.

The emphasis is on features that may be less dependent on the geometry of a specific task than measures such as raw path length.

---

## Exploratory Data Analysis

Exploratory analysis was performed before model training to understand the structure of the extracted feature dataset.

The analysis includes:

- Descriptive statistics
- Missing-value checks
- Feature distributions
- Skewness analysis
- IQR-based outlier detection
- Feature correlations
- Relationships between features and GRS scores
- Comparisons across skill levels
- Comparisons across tasks
- Comparisons across subjects

EDA outputs are available in:

```text
results/eda/
```

---

## Machine Learning Models

The following regression models were evaluated:

- Ridge Regression
- Elastic Net
- Random Forest
- Extra Trees
- Gradient Boosting
- Support Vector Regression

A **Dummy Regressor** was included as a baseline.

The best-performing nonlinear models were then tuned and evaluated again.

---

## Subject-Independent Evaluation

One of the most important design decisions in the project was avoiding subject leakage.

Trials from the same participant were not allowed to appear in both training and testing data within an evaluation fold.

The central evaluation question therefore becomes:

> **Can the model estimate the skill of a person it did not see during training?**

This makes the evaluation substantially more difficult, but also more representative of how a practical skill-estimation system would need to operate.

---

# Results

## Initial Model Comparison

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Random Forest | **4.345** | 5.367 | 0.073 |
| Extra Trees | 4.424 | 5.463 | 0.039 |
| Gradient Boosting | 4.750 | 5.975 | -0.149 |
| Dummy Regressor | 4.907 | 5.786 | -0.078 |
| Support Vector Regression | 4.936 | 5.849 | -0.101 |
| Elastic Net | 5.131 | 6.214 | -0.243 |
| Ridge Regression | 5.595 | 6.758 | -0.470 |

Random Forest produced the lowest MAE before hyperparameter tuning.

---

## Best Tuned Model

After hyperparameter tuning, **Gradient Boosting achieved the strongest overall performance**:

| Metric | Result |
|---|---:|
| **MAE** | **4.299** |
| **RMSE** | **5.193** |
| **R²** | **0.132** |

The tuned model demonstrates that the engineered movement features contain some predictive information about skill under subject-independent evaluation.

![Actual vs Predicted Skill](results/modeling/actual_vs_predicted_gradient_boosting.png)

The positive R² indicates that the model captures some relationship between the engineered kinematic features and GRS skill scores.

At the same time, the relatively low R² shows that simple trial-level summary statistics explain only a limited portion of the variance in skill.

This result suggests that **human skill appears to be reflected in movement, but it is not fully represented by a small collection of handcrafted summary features.**

---

## Feature Importance

Permutation feature importance was used to investigate which individual motion features contributed most strongly to Gradient Boosting predictions.

The strongest mean importance values included:

| Feature | Mean Importance |
|---|---:|
| Left Speed Standard Deviation | **0.263** |
| Left Jerk Standard Deviation | **0.156** |
| Right Idle Ratio | **0.089** |
| Right Median Speed | **0.079** |
| Left Acceleration Standard Deviation | **0.077** |

These results suggest that **movement variability, smoothness, and idle behavior** contain useful information for estimating skill.

![Feature Importance](results/modeling/poster_feature_importance.png)

---

## Key Findings

### 1. Kinematic movement contains information about skill

The best subject-independent model achieved a positive R², suggesting that motion-derived features contain measurable information associated with GRS skill.

### 2. Generalization to unseen individuals is difficult

The evaluation setup intentionally requires models to predict skill for subjects not observed during training.

This is a considerably harder problem than randomly splitting individual trials.

### 3. Movement variability appears important

Speed and jerk variability were among the strongest individual predictors in the final Gradient Boosting model.

### 4. Idle behavior may contain useful skill information

The importance of idle-related features suggests that pauses or periods of low movement may help distinguish different patterns of task execution.

### 5. Handcrafted summary statistics are not sufficient

The final R² of **0.132** indicates that most of the variation in GRS scores remains unexplained by the current feature representation.

This motivates future approaches that preserve more of the temporal structure of human movement.

---

## Limitations

### Small Dataset

The study contains only 103 trials, limiting the amount of data available for training and evaluation.

### Limited Number of Subjects

Subject-independent validation significantly reduces the amount of training data available within each fold.

### Surgical Domain

JIGSAWS contains surgical manipulation tasks.

Although the selected features were intended to describe more general movement characteristics, additional non-surgical datasets would be needed to determine whether the findings generalize to broader assistive-robotics applications.

### Handcrafted Features

Each entire trial is compressed into summary statistics.

This removes much of the temporal structure contained in the original motion.

Two users may produce similar average speeds or accelerations while exhibiting very different sequences of movement.

### Skill Label

GRS was designed to assess surgical skill rather than general-purpose human motor ability.

Future work should explore alternative skill representations better suited to broader human-robot interaction.

---

## Future Work

Potential extensions include:

- Evaluating the feature framework on non-surgical manipulation datasets
- Collecting more task-independent human manipulation data
- Investigating coordination between the left and right manipulators
- Introducing additional movement-efficiency and smoothness measures
- Modeling full temporal sequences rather than trial-level statistics
- Investigating sequence models for kinematic data
- Developing task-normalized skill representations
- Estimating skill in real time
- Integrating skill estimates into adaptive shared-autonomy controllers

The long-term vision is:

```text
Human Motion
     │
     ▼
Skill Estimator
     │
     ▼
Estimated User Skill
     │
     ▼
Shared-Autonomy Controller
     │
     ▼
Adaptive Robotic Assistance
```

---

## Repository Structure

```text
JIGSAWS-DATA/
│
├── raw/
│   └── Raw JIGSAWS kinematic data
│
├── processed/
│   └── Processed trial data
│
├── features/
│   └── Extracted feature dataset
│
├── scripts/
│   ├── convert.py
│   ├── columns.py
│   ├── eda.py
│   ├── feature_extraction.py
│   ├── features_dataset_eda.py
│   └── validate_features.py
│
├── results/
│   ├── eda/
│   └── modeling/
│
├── documents/
│
├── model_training.ipynb
├── .gitignore
└── README.md
```

---

## Technologies

- Python
- pandas
- NumPy
- scikit-learn
- Matplotlib
- Jupyter Notebook
- Git
- GitHub

---

## Research Context

This project was completed during the **NSF REU SITE: HUMANS MOVE** program at the **University of Wyoming** in Summer 2026.

The work was conducted in the **Robotics & Intelligent Systems Lab**.

### Researcher

**Abdurrahman Oyediran**  
Computer Science  
University of Southern Mississippi

### Mentorship

- Dr. Chao Jiang
- Umur Atan
- Varun Bharadwaj

---

## Acknowledgments

I would like to thank my mentors and the HUMANS MOVE REU program for their guidance and support throughout this project.

This project uses the **JHU-ISI Gesture and Skill Assessment Working Set (JIGSAWS)**. Credit for the original dataset belongs to its creators and associated institutions.

---

## Disclaimer

This project is an undergraduate research prototype intended to investigate machine learning methods for human skill estimation.

The models presented here are **not clinical assessment systems** and should not be interpreted as validated measures of surgical competence.

---

## Project Status

**Completed initial study — Summer 2026.**

Current directions include richer temporal representations of movement and investigating how skill estimation could eventually inform adaptive shared-autonomy systems.