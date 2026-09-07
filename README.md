Overview of Project 1


A simple rule-based chatbot built in Python that responds to predefined user inputs using dictionary-based intent matching. This project is the foundation module for the AI Engineer training track, focused on control flow, decision-making logic, and basic AI concepts — no machine learning involved yet.

Goal

Create a chatbot that can:

Handle greetings and exit commands
Match user input to predefined responses
Run in a continuous loop until the user exits
Key Concepts Demonstrated
Concept	Where it's used
Input sanitization	.strip().lower() normalizes case and whitespace
Continuous loop	while True: keeps the bot "alive" until a kill command
Dictionary lookup (O(1))	responses dict replaces a slow if-elif ladder (O(n))
Fallback handling	dict.get(key, default) returns a default reply for unknown input
Exit strategy	A dedicated exit_commands set breaks the loop cleanly
Why Dictionary Lookup Instead of If-Elif?

An if-elif ladder checks conditions one by one — the more rules you add, the slower and messier it gets (linear complexity, high technical debt). A dictionary gives instant, constant-time lookup regardless of how many intents you support, and using .get() combines the lookup and fallback into a single clean operation.

Requirements
Python 3.x
No external libraries needed
How to Run
bash
python chatbot.py

Then type messages at the You: prompt. Type bye, exit, or quit to end the conversation.

Example Interaction
Bot: Hi! I'm a simple chatbot. Type 'bye' to exit.
You: hello
Bot: Hello there! How can I help you?
You: what's your name
Bot: Sorry, I didn't understand that. Try again?
You: your name
Bot: I'm ChatBot 1.0, nice to meet you!
You: bye
Bot: Goodbye! Have a great day!
Project Structure
.
├── chatbot.py      # Main chatbot script
└── README.md       # This file
Ideas for Extension
Expand the vocabulary with more intents (aim for 5+ as required)
Add nested conditions for multi-step conversations (e.g. asking follow-up questions)
Give the bot a distinct personality in its replies
Handle partial matches or keywords instead of exact phrases
Add simple logging of conversation history to a file

Skills Practiced
Control flow, decision-making logic, dictionaries/hash maps, input handling, and the fundamentals that underpin more advanced "AI guardrail" and hybrid rule+LLM architectures covered later in the track.


Overview of Project 2

Goal

Build a basic classification model using a small dataset, moving from rule-based logic (Project 1) into supervised learning.

Key Requirements
Load and understand a dataset
Split data into training and testing sets
Apply a simple classification algorithm
Key Skills

Data handling, supervised learning basics, model training

Pipeline (IPO Framework)
Stage	What Happens
Input	Load the Iris dataset (150 samples, 3 classes, 4 features) and apply feature scaling with StandardScaler (mean = 0, variance = 1)
Process	Split data 80/20 into train/test sets, then train a K-Nearest Neighbors (KNN) classifier with k = 5
Output	Evaluate with a confusion matrix and F1 score — accuracy alone can be misleading ("the accuracy mirage"), especially on imbalanced data
Dataset

The classic Iris flower dataset:

150 samples, perfectly balanced across 3 classes
4 numeric features: sepal length, sepal width, petal length, petal width
3 target classes: setosa, versicolor, virginica
Files
data_classifier.py — main script (loads data, scales, splits, trains, evaluates)
How to Run
bash
pip install scikit-learn pandas
python data_classifier.py
Sample Output
=== Dataset Overview ===
Samples: 150, Features: 4, Classes: 3

=== Train/Test Split ===
Training samples: 120, Testing samples: 30

=== Output Validation ===
Accuracy: 93.3%
F1 Score (weighted): 0.933

Confusion Matrix:
            setosa  versicolor  virginica
setosa          10           0          0
versicolor       0           9          1
virginica        0           1          9
Why Feature Scaling Matters

KNN relies on distance calculations between points. Without scaling, features with larger numeric ranges would dominate the distance metric. StandardScaler normalizes all features to the same scale before training.

Why Not Just Accuracy?

On imbalanced datasets, a model can score high accuracy while completely failing on a minority class. The confusion matrix and F1 score expose this by showing per-class performance (true positives, false positives, false negatives) instead of a single blended number.

Possible Extensions
Try different values of k and plot the error rate (the "elbow method") to find the optimal k
Compare KNN against other simple algorithms (Decision Tree, Logistic Regression)
Test the model on a completely new, unseen dataset
Add k-fold cross-validation for more robust evaluation

