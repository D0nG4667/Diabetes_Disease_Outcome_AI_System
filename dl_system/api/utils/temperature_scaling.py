import tensorflow as tf

class TemperatureScaler(tf.keras.Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.temperature = tf.Variable(1.0, trainable=True, dtype=tf.float32)

    def get_config(self):
        config = super().get_config()
        return config

    @tf.function(reduce_retracing=True)
    def call(self, logits):
        return logits / self.temperature
