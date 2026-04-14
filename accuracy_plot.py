import matplotlib.pyplot as plt

methods = ["EAR Only", "ML Only", "Hybrid AI"]
accuracy = [75, 89, 95]

plt.figure()
plt.plot(methods, accuracy, marker='o')
plt.xlabel("Detection Method")
plt.ylabel("Accuracy (%)")
plt.title("Accuracy Comparison of Drowsiness Detection Methods")
plt.ylim(60, 100)
plt.grid(True)
plt.show()
