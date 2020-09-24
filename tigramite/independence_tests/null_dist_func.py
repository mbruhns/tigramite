def _null_dist_func(samples, T, shuffle_neighbors, neighbors, array, x_indices):
    # for sam in range(self.sig_samples):

    # Generate random order in which to go through indices loop in
    # next step
    order = np.random.permutation(T).astype("int32")
    # print(order[:5])
    # Select a series of neighbor indices that contains as few as
    # possible duplicates

    restricted_permutation = tigramite_cython_code._get_restricted_permutation_cython(
        T=T,
        shuffle_neighbors=self.shuffle_neighbors,
        neighbors=neighbors,
        order=order,
    )
    array_shuffled = np.copy(array)
    for i in x_indices:
        array_shuffled[i] = array[i, restricted_permutation]

    null_dist = self.get_dependence_measure(array_shuffled, xyz)

    return null_dist
