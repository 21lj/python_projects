# Heart Disease Prediction Model

## Project Objective

The primary objective of this project is to develop a **predictive model** that can accurately determine the **presence of heart disease** in patients based on a set of medical attributes. This model is intended to support **early diagnosis** and **potential medical intervention**, which can improve patient outcomes and overall healthcare efficiency.

---

## Dataset

This project uses the **Heart Disease dataset** from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/heart+Disease). The dataset includes various patient health metrics such as:

- Age
- Sex
- Chest pain type
- Resting blood pressure
- Serum cholesterol
- Fasting blood sugar
- Resting electrocardiographic results
- Maximum heart rate achieved
- Exercise-induced angina
- ST depression
- And more

---

## Tools & Technologies

- **Programming Language**: Python
- **Development Environment**: Jupyter Notebook

### Libraries Used

| Library       | Purpose                                 |
|---------------|-----------------------------------------|
| `numpy`       | Numerical operations                    |
| `pandas`      | Data manipulation and analysis          |
| `scikit-learn`| Machine learning algorithms and tools   |

---

## Methodology

1. **Data Loading & Exploration**  
   Load the dataset and understand the structure, types, and distribution of features.

2. **Data Preprocessing**  
   Handle missing values, encode categorical variables, and normalize data if necessary.

3. **Data Splitting**  
   Use `sklearn.model_selection.train_test_split` to divide the data into training and test sets.

4. **Model Building**  
   Train a **Logistic Regression** model using `sklearn.linear_model.LogisticRegression` to predict the presence of heart disease.

5. **Model Evaluation**  
   Assess the model’s performance using accuracy, confusion matrix, precision, recall, and F1 score.

---

## Results

The Logistic Regression model provides a baseline for classification performance. It is evaluated on how well it can predict heart disease using the available medical attributes.



---
