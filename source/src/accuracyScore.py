
from collections import defaultdict
def accuracy_score(y_true, y_pred):
    correct = sum(yt == yp for yt, yp in zip(y_true, y_pred))
    return correct / len(y_true)
def precision_recall_fscore_support(y_true, y_pred, average=None):
    y_true = list(y_true) # Convert to list if it is a pandas Series
    y_pred = list(y_pred)
    labels = sorted(set(y_true) | set(y_pred))
    label_indices = {label: idx for idx, label in enumerate(labels)}
    tp = defaultdict(int)
    fp = defaultdict(int)
    fn = defaultdict(int)
    for true, pred in zip(y_true, y_pred):
        if true == pred:
            tp[true] += 1
        else:
            fp[pred] += 1
            fn[true] += 1
    precisions = {}
    recalls = {}
    f1_scores = {}
    supports = {label: y_true.count(label) for label in labels}
    for label in labels:
        precision = tp[label] / (tp[label] + fp[label]) if (tp[label] + fp[label]) > 0 else 0.0
        recall = tp[label] / (tp[label] + fn[label]) if (tp[label] + fn[label]) > 0 else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
        precisions[label] = precision
        recalls[label] = recall
        f1_scores[label] = f1
    if average == 'macro':
        precision = sum(precisions.values()) / len(labels)
        recall = sum(recalls.values()) / len(labels)
        f1 = sum(f1_scores.values()) / len(labels)
        return precision, recall, f1, [supports[label] for label in labels]
    return precisions, recalls, f1_scores, supports
def classification_report(y_true, y_pred):
    precisions, recalls, f1_scores, supports = precision_recall_fscore_support(y_true, y_pred)
    report = "              precision    recall  f1-score   support\n"
    for label in sorted(precisions.keys()):
        report += f"{label: <12} {precisions[label]: <10.2f} {recalls[label]: <10.2f} {f1_scores[label]: <10.2f} {supports[label]: <10}\n"
    report += "\n"
    macro_p, macro_r, macro_f1, _ = precision_recall_fscore_support(y_true, y_pred, average='macro')
    report += f"macro avg    {macro_p: <10.2f} {macro_r: <10.2f} {macro_f1: <10.2f} {sum(supports.values()): <10}\n"
    return report