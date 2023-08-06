from ..nn.initializers import get_initializer, Initializer
from .activators import get_activator
from ..nn.core import Layer, Variable
from ..nn import global_graph as GlobalGraph
from ..nn.functional import conv2d, max_pool2d, avg_pool2d, channel_max_pool
from ..nn.grad_fn import Conv2DBackward, Maxpool2DBackward, Avgpool2DBackward, ChannelMaxpoolBackward, ChannelAvgpoolBackward
from typing import Tuple, Union


class Conv2D(Layer):
    def __init__(self, out_channels: int, kernel_size: Union[int, Tuple], use_bias: bool = False, stride: Union[int, Tuple] = 1, padding: Union[int, str] = 0,
                 activation: str = None, kernel_initializer: Union[str, Initializer] = 'Normal',
                 bias_initializer: Union[str, Initializer] = 'zeros', input_shape: Tuple = None, **kwargs):
        self.out_channels = out_channels
        self.kernel_size = self.__check_size(kernel_size)
        self.input_shape = input_shape
        self.use_bias = use_bias
        self.stride = self.__check_size(stride)
        self.padding = padding
        self.activation = get_activator(activation) if activation is not None else None
        self.kernel_initializer = get_initializer(kernel_initializer)
        self.bias_initializer = get_initializer(bias_initializer)
        self.pad_size = padding
        self.cols = None
        super(Conv2D, self).__init__(input_shape=input_shape, **kwargs)

    def __check_size(self, kernel_size):
        if isinstance(kernel_size, (int, float)):
            return int(kernel_size), int(kernel_size)
        return kernel_size

    def initial_params(self, input_shape: Tuple = None):
        if input_shape is not None:
            self.input_shape = input_shape
        w = self.kernel_initializer((self.out_channels, self.input_shape[0], self.kernel_size[0],
                                              self.kernel_size[1]), name='xs_variable')
        if self.use_bias:
            b = self.bias_initializer((1, self.out_channels), name='xs_variable')
        else:
            b = None
        self.variables.append(w)
        self.variables.append(b)

    def compute_output_shape(self, input_shape: Tuple = None):
        assert len(input_shape) == 3
        n_C_prev, n_H_prev, n_W_prev = input_shape
        filter_h, filter_w = self.kernel_size
        if self.padding.__class__.__name__ == 'str':
            padding = self.padding.upper()
            if padding == 'SAME':
                n_H = n_H_prev
                n_W = n_W_prev
                pad_h = (self.stride[0] * (n_H_prev - 1) - n_H_prev + filter_h) // 2
                self.pad_size = pad_h
            elif padding == 'VALID':
                n_H = (n_H_prev - filter_h) // self.stride[0] + 1
                n_W = (n_W_prev - filter_w) // self.stride[1] + 1
                self.pad_size = 0
            else:
                raise TypeError('Unknown padding type!plz inputs SAME or VALID or an integer')
        else:
            assert isinstance(self.padding, int)
            n_H = (n_H_prev - filter_h + 2 * self.padding) // self.stride[0] + 1
            n_W = (n_W_prev - filter_w + 2 * self.padding) // self.stride[1] + 1
            self.pad_size = self.padding

        return self.out_channels, n_H, n_W

    def __call__(self, inbound, *args, **kwargs):
        # if isinstance(inbound, Variable):
        if inbound.data is not None:
            if len(self.variables) == 0:
                self.initial_params(inbound.shape[1:])
            output = conv2d(inbound, self.variables[0], self.variables[1], self.stride, self.pad_size, GlobalGraph.IS_TRAINING)
            if self.activation is not None:
                output = self.activation.forward(output)
            # output是一个Variable
            return output

        super(Conv2D, self).__call__(inbound)
        return self

    def forward(self, x: Variable = None, *args):
        if x is not None:
            self.input_data = x
        w, b = self.variables
        self.data = conv2d(self.input_data, w, b, self.stride, self.pad_size, GlobalGraph.IS_TRAINING)
        if self.activation is not None:
            output = self.activation.forward(self.data)
            self.feed_variable_to_next_layers(output)
            return output
        else:
            self.feed_variable_to_next_layers(self.data)
            return self.data

    def backward(self, gradients=None):
        if self.activation is not None:
            self.activation.backward()
        Conv2DBackward(self.data)


class MaxPooling2D(Layer):
    def __init__(self, kernel_size: int = 2, stride: int = None, padding: int = 0):
        self.kernel_size = kernel_size
        self.stride = self.__check_size(kernel_size) if stride is None else self.__check_size(stride)
        self.padding = padding
        self.mode = 'reshape'
        super(MaxPooling2D, self).__init__()

    def compute_output_shape(self, input_shape=None):
        n_c, n_h_prev, n_w_prev = input_shape
        if self.kernel_size == self.stride:
            self.mode = 'reshape'
        else:
            self.mode = 'im2col'
        n_h, n_w = (n_h_prev - self.kernel_size + 2 * self.padding) // self.stride[0] + 1, (n_w_prev - self.kernel_size
                                                                                            + 2 * self.padding) // self.stride[1] + 1
        return n_c, n_h, n_w

    def __check_size(self, kernel_size):
        if isinstance(kernel_size, (int, float)):
            return int(kernel_size), int(kernel_size)
        return kernel_size

    def __call__(self, inbound, *args, **kwargs):
        if isinstance(inbound, Variable):
            output = max_pool2d(inbound, self.kernel_size, self.stride, self.padding, GlobalGraph.IS_TRAINING)
            # output是一个Variable
            return output
        super(MaxPooling2D, self).__call__(inbound)
        return self

    def forward(self, x: Variable = None, *args):
        if x is not None:
            self.input_data = x
        self.data = max_pool2d(self.input_data, self.kernel_size, self.stride, self.padding, GlobalGraph.IS_TRAINING)
        self.feed_variable_to_next_layers(self.data)
        return self.data

    def backward(self, gradients=None):
        Maxpool2DBackward(self.data)


