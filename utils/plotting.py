import matplotlib.pyplot as plt

plt.style.use("seaborn")


def display_embedding_with_dr(embedding, labels, target, n_components=2):
    if target is None:
        target = "r"
    plt.figure(figsize=(50, 20))
    if n_components == 1:
        plt.scatter(u[:, 0], range(len(u)), c=target, s=100)
    if n_components == 2:
        plt.scatter(u[:, 0], u[:, 1], c=target, s=100)
        for label, (x, y) in zip(labels, u):
            plt.text(x + 0.05, y + 0.05, label)
    if n_components == 3:
        plt.scatter(u[:, 0], u[:, 1], u[:, 2], c=embeddings, s=100)
    # let's customerize the title with dr_type, n_components ETC
    plt.title(title, fontsize=18)
    plt.savefig("show_embedding_with_label.png")
