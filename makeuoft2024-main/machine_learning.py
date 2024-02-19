# pip install scikit-learn
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import csv
def guessbin(input):
# Load the CSV file and read its contents
    foods = []
    categories = []
    with open('data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            foods.append(row['Food'])
            categories.append(row['Category'])

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(foods, categories, test_size=0.2, random_state=42)

    # Train the model
    text_clf = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', MultinomialNB()),
    ])
    text_clf.fit(X_train, y_train)

    # Test a sample sentence
    sample_sentence = input
    predicted_category = text_clf.predict([sample_sentence])[0]
    return(predicted_category)

    # Predict on the test set
    #predicted = text_clf.predict(X_test)

    # Print the classification report
    #print(classification_report(y_test, predicted))

    # Calculate and print F1 score, precision, and recall

#f1_score = text_clf.score(X_test, y_test)
#precision = text_clf.precision_score(X_test, y_test, average='macro')
#recall = text_clf.recall_score(X_test, y_test, average='macro')
#print("F1 score:", f1_score)
#print("Precision:", precision)
#print("Recall:", recall)

