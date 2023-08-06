__all__ = ['lib']

import numpy as np

from mkkm_mr.lib import _check_dims, comb_func, kernel_kmeans_iter, calc_objective, update_kernel_weights, \
    weight_normalize


def mkkm_mr(K, M, cluster_count, lambda_):  # myregmultikernelclustering
    """
    Clusters given kernels using kernel kmeans
    :param K: kernel matrices of kxnxn
    :param M:
    :param cluster_count:
    :param lambda_:
    :return:
    """
    _check_dims(K, can_2d=False)
    num_kernel = K.shape[0]  # number of kernels k
    gamma = None  # distances
    # noinspection PyTypeChecker
    obj_curr: np.ndarray = None
    # keep as long as this is not the first iteration and there is not a big different finish it
    # PS: we can add an iteration limit here
    while True:
        if gamma is None:
            gamma = np.ones(num_kernel) / num_kernel

        KC = comb_func(K, gamma)
        H = kernel_kmeans_iter(KC, cluster_count)

        obj_prev = obj_curr
        obj_curr = calc_objective(H, K, M, gamma, lambda_)

        gamma = update_kernel_weights(H, K, M, lambda_)

        if obj_prev is not None and np.abs((obj_prev - obj_curr) / obj_prev) < 1e-6:
            break

    H_normalized = weight_normalize(H, cluster_count)
    return H_normalized, gamma, obj_curr
