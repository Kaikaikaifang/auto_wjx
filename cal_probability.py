import numpy as np

def cal_probability(data: list):
    """
    :param data: list
    :return: list
    """
    data = np.array(data)
    data = data / np.sum(data)
    sum = np.sum(data)
    print(sum)
    data =  data.tolist()
    data[-1] += (1 - sum)
    return data


if __name__ == '__main__':
    res = cal_probability([75,91,75,54,0])
    print(res)