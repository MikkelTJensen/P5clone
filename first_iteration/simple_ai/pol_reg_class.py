import tensorflow as tf

class PolynomialRegression:
    def __init__(self, initializer='random'):
        if initializer == 'ones':
            self.var = 1.
        elif initializer == 'zeros':
            self.var = 0.
        elif initializer == 'random':
            self.var = tf.random.uniform(shape=[], minval=0., maxval=1.)

        self.a = tf.Variable(self.var)
        self.b = tf.Variable(self.var)
        self.c = tf.Variable(self.var)

    def predict(self, x):
        return tf.reduce_sum(self.a * x ** 2 + self.b * x, 1) + self.c

    def mse(self, true, predicted):
        return tf.reduce_mean(tf.square(true - predicted))

    def update(self, X, y, learning_rate):
        with tf.GradientTape(persistent=True) as g:
            self.loss = self.mse(y, self.predict(X))

        print("Loss: ", tf.keras.backend.get_value(self.loss))

        dy_da = g.gradient(self.loss, self.a)
        dy_db = g.gradient(self.loss, self.b)
        dy_dc = g.gradient(self.loss, self.c)

        self.a.assign_sub(learning_rate * dy_da)
        self.b.assign_sub(learning_rate * dy_db)
        self.c.assign_sub(learning_rate * dy_dc)

    def train(self, X, y, learning_rate, epochs=5):

        if len(X.shape) == 1:
            X = tf.reshape(X, [X.shape[0], 1])

        for i in range(epochs):
            print("Epoch: ", i)

            self.update(X, y, learning_rate)
