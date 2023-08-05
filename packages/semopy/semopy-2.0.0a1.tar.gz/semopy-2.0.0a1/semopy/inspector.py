#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inspector module helps researcher fetch information on estimates."""
from .model import Model
import pandas as pd
import numpy as np
import stats


def inspect(model, mode='list', what='est', information='expected'):
    """
    Get fancy view of model parameters estimates.

    Parameters
    ----------
    model : str
        Model.
    mode : str, optional
        If 'list', pd.DataFrame with estimates and p-values is returned.
        If 'mx', a dictionary of matrices is returned. The default is 'list'.
    what : TYPE, optional
        Used only if mode == 'mx'. If 'est', matrices have estimated
        values. If 'start', matrices have starting values. If 'name', matrices
        have names inplace of their parameters. The default is 'est'.
    information : str
        If 'expected', expected Fisher information is used. Otherwise,
        observed information is employed. If None, the no p-values are
        calculated. No effect is what is 'mx'. The default is 'expected'.

    Returns
    -------
    pd.DataFrame | dict
        Dataframe or mapping matrix_name->matrix.

    """
    if mode == 'list':
        return inspect_list(model, information=information)
    elif mode == 'mx':
        return inspect_matrices(model, what=what)


def inspect_matrices(model: Model, what='est'):
    """
    Get model matrices.

    Parameters
    ----------
    model : Model
        Model.
    what : str, optional
        If 'est', matrices have estimated values. If 'start', matrices have
        starting values. If 'name', matrices have names inplace of their
        parameters. The default is 'est'.

    Raises
    ------
    Exception
        DESCRIPTION.

    Returns
    -------
    ret : TYPE
        DESCRIPTION.

    """
    ret = dict()
    if hasattr(model, 'mx_beta'):
        matrix = model.mx_beta
        name = 'Beta'
        names = model.names_beta
        if what != 'est':
            matrix = _set_values(model.parameters, matrix, what == 'start')
        ret[name] = pd.DataFrame(matrix, columns=names[1],
                                 index=names[0])

    if hasattr(model, 'mx_gamma1'):
        matrix = model.mx_gamma1
        name = 'Gamma1'
        names = model.names_gamma1
        if what != 'est':
            matrix = _set_values(model.parameters, matrix, what == 'start')
        ret[name] = pd.DataFrame(matrix, columns=names[1],
                                 index=names[0])

    if hasattr(model, 'mx_gamma2'):
        matrix = model.mx_gamma2
        name = 'Gamma2'
        names = model.names_gamma2
        if what != 'est':
            matrix = _set_values(model.parameters, matrix, what == 'start')
        ret[name] = pd.DataFrame(matrix, columns=names[1],
                                 index=names[0])

    if hasattr(model, 'mx_lambda'):
        matrix = model.mx_lambda
        name = 'Lambda'
        names = model.names_lambda
        if what != 'est':
            matrix = _set_values(model.parameters, matrix, what == 'start')
        ret[name] = pd.DataFrame(matrix, columns=names[1],
                                 index=names[0])
    if hasattr(model, 'mx_psi'):
        matrix = model.mx_psi
        name = 'Psi'
        names = model.names_psi
        if what != 'est':
            matrix = _set_values(model.parameters, matrix, what == 'start')
        ret[name] = pd.DataFrame(matrix, columns=names[1],
                                 index=names[0])
    if hasattr(model, 'mx_theta'):
        matrix = model.mx_theta
        name = 'Theta'
        names = model.names_theta
        if what != 'est':
            matrix = _set_values(model.parameters, matrix, what == 'start')
        ret[name] = pd.DataFrame(matrix, columns=names[1],
                                 index=names[0])

    if hasattr(model, 'mx_d'):
        matrix = model.mx_d
        name = 'D'
        names = model.names_d
        if what != 'est':
            matrix = _set_values(model.parameters, matrix, what == 'start')
        ret[name] = pd.DataFrame(matrix, columns=names[1],
                                 index=names[0])

    if hasattr(model, 'mx_v'):
        matrix = model.mx_v
        name = 'v'
        if what != 'est':
            matrix = _set_values(model.parameters, matrix, what == 'start')
        ret[name] = matrix[0, 0]

    if hasattr(model, 'mx_data_imp'):
        matrix = model.mx_data_imp
        name = 'Imputation'
        names = model.names_data_imp
        if what != 'est':
            matrix = _set_values(model.parameters, matrix, what == 'start')
        ret[name] = pd.DataFrame(matrix, columns=names[1],
                                 index=names[0])

    return ret


