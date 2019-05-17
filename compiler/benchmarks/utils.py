class MNIST():
    def __init__(self, path='.'):
        self.path = path
        self.test_img_fname = 't10k-images-idx3-ubyte.gz'
        self.test_lbl_fname = 't10k-labels-idx1-ubyte.gz'

        self.train_img_fname = 'train-images-idx3-ubyte.gz'
        self.train_lbl_fname = 'train-labels-idx1-ubyte.gz'

        self.test_images, self.test_labels = self.load_testing()
        self.train_images, self.train_labels = self.load_training()

    def load(self, path_img, path_lbl):
        with gzip.open(path_lbl, 'rb') as file:
            magic, size = struct.unpack(">II", file.read(8))
            if magic != 2049:
                raise ValueError('Magic number mismatch, expected 2049,'
                                 'got {}'.format(magic))

            labels = array("B", file.read())

        with gzip.open(path_img, 'rb') as file:
            magic, size, rows, cols = struct.unpack(">IIII", file.read(16))
            if magic != 2051:
                raise ValueError('Magic number mismatch, expected 2051,'
                                 'got {}'.format(magic))
            image_data = array("B", file.read())

        images = []
        for i in range(size):
            images.append([0] * rows * cols)

        for i in range(size):
            images[i][:] = image_data[i * rows * cols:(i + 1) * rows * cols]

        return images, labels

    def load_testing(self):
        ims, labels = self.load(os.path.join(self.path, self.test_img_fname),
                                os.path.join(self.path, self.test_lbl_fname))

        self.test_images = np.array(ims)
        self.test_labels = np.array(labels)

        return self.test_images, self.test_labels

    def load_training(self):
        ims, labels = self.load(os.path.join(self.path, self.train_img_fname),
                                os.path.join(self.path, self.train_lbl_fname))

        self.train_images = np.array(ims)
        self.train_labels = np.array(labels)

        return self.train_images, self.train_labels

def split_data(train_size=60000, test_size=10000):
    mnist = MNIST()
    X_train = mnist.train_images[:train_size] / 255
    X_test = mnist.test_images[-test_size:] / 255
    return X_train, X_test,mnist.train_labels[:train_size], mnist.test_labels[-test_size:]