class AvgPooling2D(Layer):
    def __init__(self, kernel_size: int = 2, stride: int = None, padding: int = 0):
        self.kernel_size = kernel_size
        self.stride = self.__check_size(kernel_size) if stride is None else self.__check_size(stride)
        self.padding = padding
        super(AvgPooling2D, self).__init__()

    def __check_size(self, kernel_size):
        if isinstance(kernel_size, (int, float)):
            return int(kernel_size), int(kernel_size)
        return kernel_size

    def compute_output_shape(self, input_shape=None):
        n_c, n_h_prev, n_w_prev = input_shape
        n_h, n_w = (n_h_prev - self.kernel_size + 2 * self.padding) // self.stride[0] + 1, \
                   (n_w_prev - self.kernel_size + 2 * self.padding) // self.stride[1] + 1
        return n_c, n_h, n_w

    def __call__(self, inbound, *args, **kwargs):
        if isinstance(inbound, Variable):
            output = avg_pool2d(inbound, self.kernel_size, self.stride, self.padding, GlobalGraph.IS_TRAINING)
            # output是一个Variable
            return output
        super(AvgPooling2D, self).__call__(inbound)
        return self

    def forward(self, x: Variable = None, *args):
        if x is not None:
            self.input_data = x
        self.data = avg_pool2d(self.input_data, self.kernel_size, self.stride, self.padding, GlobalGraph.IS_TRAINING)
        self.feed_variable_to_next_layers(self.data)
        return self.data

    def backward(self, gradients=None):
        Avgpool2DBackward(self.data)


class ChannelMaxPooling(Layer):
    def __init__(self, kernel_size: int = 2, stride: int = None, padding: int = 0):
        self.kernel_size = kernel_size
        self.stride = kernel_size if stride is None else stride
        self.padding = padding
        self.mode = 'reshape'
        super(ChannelMaxPooling, self).__init__()

    def compute_output_shape(self, input_shape=None):
        n_c_prev, n_h, n_w = input_shape
        if self.kernel_size == self.stride:
            self.mode = 'reshape'
        else:
            self.mode = 'im2col'
        n_c = (n_c_prev - self.kernel_size + 2 * self.padding) / self.stride + 1
        return n_c, n_h, n_w

    def __call__(self, inbound, *args, **kwargs):
        if isinstance(inbound, Variable):
            output = channel_max_pool(inbound, self.kernel_size, self.stride, self.padding, GlobalGraph.IS_TRAINING)
            # output是一个Variable
            return output
        super(ChannelMaxPooling, self).__call__(inbound)
        return self

    def forward(self, x: Variable = None, *args):
        if x is not None:
            self.input_data = x
        self.data = channel_max_pool(self.input_data, self.kernel_size, self.stride, self.padding, GlobalGraph.IS_TRAINING)
        self.feed_variable_to_next_layers(self.data)
        return self.data

    def backward(self, gradients=None):
        ChannelMaxpoolBackward(self.data)


class ChannelAvgPooling(Layer):
    def __init__(self, kernel_size: int = 2, stride: int = None, padding: int = 0):
        self.kernel_size = kernel_size
        self.stride = kernel_size if stride is None else stride
        self.padding = padding
        self.mode = 'reshape'
        super(ChannelAvgPooling, self).__init__()

    def compute_output_shape(self, input_shape=None):
        n_c_prev, n_h, n_w = input_shape
        if self.kernel_size == self.stride:
            self.mode = 'reshape'
        else:
            self.mode = 'im2col'
        n_c = (n_c_prev - self.kernel_size + 2 * self.padding) / self.stride + 1
        return n_c, n_h, n_w

    def __call__(self, inbound, *args, **kwargs):
        if isinstance(inbound, Variable):
            output = channel_max_pool(inbound, self.kernel_size, self.stride, self.padding, GlobalGraph.IS_TRAINING)
            # output是一个Variable
            return output
        super(ChannelAvgPooling, self).__call__(inbound)
        return self

    def forward(self, x: Variable = None, *args):
        if x is not None:
            self.input_data = x
        self.data = channel_max_pool(self.input_data, self.kernel_size, self.stride, self.padding, GlobalGraph.IS_TRAINING)
        self.feed_variable_to_next_layers(self.data)
        return self.data

    def backward(self, gradients=None):
        ChannelAvgpoolBackward(self.data)
