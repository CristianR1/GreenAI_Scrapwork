# for array computations and loading data
import numpy as np

# for building linear regression models and preparing data
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# for building and training neural networks
import tensorflow as tf


# reduce display precision on numpy arrays
def mini_classification():
    np.set_printoptions(precision=2)

    # suppress warnings 
    tf.get_logger().setLevel('ERROR')
    tf.autograph.set_verbosity(0)

    # Load the dataset from the text file
    data = np.loadtxt('./data/data_w3_ex1.csv', delimiter=',')

    # Split the inputs and outputs into separate arrays
    x = data[:,0]
    y = data[:,1]

    # Convert 1-D arrays into 2-D because the commands later will require it
    x = np.expand_dims(x, axis=1)
    y = np.expand_dims(y, axis=1)

    print(f"the shape of the inputs x is: {x.shape}")
    print(f"the shape of the targets y is: {y.shape}")

    # Get 60% of the dataset as the training set. Put the remaining 40% in temporary variables: x_ and y_.
    x_train, x_, y_train, y_ = train_test_split(x, y, test_size=0.40, random_state=1)

    # Split the 40% subset above into two: one half for cross validation and the other for the test set
    x_cv, x_test, y_cv, y_test = train_test_split(x_, y_, test_size=0.50, random_state=1)

    # Delete temporary variables
    del x_, y_

    print(f"the shape of the training set (input) is: {x_train.shape}")
    print(f"the shape of the training set (target) is: {y_train.shape}\n")
    print(f"the shape of the cross validation set (input) is: {x_cv.shape}")
    print(f"the shape of the cross validation set (target) is: {y_cv.shape}\n")
    print(f"the shape of the test set (input) is: {x_test.shape}")
    print(f"the shape of the test set (target) is: {y_test.shape}")

    # Initialize the class
    scaler_linear = StandardScaler()

    # Compute the mean and standard deviation of the training set then transform it
    X_train_scaled = scaler_linear.fit_transform(x_train)

    print(f"Computed mean of the training set: {scaler_linear.mean_.squeeze():.2f}")
    print(f"Computed standard deviation of the training set: {scaler_linear.scale_.squeeze():.2f}")


    # Initialize the class
    linear_model = LinearRegression()

    # Train the model
    linear_model.fit(X_train_scaled, y_train )
    # Feed the scaled training set and get the predictions
    yhat = linear_model.predict(X_train_scaled)

    # Use scikit-learn's utility function and divide by 2
    print(f"training MSE (using sklearn function): {mean_squared_error(y_train, yhat) / 2}")

    # for-loop implementation
    total_squared_error = 0

    for i in range(len(yhat)):
        squared_error_i  = (yhat[i] - y_train[i])**2
        total_squared_error += squared_error_i                                              

    mse = total_squared_error / (2*len(yhat))

    print(f"training MSE (for-loop implementation): {mse.squeeze()}")
    # Scale the cross validation set using the mean and standard deviation of the training set
    X_cv_scaled = scaler_linear.transform(x_cv)

    print(f"Mean used to scale the CV set: {scaler_linear.mean_.squeeze():.2f}")
    print(f"Standard deviation used to scale the CV set: {scaler_linear.scale_.squeeze():.2f}")

    # Feed the scaled cross validation set
    yhat = linear_model.predict(X_cv_scaled)

    # Use scikit-learn's utility function and divide by 2
    print(f"Cross validation MSE: {mean_squared_error(y_cv, yhat) / 2}")

    # Instantiate the class to make polynomial features
    poly = PolynomialFeatures(degree=2, include_bias=False)

    # Compute the number of features and transform the training set
    X_train_mapped = poly.fit_transform(x_train)

    # Preview the first 5 elements of the new training set. Left column is `x` and right column is `x^2`
    # Note: The `e+<number>` in the output denotes how many places the decimal point should 
    # be moved. For example, `3.24e+03` is equal to `3240`
    print(X_train_mapped[:5])

    # Instantiate the class
    scaler_poly = StandardScaler()

    # Compute the mean and standard deviation of the training set then transform it
    X_train_mapped_scaled = scaler_poly.fit_transform(X_train_mapped)

    # Preview the first 5 elements of the scaled training set.
    print(X_train_mapped_scaled[:5])

    # Initialize the class
    model = LinearRegression()

    # Train the model
    model.fit(X_train_mapped_scaled, y_train )

    # Compute the training MSE
    yhat = model.predict(X_train_mapped_scaled)
    print(f"Training MSE: {mean_squared_error(y_train, yhat) / 2}")

    # Add the polynomial features to the cross validation set
    X_cv_mapped = poly.transform(x_cv)

    # Scale the cross validation set using the mean and standard deviation of the training set
    X_cv_mapped_scaled = scaler_poly.transform(X_cv_mapped)

    # Compute the cross validation MSE
    yhat = model.predict(X_cv_mapped_scaled)
    print(f"Cross validation MSE: {mean_squared_error(y_cv, yhat) / 2}")

    # Initialize lists to save the errors, models, and feature transforms
    train_mses = []
    cv_mses = []
    models = []
    polys = []
    scalers = []

    # Loop over 10 times. Each adding one more degree of polynomial higher than the last.
    for degree in range(1,11):
        
        # Add polynomial features to the training set
        poly = PolynomialFeatures(degree, include_bias=False)
        X_train_mapped = poly.fit_transform(x_train)
        polys.append(poly)
        
        # Scale the training set
        scaler_poly = StandardScaler()
        X_train_mapped_scaled = scaler_poly.fit_transform(X_train_mapped)
        scalers.append(scaler_poly)
        
        # Create and train the model
        model = LinearRegression()
        model.fit(X_train_mapped_scaled, y_train )
        models.append(model)
        
        # Compute the training MSE
        yhat = model.predict(X_train_mapped_scaled)
        train_mse = mean_squared_error(y_train, yhat) / 2
        train_mses.append(train_mse)
        
        # Add polynomial features and scale the cross validation set
        X_cv_mapped = poly.transform(x_cv)
        X_cv_mapped_scaled = scaler_poly.transform(X_cv_mapped)
        
        # Compute the cross validation MSE
        yhat = model.predict(X_cv_mapped_scaled)
        cv_mse = mean_squared_error(y_cv, yhat) / 2
        cv_mses.append(cv_mse)

    # Get the model with the lowest CV MSE (add 1 because list indices start at 0)
    # This also corresponds to the degree of the polynomial added
    degree = np.argmin(cv_mses) + 1
    print(f"Lowest CV MSE is found in the model with degree={degree}")

    # Add polynomial features to the test set
    X_test_mapped = polys[degree-1].transform(x_test)

    # Scale the test set
    X_test_mapped_scaled = scalers[degree-1].transform(X_test_mapped)

    # Compute the test MSE
    yhat = models[degree-1].predict(X_test_mapped_scaled)
    test_mse = mean_squared_error(y_test, yhat) / 2

    print(f"Training MSE: {train_mses[degree-1]:.2f}")
    print(f"Cross Validation MSE: {cv_mses[degree-1]:.2f}")
    print(f"Test MSE: {test_mse:.2f}")

    # Add polynomial features
    degree = 1
    poly = PolynomialFeatures(degree, include_bias=False)
    X_train_mapped = poly.fit_transform(x_train)
    X_cv_mapped = poly.transform(x_cv)
    X_test_mapped = poly.transform(x_test)

mini_classification()
