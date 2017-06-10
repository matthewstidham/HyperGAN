from hypergan.gan_component import GANComponent

import tensorflow as tf

class MultiComponent():
    """
        Used to combine multiple components into one.  For example, `gan.loss = MultiComponent([loss1, loss2])`
    """
    def __init__(self, components=[], combine='concat'):
        self.components = components
        self.gan = components[0].gan
        self._combine = combine

    def __getattr__(self, name):
        if len(self.components) == 0:
            return None

        attributes = self.lookup(name)
        return self.combine(attributes)

    def lookup(self, name):
        lookups = []
        for component in self.components:
            if hasattr(component, name):
                lookups.append(getattr(component,name))
            else:
                print("Warning:Skipping lookup of "+name+" because None was returned")

        return lookups

    def combine(self, data):
        if data == None or data == []:
            return data

        print("LIST", data)
        # loss functions return [d_loss, g_loss].  We combine columnwise.
        if isinstance(data, list) and isinstance(data[0], list) and isinstance(data[0][0], tf.Tensor):
            result = []
            for j,_ in enumerate(data[0]):
                column = []
                for i,_ in enumerate(data):
                    column.append(data[i][j])
                reduction = self.reduce(column)
                result.append(reduction)

            return result

        if type(data[0]) == tf.Tensor:
            return self.reduce(data)
        if callable(data[0]):
            return self.call_each(data)
        return data

    def reduce(self, data):
        data = [d for d in data if d is not None]
        if self._combine == 'concat':
            return self.gan.ops.concat(values=data, axis=1)
        elif self._combine == 'add':
            return self.gan.ops.add_n(data)

        raise "Unknown combine"

    def call_each(self, methods):
        def do_call(*args, **kwargs):
            results = []
            for method in methods:
                results.append(method(*args, **kwargs))
            return self.combine(results)
        return do_call
