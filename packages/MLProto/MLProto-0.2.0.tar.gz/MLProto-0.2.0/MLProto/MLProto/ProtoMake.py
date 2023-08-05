#!/usr/bin/env python

from . import Proto
from . import Data as helper
import argparse
from matplotlib import pyplot
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def main():
    parser = argparse.ArgumentParser(description="StockerMake script")
    parser.add_argument('filepath', help='Filepath for input data')
    parser.add_argument('target', type=int, help='Column number of target labels')
    parser.add_argument('-depth', default=1, type=int, help='Depth of LSTM neural net, (default 1)')
    parser.add_argument('-node_counts', default=[100], type=int, nargs='*', help='Node counts for each LSTM layer. (number of args must be equal to depth')
    parser.add_argument('-batch', default=50, type=int, help='Batch size (default 50)')
    parser.add_argument('-test_size', default=.2, type=float, help='Percentage of samples to use for testing (decimal form)')
    parser.add_argument('-loss', default='mse', help='Loss function for Neural Net')
    parser.add_argument('-learning_rate', default=.001, type=float, help='Learning rate of Neural Net (Default .001)')
    parser.add_argument('-epochs', default=100, type=int, help='Epoch count for training (Default 100)')
    parser.add_argument('-model_in', default=None, help='Path of pre-made model to load')
    parser.add_argument('-past_window', default=60, type=int, help='Window of past data steps to account for in training')
    parser.add_argument('--normalize', action='store_true', help='Normalizes data')
    parser.add_argument('--early_stop', action='store_true', default=False, help='Apply early stopping to model training (Patience 10)')
    parser.add_argument('--plots', action='store_true', help='Saves all plots to plots folder')
    parser.add_argument('identifier', nargs='*', help="String identifier for model")
    parse = parser.parse_args()

    # read historical daily data from alpha_vantage
    # store in python dict
    hist = pd.read_csv(parse.filepath)
    hist = hist.reindex(index=hist.index[::-1])
    print(hist, '\n')

    if parse.plots:
        pyplot.figure()
        hist.plot(subplots=True)
        pyplot.suptitle('Input Features')
        pyplot.savefig(helper.make_dir('./plots/' + symbol) + '/input.png')

    model = Proto.Proto(parse.identifier, hist, parse.target, parse.depth, parse.node_counts, parse.batch, parse.test_size, parse.loss, \
                        parse.learning_rate, parse.model_in, parse.normalize, parse.past_window)
    model.train(parse.epochs, parse.early_stop, parse.plots)
    model.evaluate()
    model.save_model()

    predictions = model.predict_data(model.val_in)

    standard_numpy = hist[int(hist.shape[0]*(1-parse.test_size)):, parse.target].to_numpy()

    if parse.plots:
        pyplot.figure()
        pyplot.plot(standard_numpy, label='True Values')
        pyplot.plot(predictions[:, 0], label='Predictions')
        pyplot.xlabel('Time Step')
        pyplot.ylabel('Adjusted Close')
        pyplot.suptitle('Predictions')
        pyplot.legend()
        pyplot.savefig(helper.make_dir('./plots/' + symbol) + '/predictions.png')

if __name__ == '__main__':
    main()