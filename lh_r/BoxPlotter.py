def BoxPlot(LowWhisker, Q1, Median, Mean, Q3, HighWhisker, XCoord, Width=0.8):
    """
    Create a boxplot from stats about a dataset. Ideal for when the dataset is
    too big to process in python. Width is the width in axis units of the box,
    so typically a value of 0.8 will ensure that boxplots will not touch.

    Call plt.show() or plt.savefig() to view the boxplots.
    """
    import numpy as np
    import matplotlib.pyplot as plt

    # Half the supplied width as the boxes are drawn around a center point
    Width = Width / 2

    plt.hlines(Q1, XCoord - Width, XCoord + Width, linewidth=0.5)
    plt.hlines(Mean, XCoord - Width, XCoord + Width, color='b', label='Mean', linewidth=0.5)
    plt.hlines(Median, XCoord - Width, XCoord + Width, color='r', label='Median', linewidth=0.5)
    plt.hlines(Q3, XCoord - Width, XCoord + Width, linewidth=0.5)

    plt.vlines(XCoord - Width, Q1, Q3, linewidth=0.5)
    plt.vlines(XCoord + Width, Q1, Q3, linewidth=0.5)

    # whiskers
    plt.vlines(XCoord, Q3, HighWhisker, linewidth=0.25)
    plt.vlines(XCoord, LowWhisker, Q1, linewidth=0.25)

    # end caps
    plt.hlines(HighWhisker, XCoord - (Width / 1.), XCoord + (Width / 1.), linewidth=0.25)
    plt.hlines(LowWhisker, XCoord - (Width / 1.), XCoord + (Width / 1.), linewidth=0.25)
