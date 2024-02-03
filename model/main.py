import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import xgboost as xgb
import numpy as np
from matplotlib import pyplot

df = pd.read_json('../data-generation/out/training_data/diff-2022-2023.json')

features, target = df.drop(['matchOutcome'], axis=1), df[[
    'matchOutcome']]

categories = features.select_dtypes(exclude=np.number).columns.tolist()

# Convert to Pandas category
for col in categories:
    features[col] = features[col].astype('category')

features_train, features_test, target_train, target_test = train_test_split(
    features, target)

# print(df.info())
# Creating an XGBoost classifier
model = xgb.XGBClassifier(
    objective='multi:softprob',
    enable_categorical=True,
    eval_metric='mlogloss',
    use_label_encoder=False,
    num_boost_round=1000
)
# Training the model on the training data
model.fit(features_train, target_train)

# Making predictions on the test set
predictions = model.predict(features_test)

# Calculating accuracy
accuracy = accuracy_score(target_test, predictions)

print("Accuracy:", accuracy)
print("\nClassification Report:")
print(classification_report(target_test, predictions,
      target_names=['Loss', 'Draw', 'Win']))

pyplot.bar(range(len(model.feature_importances_)), model.feature_importances_)
pyplot.show()