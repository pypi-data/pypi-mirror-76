import matplotlib.pyplot as plt


def gray_imshow(image, title=None):
    plt.imshow(image, cmap="gray")
    plt.axis("off")
    if title is not None:
        plt.title(title)


def rgb_imshow(image, title=None):
    plt.imshow(image)
    plt.axis("off")
    if title is not None:
        plt.title(title)


def bgr_imshow(image, title=None):
    rgb_imshow(image[..., ::-1], title)
