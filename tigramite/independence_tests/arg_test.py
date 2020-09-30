import inspect
from tigramite.independence_tests import *
import numpy as np
import time
from timeit import default_timer as timer
import pandas as pd
import feather


def timeit(method):
    def timed(*args, **kw):
        ts = timer()
        result = method(*args, **kw)
        te = timeer()
        if "log_time" in kw:
            name = kw.get("log_name", method.__name__.upper())
            kw["log_time"][name] = int((te - ts) * 1000)
        else:
            print("%r  %2.2f ms" % (method.__name__, (te - ts) * 1000))
        return result

    return timed


def foo(a, b, c):
    print(a + b + c)


class Foo:
    def __init__():
        pass

    def bar0():
        pass

    def bar1():
        pass

    def _bar2():
        pass

    def __bar3():
        pass


if __name__ == "__main__":

    tests = ["ParCorr", "CMIknn", "CMIsymb", "GPDC"]
    # tests = {"parcorr": ParCorr(), "cmiknn": CMIknn(), "cmisymb": CMIsymb(), "gpdc": GPDC()}
    tests = [ParCorr(), CMIknn(), CMIsymb(), GPDC()]

    T = 250
    dim = 3
    df = T - dim
    array = np.random.normal(0, 1, size=(dim, T))
    value = 0.5
    conf_lev = 0.95

    # ParCorr benchmarking
    parcorr = ParCorr()

    func_dict = {
        parcorr._get_single_residuals: ("array", "target_var"),
        parcorr.get_dependence_measure: ("array", "xyz"),
        parcorr.get_shuffle_significance: ("array", "xyz", "value"),
        parcorr.get_analytic_significance: ("value", "T", "dim"),
        parcorr.get_analytic_confidence: ("value", "df", "conf_lev"),
        # parcorr.get_model_selection_criterion: ("j"=0, parents, tau_max=0)
    }

    parcorr._get_single_residuals(array=array, target_var=1)
    parcorr.get_dependence_measure(array=array, xyz=None)
    parcorr.get_shuffle_significance(array=array, xyz=None, value=value)
    parcorr.get_analytic_significance(value=value, T=T, dim=dim)
    parcorr.get_analytic_confidence(value=value, df=dim, conf_lev=conf_lev)
    # parcorr.get_model_selection_criterion(j=0, parents, tau_max=0)

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
        "xyz": None,
        "value": value,
        "df": dim,
        "conf_lev": conf_lev,
        "value": value,
        "conf_lev": conf_lev,
        "T": T,
        "dim": dim,
        "j": 0,
        "parents": None,
    }

    for function in parcorr_lst:
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

    for test in tests:
        method_list = [
            func[0]
            for func in inspect.getmembers(test, predicate=inspect.isfunction)
            if not func[0] == "__init__"
        ]
        print(method_list)
        break

        func_vars = test.__code__.co_varnames

        args = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
        args_sub = {key: args[key] for key in func_vars}

        foo(**args_sub)

        method_list = [
            func[0]
            for func in inspect.getmembers(Foo, predicate=inspect.isfunction)
            if not func[0] == "__init__"
        ]

        print(method_list)
