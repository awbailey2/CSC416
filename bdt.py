import csv
from collections import Counter
import math

# Node class for the decision tree
class Node:
    def __init__(self, feature=None, decision=None):
        self.feature = feature  # Feature to split on
        self.decision = decision  # Decision at this node (if it's a leaf)
        self.children = {}  # Dictionary to store child nodes

    def __repr__(self):
        if self.decision is not None:
            return f"Node(decision={self.decision})"
        else:
            return f"Node(feature={self.feature}, children={list(self.children.keys())})"

# Function to calculate entropy
def calculate_entropy(data):
    total = len(data)
    if total == 0:
        return 0
    decision_counts = Counter(row[-1] for row in data)
    entropy = -sum((count / total) * math.log2(count / total) for count in decision_counts.values())
    return entropy

# Function to calculate information gain
def calculate_information_gain(feature_index, data):
    total_entropy = calculate_entropy(data)
    total = len(data)
    subsets = {}
    for row in data:
        feature_value = row[feature_index]
        if feature_value not in subsets:
            subsets[feature_value] = []
        subsets[feature_value].append(row)

    subset_entropy = 0
    for value, subset in subsets.items():
        subset_entropy_val = calculate_entropy(subset)
        subset_entropy += (len(subset) / total) * subset_entropy_val
        print(f"Feature Value: {value}, Subset Entropy: {subset_entropy_val}")
    
    information_gain = total_entropy - subset_entropy
    print(f"Total Entropy: {total_entropy}, Subset Entropy: {subset_entropy}, Information Gain: {information_gain}")
    return information_gain

# Function to build the decision tree
def build_decision_tree(data, features):
    decisions = set(row[-1] for row in data)
    if len(decisions) == 1:
        # All decisions are the same; return a leaf node
        return Node(decision=data[0][-1])

    if not features:
        # No more features to split on; return the most common decision
        most_common_decision = Counter(row[-1] for row in data).most_common(1)[0][0]
        return Node(decision=most_common_decision)

    # Find the best feature to split on
    best_feature_index = max(
        range(len(features)),
        key=lambda i: calculate_information_gain(i, data)
    )
    best_feature = features[best_feature_index]

    # Create a node for the best feature
    root = Node(feature=best_feature)
    subsets = {}
    for row in data:
        feature_value = row[best_feature_index]
        if feature_value not in subsets:
            subsets[feature_value] = []
        subsets[feature_value].append(row)

    # Remove the best feature from the list of features for child nodes
    remaining_features = features[:best_feature_index] + features[best_feature_index + 1:]

    # Recursively build child nodes
    for value, subset in subsets.items():
        root.children[value] = build_decision_tree(subset, remaining_features)

    return root

# Function to print the tree
def print_tree(node, level=0):
    indent = "  " * level
    if node.decision is not None:
        print(f"{indent}Decision: {node.decision}")
    else:
        print(f"{indent}Feature: {node.feature}")
        for value, child in node.children.items():
            print(f"{indent}  Value: {value}")
            print_tree(child, level + 1)

# Main function
def main():
    # Read the CSV file
    with open("decision_tree_dataset.csv", "r") as file:
        reader = csv.reader(file)
        data = list(reader)

    # Extract features and data
    features = data[0][:-1]  # Feature names (excluding "Decision")
    data = data[1:]  # Data (excluding the header row)

    # Build the decision tree
    decision_tree = build_decision_tree(data, features)

    # Print the decision tree
    print_tree(decision_tree)

if __name__ == "__main__":
    main()

    import unittest

class TestDecisionTree(unittest.TestCase):
 def test_information_gain(self):
        # Test dataset
        data = [
            ["young", "high", "yes"],
            ["young", "high", "yes"],
            ["middle-aged", "low", "no"],
            ["senior", "low", "no"],
            ["senior", "high", "yes"],
            ["young", "low", "no"]
        ]
        # Feature index for 'Age' (index 0 in the list)
        feature_index = 0  
        
        # Expected information gain for 'Age' feature based on manual calculation
        expected_gain_age = 0.20755  # Corrected based on manual calculation

        # Calculate the information gain for 'Age' feature
        gain_age = calculate_information_gain(feature_index, data)

        # Test if the calculated gain is close to the expected value
        self.assertAlmostEqual(gain_age, expected_gain_age, places=4)
def test_build_decision_tree(self):
        # Test decision tree construction
        data = [
            ["young", "excellent", "yes", "yes"],
            ["middle-aged", "fair", "no", "no"],
            ["senior", "excellent", "yes", "no"],
            ["young", "excellent", "yes", "yes"],
            ["middle-aged", "fair", "no", "no"]
        ]
        features = ["Age", "Credit_rating", "Student"]  # Features for the tree
        tree = build_decision_tree(data, features)
        
        # Print the decision tree structure
        print("Decision Tree:")
        print_tree(tree)

# Function to print the decision tree (for visualization)
def print_tree(node, level=0):
    indent = "  " * level
    if node.decision is not None:
        print(f"{indent}Decision: {node.decision}")
    else:
        print(f"{indent}Feature: {node.feature}")
        for value, child in node.children.items():
            print(f"{indent}  Value: {value}")
            print_tree(child, level + 1)

if __name__ == '__main__':
    unittest.main()