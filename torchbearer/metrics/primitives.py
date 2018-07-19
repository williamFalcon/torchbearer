import torchbearer
from torchbearer import metrics

import torch


class CategoricalAccuracy(metrics.BatchLambda):
    """Categorical accuracy metric. Uses torch.max to determine predictions and compares to targets.
    """

    def __init__(self):
        def metric_function(y_pred, y_true):
            _, y_pred = torch.max(y_pred, 1)
            return (y_pred == y_true).float()
        super(CategoricalAccuracy, self).__init__('acc', metric_function)


@metrics.default_for_key('acc')
@metrics.default_for_key('accuracy')
@metrics.running_mean
@metrics.std
@metrics.mean
class CategoricalAccuracyFactory(metrics.MetricFactory):
    def build(self):
        return CategoricalAccuracy()


class Loss(metrics.Metric):
    """Simply returns the 'loss' value from the model state.
    """

    def __init__(self):
        super().__init__('loss')

    def process(self, state):
        return state[torchbearer.LOSS]


@metrics.default_for_key('loss')
@metrics.running_mean
@metrics.std
@metrics.mean
class LossFactory(metrics.MetricFactory):
    def build(self):
        return Loss()


class Epoch(metrics.Metric):
    """Returns the 'epoch' from the model state.
    """

    def __init__(self):
        super().__init__('epoch')

    def process_final(self, state):
        return self._process(state)

    def process(self, state):
        return self._process(state)

    def _process(self, state):
        return state[torchbearer.EPOCH]


@metrics.default_for_key('epoch')
@metrics.running_mean
@metrics.std
@metrics.mean
class EpochFactory(metrics.MetricFactory):
    def build(self):
        return Epoch()
