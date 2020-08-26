import ray
ray.init()

@ray.remote
def f(x):
    return x * x


#serial = [f(i) for i in range(size)]
futures = [f.remote(i) for i in range(size)]
