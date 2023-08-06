from torch import nn, load, device
from collections import OrderedDict

from torchsummary import summary

try:
    SUMMARY = True
except ImportError:
    SUMMARY = False
from functools import partial

from . import network_initialization

from torch.utils.data import TensorDataset


class Model(object):
    def __init__(self, model: nn.Module, input_shape=None, initializer='Xavier'):
        self.model = model
        self.shape = input_shape
        self.initializable_layers = [self.model.parameters()]
        self.initializer = initializer

    def _initialize_layers(self):
        if self.initializable_layers is None:
            print('Network not automatically initilized')
            return False
        else:
            print('Network automatically initilized at : \n ')
            for m in self.initializable_layers:
                print('\t' + m.__class__.__name__)
            map(self.init_function, self.initializable_layers)
            return True

    def with_summary(self):
        if self.shape is not None and SUMMARY:
            return True
        else:
            return False

    def get_summary(self, device='cuda'):
        if self.with_summary():
            return summary(self.model, self.shape, device=device)
        else:
            return str(self.model)

    def init_function(self):
        """
        :return: Returns a function which initialize layers given an iterator of parameters.
        """
        return partial(network_initialization.init_weights, init_type=self.initializer)

    def load(self, directory, strict_loading=True, from_checkpoint=False):
        """
        Load model function which allows to load from a python dict, path to weights or checkpoint.
        If called enables framework.loaded_model = True

        :param directory: Loaded state dict or path to weights or checkpoint.
        :type directory: dict,str
        :param strict_loading: PyTorch strict_loading flag. Impose exact matching between loaded weights and model.
        :type strict_loading: bool
        :param from_checkpoint: Forces function to interpret given weights as checkpoint dictionary.
        :type   from_checkpoint: bool
        :return: None
        """
        print('Loading pre-trained weights')
        if isinstance(directory, dict):
            state_dict = directory
        else:
            state_dict = load(directory, map_location=lambda storage, loc: storage)
        if from_checkpoint:
            state_dict = state_dict['state_dict']
        new_state_dict = OrderedDict()

        for k, v in state_dict.items():
            if k[:7] == 'module.':
                name = k[7:]  # remove `module.`
            else:
                name = k
            new_state_dict[name] = v
        self.model.load_state_dict(new_state_dict, strict=strict_loading)

    def get_dataset(self, N=2, gt=None, visualization=None):
        if self.shape is None:
            raise ValueError('get_dataset method called but no input shape provided')
        from torch import rand
        if isinstance(self.shape, tuple):
            input_size = [self.shape]
        x = []
        if gt is not None:
            x.append(rand(N, *gt))
        x.append(rand(N, *input_size[0]).float())

        if visualization is not None:
            x.append(rand(N, *visualization))
        return TensorDataset(*x)

    def to(self, device):
        return Model(self.model.to(device), self.shape, self.initializer)
