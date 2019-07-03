import numpy as np


class Smoothing(object):

    def moving_means(self, dseries, days):
        append_nan = np.array([np.nan] * (days-1))
        return np.append(append_nan, np.convolve(dseries, np.ones(days), "valid") / days)

    def moving_medians(self, dseries, days):
        append_nan = np.array([np.nan] * (days-1))
        result = []
        for _ in range(len(dseries) - days + 1):
            result.append(round(np.median(dseries[-days:]), 2))
            dseries = np.delete(dseries, -1)
        return np.append(append_nan, np.array(result[::-1]))

    def moving_max(self, dseries, days):
        append_nan = np.array([np.nan] * (days-1))
        result = []
        for _ in range(len(dseries) - days + 1):
            result.append(round(np.max(dseries[-days:]), 2))
            dseries = np.delete(dseries, -1)
        return np.append(append_nan, np.array(result[::-1]))

    def moving_min(self, dseries, days):
        append_nan = np.array([np.nan] * (days-1))
        result = []
        for _ in range(len(dseries) - days + 1):
            result.append(round(np.min(dseries[-days:]), 2))
            dseries = np.delete(dseries, -1)
        return np.append(append_nan, np.array(result[::-1]))

    def moving_exp_means(self, dseries, days):
        result = []
        nbr_nan = np.count_nonzero(np.isnan(dseries))
        result.extend([np.nan] * (nbr_nan + days - 1))

        alpha = 2 / (days + 1)
        result.extend(dseries[nbr_nan: nbr_nan + 1])
        dseries = np.delete(dseries, range(nbr_nan + days))
        for _ in range(len(dseries)):
            result.append(((alpha * dseries[0]) + ((1 - alpha) * result[-1])))
            dseries = np.delete(dseries, 0)
        return np.array(result)

class TecAnalysis(Smoothing):

    def cal_kd_value(self, dseries_rsv):
        '''
        RSV = (今日收盤價 - 最近N日的最低價) / (最近N日的最高價 - 最近N日的最低價) * 100
        當日 K 值 = 前日 K 值 * (2/3) + 當日 RSV * (1/3)
        當日 D 值 = 前日 D 值 * (2/3) + 當日 K 值 * (1/3)
        '''
        dseries_na = dseries_rsv[np.isnan(dseries_rsv)]
        dseries_rsv = dseries_rsv[~np.isnan(dseries_rsv)]

        result = {'K_val':[50], 'D_val':[50]}
        K_val_list = [50]
        D_val_list = [50]
        for i in range(1, len(dseries_rsv)):
            K_value = (1/3) * dseries_rsv[i] + (2/3) * K_val_list[i-1]
            K_val_list.append(K_value)
            D_value = (2/3) * D_val_list[i-1] + (1/3) * K_val_list[i]
            D_val_list.append(D_value)

        return np.append(dseries_na, np.array(K_val_list)), np.append(dseries_na, np.array(D_val_list))

    def cal_macd(self, dseries):
        '''
        '''
        ema12 = Smoothing.moving_exp_means(self, dseries, 12)
        ema26 = Smoothing.moving_exp_means(self, dseries, 26)
        dif = ema12 - ema26
        macd = Smoothing.moving_exp_means(self, dif, 9)
        osc = dif - macd
        return macd, osc