def inspect_list(model: Model, information='expected'):
    """
    Get a pandas DataFrame containin a view of parameters estimates.

    Parameters
    ----------
    model : Model
        Model.
    information : str
        If 'expected', expected Fisher information is used. Otherwise,
        observed information is employed. If None, the no p-values are
        calculated. The default is 'expected'.

    Returns
    -------
    pd.DataFrame
        DataFrame with parameters information.

    """
    if not hasattr(model, 'last_result'):
        raise Exception('Can''t inspect model parameters estimates as they \
                        don''t exist')
    res = list()
    vals = model.param_vals
    if information is not None:
        se = stats.calc_se(model, information=information)
        zscores = stats.calc_zvals(model, std_errors=se)
        pvals = stats.calc_pvals(model, z_scores=zscores)
    else:
        se = ['-'] * len(vals)
        zscores = pvals = se
    keys = list(model.parameters.keys())
    keys_active = [k for k in keys if model.parameters[k].active]
    # Beta
    if hasattr(model, 'mx_beta'):
        mx = model.mx_beta
        names = model.names_beta
        op = '~'
        for name, param in model.parameters.items():
            for loc in param.locations:
                if loc.matrix is mx:
                    ind = loc.indices
                    a, b = names[0][ind[0]], names[1][ind[1]]
                    if param.active:
                        i = keys_active.index(name)
                        val = vals[i]
                        std = se[i]
                        zs = zscores[i]
                        pval = pvals[i]
                    else:
                        val = param.start
                        std = '-'
                        zs = '-'
                        pval = '-'
                    res.append((a, op, b, val, std, zs, pval))

    means = list()
    # Gamma1
    if hasattr(model, 'mx_gamma1'):
        mx = model.mx_gamma1
        names = model.names_gamma1
        op = '~'
        for name, param in model.parameters.items():
            for loc in param.locations:
                if loc.matrix is mx:
                    ind = loc.indices
                    a, b = names[0][ind[0]], names[1][ind[1]]
                    if param.active:
                        i = keys_active.index(name)
                        val = vals[i]
                        std = se[i]
                        zs = zscores[i]
                        pval = pvals[i]
                    else:
                        val = param.start
                        std = '-'
                        zs = '-'
                        pval = '-'
                    if b == '1':
                        means.append((a, op, b, val, std, zs, pval))
                    else:
                        res.append((a, op, b, val, std, zs, pval))

    # Gamma2
    if hasattr(model, 'mx_gamma2'):
        mx = model.mx_gamma2
        names = model.names_gamma2
        op = '~'
        for name, param in model.parameters.items():
            for loc in param.locations:
                if loc.matrix is mx:
                    ind = loc.indices
                    a, b = names[0][ind[0]], names[1][ind[1]]
                    if param.active:
                        i = keys_active.index(name)
                        val = vals[i]
                        std = se[i]
                        zs = zscores[i]
                        pval = pvals[i]
                    else:
                        val = param.start
                        std = '-'
                        zs = '-'
                        pval = '-'
                    if b == '1':
                        means.append((a, op, b, val, std, zs, pval))
                    else:
                        res.append((a, op, b, val, std, zs, pval))

    # Lambda
    if hasattr(model, 'mx_lambda'):
        mx = model.mx_lambda
        names = model.names_lambda
        op = '~'
        for name, param in model.parameters.items():
            for loc in param.locations:
                if loc.matrix is mx:
                    ind = loc.indices
                    a, b = names[0][ind[0]], names[1][ind[1]]
                    if param.active:
                        i = keys_active.index(name)
                        val = vals[i]
                        std = se[i]
                        zs = zscores[i]
                        pval = pvals[i]
                    else:
                        val = param.start
                        std = '-'
                        zs = '-'
                        pval = '-'
                    res.append((a, op, b, val, std, zs, pval))
    res.extend(means)
    means.clear()
    # Psi
    if hasattr(model, 'mx_psi'):
        mx = model.mx_psi
        names = model.names_psi
        op = '~~'
        obs_exo = set(model.vars['observed']) & model.vars['exogenous']
        for name, param in model.parameters.items():
            for loc in param.locations:
                if loc.matrix is mx:
                    ind = loc.indices
                    a, b = names[0][ind[0]], names[1][ind[1]]
                    if param.active:
                        i = keys_active.index(name)
                        val = vals[i]
                        std = se[i]
                        zs = zscores[i]
                        pval = pvals[i]
                    else:
                        if a in obs_exo and b in obs_exo:
                            continue
                        val = param.start
                        std = '-'
                        zs = '-'
                        pval = '-'
                    res.append((a, op, b, val, std, zs, pval))
    # Theta
    if hasattr(model, 'mx_theta'):
        mx = model.mx_theta
        names = model.names_theta
        op = '~~'
        for name, param in model.parameters.items():
            for loc in param.locations:
                if loc.matrix is mx:
                    ind = loc.indices
                    a, b = names[0][ind[0]], names[1][ind[1]]
                    if param.active:
                        i = keys_active.index(name)
                        val = vals[i]
                        std = se[i]
                        zs = zscores[i]
                        pval = pvals[i]
                    else:
                        val = param.start
                        std = '-'
                        zs = '-'
                        pval = '-'
                    res.append((a, op, b, val, std, zs, pval))

    # D -- Variance of random effects matrix
    if hasattr(model, 'mx_d'):
        mx = model.mx_d
        names = model.names_d
        op = 'RF'
        for name, param in model.parameters.items():
            for loc in param.locations:
                if loc.matrix is mx:
                    ind = loc.indices
                    a, b = names[0][ind[0]], names[1][ind[1]]
                    if param.active:
                        i = keys_active.index(name)
                        val = vals[i]
                        std = se[i]
                        zs = zscores[i]
                        pval = pvals[i]
                    else:
                        val = param.start
                        std = '-'
                        zs = '-'
                        pval = '-'
                    res.append((a, op, b, val, std, zs, pval))
    # v -- Variance of random effects variable
    if hasattr(model, 'mx_v'):
        mx = model.mx_v
        names = model.names_v
        op = 'RF(v)'
        for name, param in model.parameters.items():
            for loc in param.locations:
                if loc.matrix is mx:
                    ind = loc.indices
                    a, b = names[0][ind[0]], names[1][ind[1]]
                    if param.active:
                        i = keys_active.index(name)
                        val = vals[i]
                        std = se[i]
                        zs = zscores[i]
                        pval = pvals[i]
                    else:
                        val = param.start
                        std = '-'
                        zs = '-'
                        pval = '-'
                    res.append((a, op, b, val, std, zs, pval))
    # Data_imp -- Matrix of imputed data
    if hasattr(model, 'mx_data_imp'):
        mx = model.mx_data_imp
        names = model.names_data_imp
        op = '@'
        for name, param in model.parameters.items():
            for loc in param.locations:
                if loc.matrix is mx:
                    ind = loc.indices
                    a, b = names[0][ind[0]], names[1][ind[1]]
                    if param.active:
                        i = keys_active.index(name)
                        val = vals[i]
                        std = se[i]
                        zs = zscores[i]
                        pval = pvals[i]
                    else:
                        val = param.start
                        std = '-'
                        zs = '-'
                        pval = '-'
                    res.append((a, op, b, val, std, zs, pval))

    return pd.DataFrame(res,
                        columns=['lval', 'op', 'rval', 'Estimate', 'Std. Err',
                                 'z-value', 'p-value'])


def _set_values(params: dict, ref: np.ndarray, start=True):
    mx = ref.astype('O')
    for name, param in params.items():
        for loc in param.locations:
            if loc.matrix is ref:
                if start:
                    mx[loc.indices] = param.start
                else:
                    mx[loc.indices] = name
    return mx
