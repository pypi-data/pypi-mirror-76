class IndexTracker(object):
    def __init__(self, ax, X):
        """
        It is used at "Stack.show()".
        You can scroll to navigate different z-slices.
        """
        self.ax = ax
        ax.set_title('use scroll wheel to navigate images')

        self.X = X
        self.slices = X.shape
        self.ind = self.slices[2]//2

        self.im = ax.imshow(self.X[:, :, self.ind], cmap='gray')
        self.update()

    def onscroll(self, event):
        if event.button == 'up':
            self.ind = (self.ind + 1) % self.slices[2]
        else:
            self.ind = (self.ind - 1) % self.slices[2]
        self.update()

    def update(self):
        self.im.set_data(self.X[:, :, self.ind])
        self.ax.set_ylabel('slice %s' % self.ind)
        self.im.axes.figure.canvas.draw()