from sklearn.metrics import accuracy_score


def baseline_model(data, target):
    data[target].value_counts(normalize=True)
    majority_class = data[target].mode()[0]
    y_pred = [majority_class] * len(data)
    baseline_score = int(round(accuracy_score(data[target],
                                              y_pred), 2) * 100)
    print(f"Baseline Accuracy Score: {baseline_score}%")
