from tigramite.independence_tests import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from timeit import default_timer as timer
import feather
import json
import pprint
import os
import sys


def get_payload(data):
    arg_dict = {}


if __name__ == "__main__":

    file_list = []
    data_path = os.path.expanduser("~") + "/CauseMeData/Datasets/"

    df_benchmarking = pd.DataFrame(columns=["Function", "N", "T", "Time"])

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
        cmiknn._get_nearest_neighbors: ("array", "xyz", "knn"),
        cmiknn.get_dependence_measure: ("array", "xyz"),
        cmiknn.get_shuffle_significance: ("array", "xyz", "value"),
        gpdc._get_single_residuals: ("array", "target_var"),
        # gpdc.get_model_selection_criterion: ("j", "parents"),
        gpdc.get_dependence_measure: ("array", "xyz"),
        gpdc.get_shuffle_significance: ("array", "xyz", "value"),
        gpdc.get_analytic_significance: ("value", "T", "dim")
        # parcorr.get_model_selection_criterion: ("j"=0, parents,
        # tau_max=0)
    }

    for root, dirs, files in os.walk(data_path):
        for name in files:
            if name.endswith(".json"):
                file_list.append(os.path.join(root, name))

    for file in file_list:
        with open(file) as json_file:
            data = json.load(json_file)
            datasets = np.asarray(data["datasets"])
            realizations, T, dim = datasets.shape
            for i in range(realizations):
                # Transpose to get correct shape of array
                array = datasets[i, :, :].T

                arg_dict = {
                    "array": array,
                    "target_var": 1,
                    "xyz": np.arange(dim),
                    "df": T - dim,
                    "conf_lev": 0.95,
                    "value": 0.5,
                    "T": T,
                    "dim": dim,
                    "j": 0,
                    "parents": None,
                    "knn": 1,  # How to choose this value?
                }

                for function in func_dict:
                    class_name = function.__module__[29:]
                    args_sub = {
                        key: arg_dict[key] for key in func_dict[function]
                    }
                    start = timer()
                    function(**args_sub)
                    end = timer() - start
                    measurement = {
                        "Function": f"{class_name}.{function.__name__}",
                        "N": arg_dict["dim"],
                        "T": arg_dict["T"],
                        "Time": end,
                    }
                    df_benchmarking = df_benchmarking.append(
                        measurement, ignore_index=True
                    )

    print(df_benchmarking)

    sys.exit()

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
        cmiknn._get_nearest_neighbors: ("array", "xyz", "knn"),
        cmiknn.get_dependence_measure: ("array", "xyz"),
        cmiknn.get_shuffle_significance: ("array", "xyz", "value"),
        gpdc._get_single_residuals: ("array", "target_var"),
        # gpdc.get_model_selection_criterion: ("j", "parents"),
        gpdc.get_dependence_measure: ("array", "xyz"),
        gpdc.get_shuffle_significance: ("array", "xyz", "value"),
        gpdc.get_analytic_significance: ("value", "T", "dim")
        # parcorr.get_model_selection_criterion: ("j"=0, parents, tau_max=0)
    }

    df_benchmarking = pd.DataFrame(columns=["Function", "N", "T", "Time"])

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
        "knn": 1,  # How to choose this value?
    }

    for function in func_dict:
        class_name = function.__module__[29:]
        args_sub = {key: arg_dict[key] for key in func_dict[function]}
        start = timer()
        function(**args_sub)
        end = timer() - start
        measurement = {
            "Function": f"{class_name}.{function.__name__}",
            "N": arg_dict["dim"],
            "T": arg_dict["T"],
            "Time": end,
        }
        df_benchmarking = df_benchmarking.append(
            measurement, ignore_index=True
        )

    print(df_benchmarking)
