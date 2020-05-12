import numpy as np
import statsmodels.api as sm

def get_regression_ModelYearEofs(X, Y, num_eof, REA=0):
    # Note that the predictor here already include an constant term
    if REA==0:
        x_array = X
        mean_output_array = np.zeros([Y.shape[0], Y.shape[1], num_eof+2])
        for modIDX in range(Y.shape[0]):
            for yearIDX in range(Y.shape[1]):
                y_array = Y[modIDX, yearIDX]
                regress = sm.OLS(y_array, x_array).fit()
                mean_output_array[modIDX, yearIDX] = np.r_[regress.params, regress.rsquared*100]
        return mean_output_array
    elif REA==1:
        x_array = X
        mean_output_array = np.zeros([Y.shape[0], num_eof+2])
        for yearIDX in range(Y.shape[0]):
            y_array = Y[yearIDX]
            regress = sm.OLS(y_array, x_array).fit()
            mean_output_array[yearIDX]   = np.r_[regress.params, regress.rsquared*100]
        return mean_output_array

def get_regression_ModelEofs(vDT_REA_Both, array_vDT_HIS, num_eof):
    x_array = vDT_REA_Both
    mean_output_array = np.zeros([array_vDT_HIS.shape[0], num_eof+2])
    for modIDX in range(array_vDT_HIS.shape[0]):
        y_array = array_vDT_HIS[modIDX]
        regress = sm.OLS(y_array, x_array).fit()
        mean_output_array[modIDX]  = np.r_[regress.params, regress.rsquared*100]
    return mean_output_array

def get_regression_prediction(x_array, y_array, predict_coe, add_const=1):
    num = y_array.shape[0]
    if add_const == 0: new_x_array, new_predict_coe = x_array, predict_coe
    if add_const == 1: new_x_array, new_predict_coe = np.c_[np.ones(num), x_array], np.r_[1, predict_coe]
    regress = sm.OLS(y_array, new_x_array).fit()
    predict = regress.get_prediction(new_predict_coe)
    return predict