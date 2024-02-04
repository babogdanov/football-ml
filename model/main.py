import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import xgboost as xgb
from xgboost import plot_importance, plot_tree
import numpy as np
from matplotlib import pyplot

xgb.config_context(
    verbosity=3,
)

MAX_ACCURACY = 0.719
df = pd.read_json('../data-generation/out/training_data/diff-2022-2023.json')

features, target = df.drop(['matchOutcome', 'team_one_id', 'team_two_id', 'team_one_name', 'team_two_name'], axis=1), df[[
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

    #enable_categorical=True,
    #eval_metric='mlogloss',
    #use_label_encoder=False,
)

# Training the model on the training data
#model.fit(features_train, target_train)

model.load_model('./best_xgb_model.json')
# Making predictions on the test set
predictions = model.predict(features_test)

# Calculating accuracy
accuracy = accuracy_score(target_test, predictions)

if accuracy > MAX_ACCURACY:
    model.save_model('best_xgb_model.json')

print("Accuracy:", accuracy)
print("\nClassification Report:")
print(classification_report(target_test, predictions,
      target_names=['Loss', 'Draw', 'Win']))

plot_tree(model)
plot_importance(model)
pyplot.show()

# TODO: remove name and id fields