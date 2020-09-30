from tigramite.independence_tests import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from timeit import default_timer as timer
import feather

if __name__ == "__main__":

    T = 250
    dim = 3
    df = T - dim
    array = np.random.normal(0, 1, size=(dim, T))
    value = 0.5
    conf_lev = 0.95

    # ParCorr benchmarking
    parcorr = ParCorr()
    cmiknn = CMIknn()
    cmisymb = CMIsymb()
    gpdc = GPDC()

    func_dict = {
        parcorr._get_single_residuals: ("array", "target_var"),
        parcorr.get_dependence_measure: ("array", "xyz"),
        parcorr.get_shuffle_significance: ("array", "xyz", "value"),
        parcorr.get_analytic_significance: ("value", "T", "dim"),
        parcorr.get_analytic_confidence: ("value", "df", "conf_lev"),
        cmiknn._get_nearest_neighbors:  ("array", "xyz", "knn"),
        cmiknn.get_dependence_measure:  ("array", "xyz"),
        cmiknn.get_shuffle_significance:    ("array", "xyz", "value")
        # parcorr.get_model_selection_criterion: ("j"=0, parents, tau_max=0)
    }

    df_benchmarking = pd.DataFrame(columns=["Function", "N", "T", "Time"])

    parcorr_lst = [
        parcorr._get_single_residuals,
        parcorr.get_dependence_measure,
        parcorr.get_shuffle_significance,
        parcorr.get_analytic_significance,
        parcorr.get_analytic_confidence,
    ]

    arg_dict = {
        "array": array,
        "target_var": 1,
        "xyz": np.arange(dim),
        "value": value,
        "df": dim,
        "conf_lev": conf_lev,
        "value": value,
        "conf_lev": conf_lev,
        "T": T,
        "dim": dim,
        "j": 0,
        "parents": None,
        "knn":  1 # How to choose this value?
    }

    for function in func_dict:
        # func_vars = element.__code__.co_varnames
        args_sub = {key: arg_dict[key] for key in func_dict[function]}
        start = timer()
        function(**args_sub)
        end = timer() - start
        new_row = {
            "Function": function.__name__,
            "N": arg_dict["dim"],
            "T": arg_dict["T"],
            "Time": end,
        }
        df_benchmarking = df_benchmarking.append(new_row, ignore_index=True)

    print(df_benchmarking)
