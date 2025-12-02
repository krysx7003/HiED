import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

data = pd.read_csv("heart.csv")

categorical_cols = ["Sex", "ChestPainType", "RestingECG", "ExerciseAngina", "ST_Slope"]
data_encoded = pd.get_dummies(data, columns=categorical_cols, drop_first=True)

X = data_encoded.drop("HeartDisease", axis=1)
y = data_encoded["HeartDisease"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

models = {
    "decision_tree": DecisionTreeClassifier(random_state=42),
    "random_forest": RandomForestClassifier(random_state=42),
    "svc": SVC(probability=True, random_state=42),
    "logistic_reg": LogisticRegression(random_state=42, max_iter=1000),
}

results = {}
for name, model in models.items():
    if name in ["svc", "logistic_reg"]:
        X_tr, X_te = X_train_scaled, X_test_scaled
    else:
        X_tr, X_te = X_train, X_test

    model.fit(X_tr, y_train)

    y_pred = model.predict(X_te)
    y_pred_proba = model.predict_proba(X_te)[:, 1] if hasattr(model, "predict_proba") else None

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba) if y_pred_proba is not None else None

    results[name] = {
        "model": model,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "roc_auc": roc_auc,
        "y_pred": y_pred,
        "y_pred_proba": y_pred_proba,
    }

results_df = pd.DataFrame(
    {
        "Model": list(results.keys()),
        "Accuracy": [results[m]["accuracy"] for m in results],
        "Precision": [results[m]["precision"] for m in results],
        "Recall": [results[m]["recall"] for m in results],
        "F1-Score": [results[m]["f1"] for m in results],
        "ROC-AUC": [results[m]["roc_auc"] if results[m]["roc_auc"] else np.nan for m in results],
    }
)


name_mapping = {
    "decision_tree": "Drzewo\ndecyzyjne",
    "random_forest": "Las\nlosowy",
    "svc": "Maszyna wektorów\nnośnych",
    "logistic_reg": "Regresja\nlogistyczna",
}
metrics_plot = results_df.set_index("Model")[["Accuracy", "Precision", "Recall", "F1-Score"]]
metrics_plot.index = [name_mapping.get(name, name) for name in metrics_plot.index]

plt.figure(figsize=(10, 6))
metrics_plot.plot(kind="bar", width=0.8)

plt.ylabel("Wartość")
plt.legend(loc="lower right")
plt.grid(True, alpha=0.3)

plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("porownanie_modeli_1.png", dpi=300, bbox_inches="tight")
plt.show()

plt.figure(figsize=(10, 6))
for name, res in results.items():
    if res["roc_auc"] is not None and res["y_pred_proba"] is not None:
        fpr, tpr, _ = roc_curve(y_test, res["y_pred_proba"])
        plt.plot(fpr, tpr, lw=2, label=f"{name} (AUC = {res['roc_auc']:.3f})")

plt.plot([0, 1], [0, 1], "k--", lw=1, label="Random Classifier")
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.legend(loc="lower right")
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("porownanie_modeli_2.png", dpi=300, bbox_inches="tight")
plt.show()


plt.figure(figsize=(10, 6))
tree_model = results["decision_tree"]["model"]
feature_importance_tree = pd.Series(tree_model.feature_importances_, index=X.columns)
top_features_tree = feature_importance_tree.sort_values(ascending=False).head(10)
top_features_tree.plot(kind="barh", color="skyblue")
plt.xlabel("Ważność cechy")

plt.tight_layout()
plt.savefig("ważność_cech_tree.png", dpi=300, bbox_inches="tight")
plt.show()

rf_model = results["random_forest"]["model"]
feature_importance_rf = pd.Series(rf_model.feature_importances_, index=X.columns)
top_features_rf = feature_importance_rf.sort_values(ascending=False).head(10)
top_features_rf.plot(kind="barh", color="lightgreen")
plt.xlabel("Ważność cechy")

plt.tight_layout()
plt.savefig("ważność_cech_forest.png", dpi=300, bbox_inches="tight")
plt.show()

lr_model = results["logistic_reg"]["model"]
feature_coef = pd.Series(lr_model.coef_[0], index=X.columns)
top_coef = feature_coef.abs().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 6))
top_coef.plot(kind="barh", color="salmon")
plt.xlabel("Wartość bezwzględna współczynnika")
plt.tight_layout()
plt.savefig("ważność_cech_lr.png", dpi=300, bbox_inches="tight")
plt.show()

best_model_f1 = results_df.loc[results_df["F1-Score"].idxmax(), "Model"]
best_f1_score = results_df["F1-Score"].max()

best_model_acc = results_df.loc[results_df["Accuracy"].idxmax(), "Model"]
best_acc_score = results_df["Accuracy"].max()


print(results_df)

print("\nNajlepszy model według F1-Score (zbalansowany):")
print(f"   • Model: {best_model_f1}")
print(f"   • F1-Score: {best_f1_score:.4f}")

print("\nNajlepszy model według Accuracy:")
print(f"   • Model: {best_model_acc}")
print(f"   • Accuracy: {best_acc_score:.4f}")

print("\nNajważniejsze cechy według modeli drzewiastych:")
common_features = set(top_features_tree.head(5).index) & set(top_features_rf.head(5).index)
if common_features:
    for i, feature in enumerate(common_features, 1):
        print(f"   {i}. {feature}")
else:
    print("   Brak wspólnych cech w top 5")

print(f"\n8. Raport klasyfikacyjny najlepszego modelu ({best_model_f1}):")
best_model_results = results[best_model_f1]
print(
    classification_report(
        y_test, best_model_results["y_pred"], target_names=["Zdrowy (0)", "Chory (1)"]
    )
)

results_df.to_csv("wyniki_modeli.csv", index=False)
