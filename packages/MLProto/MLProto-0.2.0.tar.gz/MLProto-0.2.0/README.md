# MLProto: Modular Prototyping Tool for LSTM Machine Learning Models

## Usage

### Video overview coming

### The ProtoMake Script

The ProtoMake script combines the Proto and Data modules into one to create an easy, convenient, and modular neural network prototyping tool for LSTM machine learning models. The script will take the user's desired parameters and create, train, and evaluate a model fitting said parameters. This allows the user to quickly analyze model prototypes, make adjustments, and iterate on model designs.

#### Arguments

    Positional:
        key ---- User's Alpha_Vantage API key
        identifier ---- Ticker symbols to create models for
        target ---- Column number of target values

    Optional:
        -depth ---- number of layers to include in the neural network (def: 1)
        -node_counts ---- list of node counts for layers (len(node_counts) must equal depth)
        -batch ---- batch size of input data set (def: [100])
        -test_size ---- proportion of dataset to use as validation (def: .2)
        -loss ---- identifier string of keras-supported loss function to be used in training (def: mse)
        -learning_rate ---- learning rate to be used by the Adam optimizer
        -epochs ---- maximum number of epochs to train the model (def: 100)
        -model_in ---- file path of pre-made model to load
        --early_stop ---- flag deciding whether to apply early stopping (patience 5) to the training phase
        --plots ---- flag deciding whether to save loss, input, and prediction graphs
        --normalize ---- flag deciding whether or not to normalize input data

#### Usage Example

    ProtoMake test.csv test_model --early_stop --plots

The above command will create, train, and evaluate a model for the data in test.csv. It saves a model test_model.h5 in directory ./models/ and input, loss, and prediction graphs in the directory ./plots/ for analysis.

### The Proto Module

The Proto module contains the core functionality of the machine-learning portion of the package. It holds all of the model manipulation methods.

    ``` Python
    from MLProto import *

    """ Data operations (assign data, pred_data)
    ______________________________________________
    """

    stkr = Proto('test', data)
    stkr.train(25, True, True))
    stkr.evaluate()
    stkr.predict_data(pred_data)
    ```

The above code will take prepared data, create a Proto instance "test" for the data given, train for 25 epochs, save the model to the models folder as train.h5 and predict data points based on the user's prepared prediction data.

### The Data module

This module includes the data operation helper functions used by MLProto.

single_step_data takes a full dataset and creates a timeseries dataset from it for input into an LSTM model.

## Contributions

Please send pull requests! I am a full-time student, so development and support for MLProto will likely be slow with me working alone. I welcome any and all efforts to contribute!

## License

[GNU LGPLv3](https://choosealicense.com/licenses/lgpl-3.0/)
