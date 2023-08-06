
###############################################################################################################
# FE_groupby_master
###############################################################################################################
import numpy as np
import pandas as pd
import os, sys, gc, time, datetime

# merge inplace
def pd_merge(d1, d2, on, how = 'left'):
    keys = on if type(on) is list else [on]
    d2 = d1[keys].merge(d2, on = keys, how = how) # uid in d2 must unique
    if len(d2) != len(d1):
        print('[***] error, uid in d2 is not unique')
    d2 = d2.drop(keys, axis = 1)    
    d1[d2.columns] = d2; del d2; gc.collect()
    return d1

# formated name
def get_name(keys, col, op, s = 1, RATIO = False, DIV = False, DIFF = False):
    if op == 'cumcount':
        return 'CUM_COUNT_({})'.format('_'.join(keys))
    if op == 'count' or col is None:
        return 'COUNT_({})'.format('_'.join(keys))

    if op in ['cumsum', 'shift']:            
        if op =='cumsum':
            name = 'CUM_SUM_({})_({})'.format('_'.join(keys), col)
        if op == 'shift':
            name = 'SHIFT_{}_({})_({})'.format(str(s), '_'.join(keys), col)
    else:
        head = 'RATIO_' if RATIO else 'AGG_'
        name = head + '{}_({})_({})'.format(op.upper(), '_'.join(keys), col)
    name += '_DIFF' if DIFF else ''        
    name += '_DIV' if DIV else ''
    return name

# groupby for cumcount, cumsum, shift
def _FE_groupyby_master_time(train, test, keys, col, op = 'cumcount', s = 1):
    n_train = len(train)
    cols_use = keys if col is None else keys + [col]
    df = pd.concat([train[cols_use], test[cols_use]], axis = 0).reset_index(drop = True)
    if 'cum' in op:
        col = keys[0] if col is None else col
        df_fe = df.groupby(keys)[col].agg(op).to_frame()
    elif 'shift' in op:
        df_fe = df.groupby(keys)[col].shift(s).to_frame()
    else:
        print('[***] error op')
        return train, test
    return df_fe[:n_train].reset_index(drop = True), df_fe[n_train:].reset_index(drop = True)

# FE_groupyby_master
def FE_groupyby_master(train, test, keys, col = None, op = 'nunique', s = 1, \
                       RATIO = False, DIV = False, DIFF = False, ret_fe = False, ret_map = False):
    name = get_name(keys, col, op, s, RATIO, DIV, DIFF)
    print(name) 
    # ++++++++++++++++++++++++++++++++++++++++ time seties ++++++++++++++++++++++++++++++++++++++++++++
    if op in ['cumcount', 'cumsum', 'shift']:
        train_fe, test_fe = _FE_groupyby_master_time(train, test, keys, col, op, s)
        train_fe.columns = [name]
        test_fe.columns = [name]

    # ++++++++++++++++++++++++++++++++++++++++ not time seties ++++++++++++++++++++++++++++++++++++++++    
    else:
        cols_use = keys if col is None else keys + [col]
        df = pd.concat([train[cols_use], test[cols_use]], axis = 0).reset_index(drop = True)
        if col is None or op == 'count':
            df_map = df.groupby(keys).size().to_frame()       # COUNT
        elif op != 'count':
            df_map = df.groupby(keys)[col].agg(op).to_frame() # AGG
            if RATIO:
                df_group_size = df.groupby(keys)[col].count().to_frame()
                df_map = df_map / df_group_size               # RATIO
        else:
            print('[***] error op')
            return train, test
        
        # ==================== MAP ==========================
        name = get_name(keys, col, op, s, RATIO, DIV, DIFF)
        df_map.reset_index(inplace = True)
        df_map.columns = keys + [name]
        if ret_map:
            return df_map #
        train_fe = train[keys].merge(df_map, on = keys, how = 'left')
        test_fe = test[keys].merge(df_map, on = keys, how = 'left')
    
    # ==================== DIV or DIFF ==========================
    if op != 'count' and DIFF:
        train_fe[name] = train[col] - train_fe[name]
        test_fe[name] = test[col] - test_fe[name]
    if op != 'count' and DIV:
        train_fe[name] = train[col] / train_fe[name]
        test_fe[name] = test[col] / test_fe[name]
    if ret_fe:
        return train_fe, test_fe #
    train[train_fe.columns] = train_fe; del train_fe; gc.collect();
    test[test_fe.columns] = test_fe; del test_fe; gc.collect();
    return train, test

def FE_pivot(train, test, idxs, cols, val = None, op = 'count'):
    cols_sel = idxs + cols if val is None else idxs + cols + [val]
    df = pd.concat([train[cols_sel], test[cols_sel]], axis = 0).reset_index(drop = True)
    if val is None:
        val = 'ONE'
        df['ONE'] = 1
        
    # print(train.shape, test.shape)    
    # print(idxs, cols, val, op)
    df_map = pd.pivot_table(df, 
                            index = idxs, 
                            values = [val],
                            columns = cols,
                            aggfunc = op,
                            fill_value = 0)
    name_idxs = '_'.join(idxs)
    name_cols = '_'.join(cols)
    df_map.columns = ['PIVOT_({})_{}_({})_({})_{}'.\
                      format(name_idxs, op.upper(), c[0], name_cols, '_'.join([str(ci) for ci in c[1:]])) for c in df_map]
    print(df_map.columns[0])
    df_map.reset_index(inplace = True)
    return df_map