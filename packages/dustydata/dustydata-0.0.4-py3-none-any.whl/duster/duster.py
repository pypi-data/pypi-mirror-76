from sklearn.metrics import accuracy_score


def baseline_score_clf(data, target):
    data[target].value_counts(normalize=True)
    majority_class = data[target].mode()[0]
    y_pred = [majority_class] * len(data)
    baseline_score = int(round(accuracy_score(data[target],
                                              y_pred), 2) * 100)
    print(f"Baseline Accuracy Score: {baseline_score}")


def cut_cardinality(data, threshold=50):
    cardinality = data.select_dtypes(exclude='number').nunique()
    categorical_features = cardinality[cardinality <= threshold].index.tolist()
    return categorical_features
