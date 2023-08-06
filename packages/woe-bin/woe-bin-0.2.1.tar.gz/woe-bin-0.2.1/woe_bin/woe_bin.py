# -*- coding: utf-8 -*-
"""
Created on 2020/5/14 18:07

@author: jinxinbo
"""

# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import time


class woe_bin(object):
    def __init__(self, indata, target, min_group_rate=0.1, max_bin=6):
        self.indata = indata
        self.target = target
        self.min_group_rate = min_group_rate
        self.max_bin = max_bin

        self.min_num = np.round(len(self.indata) * self.min_group_rate, 0)  # 限定最小分组数

    def read_data(self, tabname, tabkey):
        return pd.read_csv(tabname, index_col=tabkey)

    def bin_trans(self, var, sp_list):
        # sp_list = [1, 3.5]
        for i, vi in enumerate(sp_list):
            if var <= vi:
                bin = i + 1
                break
            else:
                bin = len(sp_list) + 1
        return bin

    # bin_trans(12, [1, 3.5, 11])

    def woe_trans(self, var, sp_list, woe_list):
        if np.isnan(sp_list).any():
            if pd.isna(var):
                woe = woe_list[np.where(np.isnan(sp_list))][0]
            else:
                for i, vi in enumerate(sp_list):
                    if var <= vi:
                        woe = woe_list[i]
                        break
                    else:
                        woe = woe_list[len(woe_list) - 1]
        else:
            for i, vi in enumerate(sp_list):
                if var <= vi:
                    woe = woe_list[i]
                    break
                else:
                    woe = woe_list[len(woe_list) - 1]
        return woe

    def get_bin(self, tabname, varname, sp_list):
        tab1 = tabname.copy()
        kwds = {"sp_list": sp_list}
        tab1['bin'] = tab1[varname].apply(self.bin_trans, **kwds)

        return tab1[['target', 'bin']]

    # test = get_bin(data1, 'td_id_3m', [1, 3.5])



    def get_bound(self, sp_list):
        # sp_list = [1, 3.5]
        ul = sp_list.copy()
        ll = sp_list.copy()
        ul.append(float("inf"))
        ll.insert(0, float("-inf"))

        sp_dict = {'bin': [i + 1 for i in list(range(len(sp_list) + 1))], 'll': ll, 'ul': ul}
        return pd.DataFrame(sp_dict)

    def get_dist(self, df, t0, t1):
        '''

        :param df: 
        :param t0: t0和t1以全部数据来计算woe和iv
        :param t1: 
        :return: 
        '''
        # t_sum = pd.pivot_table(df, index='bin', columns='target', values='one', aggfunc=[np.sum])
        # t1 = df.target.sum()
        # t0 = len(df) - t1
        t_sum = df.groupby(['bin'])['target', 'one'].sum()
        t_sum.rename(columns={'target': 'p1'}, inplace=True)
        t_sum['p0'] = t_sum['one'] - t_sum['p1']
        t_sum.reset_index(level=0, inplace=True)

        t_sum['p1_r'] = t_sum['p1'] / t1 + 1e-6
        t_sum['p0_r'] = t_sum['p0'] / t0 + 1e-6
        t_sum['woe'] = np.log(t_sum['p1_r'] / t_sum['p0_r'])
        t_sum['iv0'] = (t_sum['p1_r'] - t_sum['p0_r']) * t_sum['woe']

        t_sum.drop(['one', 'p0_r', 'p1_r'], axis=1, inplace=True)
        return t_sum

    def get_mapiv_result(self, tabname, varname, sp_list, t0, t1):
        boundry = self.get_bound(sp_list)
        bin = self.get_bin(tabname, varname, sp_list)

        bin['one'] = 1
        mapiv1 = self.get_dist(bin, t0, t1)

        return boundry.merge(mapiv1, on='bin')

    # test = pd.DataFrame({'bin':[0,1,1,2,3,0,0,3,2],'target':[0,0,1,0,0,1,1,1,1]})
    # test['one'] = 1
    # test1 = get_dist(test)
    #
    # test1.index


    def get_iv(self, intab, varname, split_i):
        data_l = intab[intab[varname] <= split_i]
        data_u = intab[intab[varname] > split_i]

        p1 = intab['target'].sum()
        p0 = len(intab) - p1

        if p1 > 0 and p0 > 0:  # 分割后的数据满足最小分组数要求
            p1_l = data_l['target'].sum()
            p0_l = len(data_l) - p1_l

            p1_u, p0_u = p1 - p1_l, p0 - p0_l
            p1_u, p1_l, p0_u, p0_l = p1_u + 1e-6, p1_l + 1e-6, p0_u + 1e-6, p0_l + 1e-6
            if p0_l > 0 and p0_u > 0 and p1_l > 0 and p1_u > 0 and (p0_l + p1_l) >= self.min_num and (
                p0_u + p1_u) >= self.min_num:

                woe_l = np.log((p1_l / p1) / (p0_l / p0) + 1e-6)
                iv_l = (p1_l / p1 - p0_l / p0) * np.log((p1_l / p1) / (p0_l / p0) + 1e-6)
                woe_u = np.log((p1_u / p1) / (p0_u / p0) + 1e-6)
                iv_u = (p1_u / p1 - p0_u / p0) * np.log((p1_u / p1) / (p0_u / p0) + 1e-6)
            else:
                return (0, -1)
                # iv = iv_l + iv_u
        else:
            return (0, -1)
        return (iv_l + iv_u, np.float(woe_l < woe_u))

    def split_var_bin(self, tabname, varname, woe_direct):
        t1 = np.unique(tabname[varname])
        if len(t1) > 1:
            t2 = [round((t1[i] + t1[i + 1]) / 2.0, 4) for i in range(len(t1) - 1)]  # 切割点平均值
            t3 = [(i, self.get_iv(tabname, varname, i)) for i in t2]
            t3_1 = [j for j in t3 if j[1][1] == woe_direct and j[1][0] >= 0.001]  # 与首次切割方向相同
            if len(t3_1) > 0:

                t3_max = [i[1][0] for i in t3_1]
                max_index = t3_max.index(max(t3_max))

                split_value = t3_1[max_index][0]
                gain_iv = max(t3_max)
                tab_l = tabname[tabname[varname] <= split_value]
                tab_u = tabname[tabname[varname] > split_value]

                split_value_i, max_iv_i = self.split_var_bin(tab_l, varname, woe_direct)
                split_value_j, max_iv_j = self.split_var_bin(tab_u, varname, woe_direct)
            else:
                return [], []
        else:
            return [], []
        # return split_value.append(split_value_i.append(split_value_j))
        return [split_value] + split_value_i + split_value_j, [gain_iv] + max_iv_i + max_iv_j

    def first_split(self, tabname, varname):
        # 第一次决定分割的woe方向

        t1 = np.unique(tabname[varname])
        t2 = [round((t1[i] + t1[i + 1]) / 2.0, 4) for i in range(len(t1) - 1)]  # 切割点平均值
        t3 = [(i, self.get_iv(tabname, varname, i)) for i in t2]
        # t3_1 = [j for j in t3 if j[1][0] >= 0.001]

        t3_max = [i[1][0] for i in t3]
        max_index = t3_max.index(max(t3_max))

        return t3[max_index][0], t3[max_index][1][1]

    def get_nulldata_mapiv(self, tab, t0, t1):
        null_t1 = tab.target.sum()
        null_t0 = len(tab) - null_t1
        null_p1r = null_t1 / t1 + 1e-6
        null_p0r = null_t0 / t0 + 1e-6
        null_woe = np.log(null_p1r / null_p0r)
        null_iv = (null_p1r - null_p0r) * null_woe
        nullmapiv = pd.DataFrame(
            {'bin': 0, 'll': np.nan, 'ul': np.nan, 'p1': null_t1, 'p0': null_t0, 'woe': null_woe, 'iv0': null_iv},
            index=[0])
        # nullmapiv = pd.DataFrame({'bin':[0], 'll':[np.nan], 'ul':[np.nan], 'p1':[null_t1], 'p0':[null_t0], 'woe':[null_woe], 'iv0':[null_iv]})

        return nullmapiv

    def get_firstnull_mapiv(self, tab, t0, t1):
        n_null_t1 = tab.target.sum()
        n_null_t0 = len(tab) - n_null_t1
        n_null_p1r = n_null_t1 / t1 + 1e-6
        n_null_p0r = n_null_t0 / t0 + 1e-6
        n_null_woe = np.log(n_null_p1r / n_null_p0r)
        n_null_iv = (n_null_p1r - n_null_p0r) * n_null_woe
        n_nullmapiv = pd.DataFrame(
            {'bin': 1, 'll': -np.inf, 'ul': np.inf, 'p1': n_null_t1, 'p0': n_null_t0, 'woe': n_null_woe, 'iv0': n_null_iv},
            index=[1])
        # nullmapiv = pd.DataFrame({'bin':[0], 'll':[np.nan], 'ul':[np.nan], 'p1':[null_t1], 'p0':[null_t0], 'woe':[null_woe], 'iv0':[null_iv]})

        return n_nullmapiv

    def split_onevar(self, tabname, varname):

        t1 = tabname.target.sum()
        t0 = len(tabname) - t1

        nulltab = tabname[pd.isnull(tabname[varname])]  # 缺失值单独一箱
        n_nulltab = tabname[pd.isnull(tabname[varname]) == 0]  # 非缺失
        if len(np.unique(n_nulltab[varname])) > 1:
            split_value_1, woe_direct = self.first_split(n_nulltab, varname)
            if woe_direct == -1:
                n_nullmapiv = self.get_firstnull_mapiv(n_nulltab, t0, t1) #非缺失值不能再成功分组
            else:
                tab_l = n_nulltab[n_nulltab[varname] <= split_value_1]
                tab_u = n_nulltab[n_nulltab[varname] > split_value_1]

                split_value = [split_value_1]
                split_value_l, max_iv_l = self.split_var_bin(tab_l, varname, woe_direct)
                split_value_u, max_iv_u = self.split_var_bin(tab_u, varname, woe_direct)

                sp_result = split_value + split_value_l + split_value_u
                gain_iv_resulit = [1] + max_iv_l + max_iv_u

                # 取gain_iv_resulit前max_bin-1个索引

                # print(split_value, split_value_l, split_value_u)
                max_bin = min(self.max_bin - 1, len(gain_iv_resulit))
                sp_result1 = [sp_result[i] for i in np.argpartition(gain_iv_resulit, -max_bin)[-max_bin:]]

                sp_result1.sort()

                n_nullmapiv = self.get_mapiv_result(n_nulltab, varname, sp_result1, t0, t1)  # 非缺失值的分布，计算时传入t0,t1
        else:
            n_nullmapiv = pd.DataFrame()

        if len(nulltab) > 0:
            nullmapiv = self.get_nulldata_mapiv(nulltab, t0, t1)
        else:
            nullmapiv = pd.DataFrame()

        # print(sp_result)
        return pd.concat([nullmapiv, n_nullmapiv], axis=0)

    def split_data(self):
        if self.target != 'target':
            self.indata.rename(columns={self.target: 'target'}, inplace=True)

        order = ['varname', 'bin', 'll', 'ul', 'p0', 'p1', 'total', 'woe', 'iv0', 'iv']  # 指定输出列名
        feature_list = [c for c in self.indata if (self.indata[c].dtype.kind in ('i', 'f')) & ('target' not in c)]

        mapiv = pd.DataFrame()
        for var_i in feature_list:
            print(var_i)
            indata = self.indata[[var_i, 'target']]
            indata[var_i] = indata[var_i].apply(lambda x : round(x, 4))
            mapiv1 = self.split_onevar(indata, var_i)
            mapiv1['varname'] = var_i
            mapiv = pd.concat([mapiv1, mapiv], axis=0)
        mapiv['woe'] = round(mapiv['woe'], 6)
        mapiv['iv0'] = round(mapiv['iv0'], 6)
        m1 = mapiv.groupby(['varname'])[['iv0']].sum()
        m1.rename(columns={'iv0': 'iv'}, inplace=True)
        m1.reset_index(level=0, inplace=True)
        mapiv_t = mapiv.merge(m1, on='varname')

        mapiv_t['total'] = mapiv_t['p0'] + mapiv_t['p1']

        mapiv_t = mapiv_t[order]

        # 仅保留最小分箱数满足要求的分组(缺失那箱可以不用满足该条件)

        min_per = mapiv_t[mapiv_t['bin'] > 0].groupby(['varname'])[['total']].min()
        min_per.reset_index(level=0, inplace=True)
        min_per['flag'] = min_per['total'] >= self.min_num

        mapiv_select = mapiv_t.merge(min_per[['varname', 'flag']], how='left', on='varname')
        mapiv_select1 = mapiv_select[mapiv_select['flag'] == 1]

        return mapiv_select1.drop('flag', axis=1)

    def apply_woetab(self, indata, mapiv):
        outdata = indata.copy()
        var_list = np.unique(mapiv['varname'])
        for vi in var_list:
            if vi in outdata.columns:
                ul_list = mapiv[mapiv['varname'] == vi]['ul'].values
                woe_list = mapiv[mapiv['varname'] == vi]['woe'].values
                kwds = {"sp_list": ul_list, "woe_list": woe_list}
                outdata['W_{}'.format(vi)] = outdata[vi].apply(self.woe_trans, **kwds)
            else:
                continue

        outdata_col = list(outdata)
        outdata_col_woe = [i for i in outdata_col if 'W_' in i]
        # outdata_woe = outdata[['target'] + outdata_col_woe]
        outdata_woe = outdata[outdata_col_woe] #不再提供‘target’
        return outdata_woe

    def cal_cate_woe(self, var):

        data_df = self.indata.copy()
        t1 = data_df[self.target].sum()
        t0 = len(data_df) - t1
        cnt0 = data_df.groupby(var)[[self.target]].count()
        cnt0.rename(columns={'target':'total'}, inplace=True)
        sum0 = data_df.groupby(var)[[self.target]].sum()
        sum0.rename(columns={'target':'bad'}, inplace=True)

        map0 = pd.concat([cnt0, sum0], axis=1)
        map0['good'] = map0['total'] - map0['bad']
        map0['p1_r'] = map0['bad'] / t1 + 1e-6
        map0['p0_r'] = map0['good'] / t0 + 1e-6
        map0['woe'] = np.log(map0['p1_r'] / map0['p0_r'])
        map0.reset_index(inplace=True)

        return map0[[var, 'woe']]

    def split_data_cate(self):

        data_df = self.indata.copy()
        if self.target != 'target':
            data_df.rename(columns={self.target: 'target'}, inplace=True)
            self.target = 'target'

        order = ['varname', 'bin', 'll', 'ul', 'p0', 'p1', 'total', 'woe', 'iv0', 'iv']  # 指定输出列名
        feature_list = [c for c in self.indata if (self.indata[c].dtype.kind not in ('i', 'f'))]
        mapiv = pd.DataFrame()

        all_map_order = ['varname', 'val', 'woe', 'new_woe']
        all_map = pd.DataFrame()
        for var_i in feature_list:
            print(var_i)
            map_i = self.cal_cate_woe(var_i)
            map_dict = dict(map_i.values)
            map_i.rename(columns={var_i:'val'}, inplace=True)
            map_i['varname'] = var_i
            data_df['tempW_{}'.format(var_i)] = data_df[var_i].map(map_dict)

            indata = data_df[['tempW_{}'.format(var_i), 'target']]
            indata['tempW_{}'.format(var_i)] = indata['tempW_{}'.format(var_i)].apply(lambda x : round(x, 4))
            mapiv1 = self.split_onevar(indata, 'tempW_{}'.format(var_i))
            mapiv1['varname'] = var_i
            mapiv = pd.concat([mapiv1, mapiv], axis=0)

            ul_list = mapiv['ul'].values
            woe_list = mapiv['woe'].values
            kwds = {"sp_list": ul_list, "woe_list": woe_list}
            map_i['new_woe'] = map_i['woe'].apply(self.woe_trans, **kwds)
            all_map = all_map.append(map_i)

        mapiv['woe'] = round(mapiv['woe'], 6)
        mapiv['iv0'] = round(mapiv['iv0'], 6)
        m1 = mapiv.groupby(['varname'])[['iv0']].sum()
        m1.rename(columns={'iv0': 'iv'}, inplace=True)
        m1.reset_index(level=0, inplace=True)
        mapiv_t = mapiv.merge(m1, on='varname')

        mapiv_t['total'] = mapiv_t['p0'] + mapiv_t['p1']
        mapiv_t = mapiv_t[order]

        # 仅保留最小分箱数满足要求的分组(缺失那箱可以不用满足该条件)

        min_per = mapiv_t[mapiv_t['bin'] > 0].groupby(['varname'])[['total']].min()
        min_per.reset_index(level=0, inplace=True)
        min_per['flag'] = min_per['total'] >= self.min_num

        mapiv_select = mapiv_t.merge(min_per[['varname', 'flag']], how='left', on='varname')
        mapiv_select1 = mapiv_select[mapiv_select['flag'] == 1]

        return mapiv_select1.drop('flag', axis=1), all_map[all_map_order]

    def apply_woetab_cate(self, indata, all_mapdict):

        outdata = indata.copy()
        var_list = np.unique(all_mapdict['varname'])
        for vi in var_list:
            if vi in outdata.columns:
                map_dict = dict(all_mapdict[all_mapdict['varname'] == vi][['val', 'new_woe']].values)
                outdata['W_{}'.format(vi)] = outdata[vi].map(map_dict)
            else:
                continue

        outdata_col = list(outdata)
        outdata_col_woe = [i for i in outdata_col if 'W_' in i]
        # outdata_woe = outdata[['target'] + outdata_col_woe]
        outdata_woe = outdata[outdata_col_woe] #不再提供‘target’
        return outdata_woe