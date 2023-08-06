

from ChosenAPI.function.common import CommonFunction


class BondModels(object):
    def __init__(self):
        pass

    @staticmethod
    def macaulay_duration(c, m, y, t0, t1, method):
        """
        :param c:
        :param m:
        :param y:
        :param t0:
        :param t1:
        :param method:
        :return: ,
        """
        obj = {'info': 'MacaulayDuration', 'c': c, 'm': m, 'y': y, 't0': t0, 't1': t1, "method": method}
        func = "bond_macaulay_duration"
        data = CommonFunction.send_data_by_post(obj, func)
        return data

    @staticmethod
    def macaulay_duration_value_change(c, m, y, y_change, t0, t1, l, method):
        """
        :param c:
        :param m:
        :param y:
        :param y_change:
        :param t0:
        :param t1:
        :param l:
        :param method:
        :return:
        """
        obj = {'info': 'MacaulayDurationValueChange', 'c': c, 'm': m, 'y': y, 'y_change': y_change, 't0': t0, 't1': t1, 'l':l, "method":method}
        func = "bond_macaulay_duration"
        data = CommonFunction.send_data_by_post(obj, func)
        return data

    @staticmethod
    def convexity(c, m, y, t0, t1):
        """
        :param c:
        :param m:
        :param y:
        :param t0:
        :param t1:
        :return:
        """
        obj = {'info': 'MacaulayDurationValueChange', 'c': c, 'm': m, 'y': y, 't0': t0, 't1': t1}
        func = "bond_convexity"
        data = CommonFunction.send_data_by_post(obj, func)
        return data

    @staticmethod
    def zero_coupon_bond_value(c, m, y, t0, t1, par):
        """
        :param c:
        :param m:
        :param y:
        :param t0:
        :param t1:
        :param par:
        :return:
        """
        obj = { 'c': c, 'm': m, 'y': y, 't0': t0, 't1': t1, "par": par}
        func = "zero_coupon_bond_value"
        data = CommonFunction.send_data_by_post(obj, func)
        return data

