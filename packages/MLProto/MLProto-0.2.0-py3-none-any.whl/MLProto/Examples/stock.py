#!/usr/bin/env python

from alpha_vantage.timeseries import TimeSeries
from ..MLProto import Proto as proto
from ..MLProto import Data as helper
import argparse
from matplotlib import pyplot
import pandas
import numpy
from sklearn.preprocessing import MinMaxScaler

import warnings
warnings.filterwarnings("ignore")

def daily_adjusted(symbol, key, compact=True):
    """ Returns data frame of queried data

        args:
            symbol -- symbol of desired stock
            key -- user's API key
        compact -- True -> last 100 results
                   False -> all past results
    """

    # create time series
    ts = TimeSeries(key=key, output_format='pandas')

    # take last 100 or complete historical as needed
    if compact:
        data, _ = ts.get_daily_adjusted(symbol=symbol, outputsize='compact')
    else:
        data, _ = ts.get_daily_adjusted(symbol=symbol, outputsize='full')

    return data

def main():
    parser = argparse.ArgumentParser(description="StockerMake script")
    parser.add_argument('key', help='User API Key')
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
    parser.add_argument('symbols', nargs='*', help="List of symbols to train")
    parse = parser.parse_args()

    symbols = parse.symbols

    for symbol in symbols:

        # read historical daily data from alpha_vantage
        # store in python dict
        hist = daily_adjusted(symbol, parse.key, compact=False)
        hist = hist.drop(['6. volume', '7. dividend amount', '8. split coefficient'], axis=1)
        hist = hist.reindex(index=hist.index[::-1])
        print(hist)
        print()

        if parse.plots:
            pyplot.figure()
            hist.plot(subplots=True)
            pyplot.suptitle('Input Features')
            pyplot.savefig(helper.make_dir('./plots/' + symbol) + '/input.png')

        model = proto.Proto(symbol, hist, 3, parse.depth, parse.node_counts, parse.batch, parse.test_size, parse.loss, \
                            parse.learning_rate, parse.model_in, parse.normalize, parse.past_window)
        model.train(parse.epochs, parse.early_stop, parse.plots)
        model.evaluate()
        model.save_model()

        predictions = model.predict_data(model.val_in)
        #print(predictions)
        #print(predictions.shape)

        standard_numpy = hist[int(hist.shape[0]*(1-parse.test_size))+60:]['4. close'].to_numpy()
        # print(standard_numpy.shape)

        if parse.plots:
            pyplot.figure()
            pyplot.plot(standard_numpy, label='True Values')
            pyplot.plot(predictions[:, 0], label='Predictions')
            pyplot.xlabel('Time Step')
            pyplot.ylabel('Closing Prices')
            pyplot.suptitle(symbol + ' Predictions')
            pyplot.legend()
            pyplot.savefig(helper.make_dir('./plots/' + symbol) + '/predictions.png')

if __name__ == '__main__':
    main()