# 计算标准图幅号
# 1.通过输入图幅号，获取四角范围
# 2.通过输入经纬度，将各比例尺下图幅号输出
#
#                   by David.Ocean  2019.01.15
#                   Email:david_ocean@163.com
#


# 字典中包含比例尺和对应的纬度和经度间隔
lat_lon_gap = {
    "A": [4, 6],
    "B": [2, 3],
    "C": [1, 3 / 2],
    "D": [1 / 3, 1 / 2],
    "E": [1 / 6, 1 / 4],
    "F": [1 / 12, 1 / 8],
    "G": [1 / 24, 1 / 16],
    "H": [1 / 48, 1 / 32],
    "I": [1 / 144, 1 / 96],
    "J": [1 / 288, 1 / 192],
    "K": [1 / 576, 1 / 384]
}


def main():
    # jingdu = 114.5625
    # weidu = 39.375

    get_jwd("J50B001001")
    get_jwd("J50D002002")


# 输入经纬度获取图幅号
def get_tfh(lon, lat):
    if is_number(lat):
        lon = float(lon)
    if is_number(lon):
        lat = float(lat)

    if not is_lon_lat(lon, lat):
        # print("back", lon, type(lon), lat, type(lat))
        return
    baiwan_tf = get_tfh_100w(lon, lat)
    tfh_dic = {}

    for k, v in lat_lon_gap.items():
        scale = k
        lat_temp = int(4 / v[0]) - int((lat % 4) / v[0])
        lon_temp = int((lon % 6) / v[1]) + 1
        if scale == "A":
            lat_num = ""
            lon_num = ""
            scale = ""#转为百万分幅考虑
        elif scale == "J" or scale == "K":  # 当为J或K的时候，则填充为4位
            lat_num = str(lat_temp).rjust(4, "0")
            lon_num = str(lon_temp).rjust(4, "0")
        else:
            lat_num = str(lat_temp).rjust(3, "0")
            lon_num = str(lon_temp).rjust(3, "0")
        tfh_temp = baiwan_tf + scale + lat_num + lon_num
        tfh_dic[k] = tfh_temp
    return tfh_dic
    # print(out_put)


# 计算百万分幅
def get_tfh_100w(lon, lat):
    lat_temp = int(lat / 4) + 1
    lon_temp = int(lon / 6) + 31

    lat_num = chr(lat_temp + 64)
    lon_num = str(lon_temp)

    tf_temp = lat_num + lon_num  # 合在一起成为百万分幅号

    return tf_temp


# 通过图幅号获取经纬度
def get_jwd(tfh):
    tfh = tfh.upper()
    if not is_tfh(tfh):
        return

    a = ord(tfh[0]) - 64
    b = int(tfh[1:3])
    # 对百万分幅图幅号计算
    if len(tfh) == 3:
        x_min = (b - 31) * 6
        x_min_DD = D2Dms(x_min)
        y_min = (a - 1) * 4
        y_min_DD = D2Dms(y_min)
        # 右上角的点坐标
        x_max = x_min + 6
        x_max_DD = D2Dms(x_max)
        y_max = y_min + 4
        y_max_DD = D2Dms(y_max)
        # print(x,y)
        dic_jwd = {"lon_min": x_min, "lat_min": y_min,
                   "lon_max": x_max, "lat_max": y_max,
                   "lon_min_DD": x_min_DD, "lat_min_DD": y_min_DD,
                   "lon_max_DD": x_max_DD, "lat_max_DD": y_max_DD}
        return dic_jwd

    c = tfh[3]
    if c == "K" or c == "J":
        d = int(tfh[4:8])
        e = int(tfh[8:12])
    else:
        d = int(tfh[4:7])
        e = int(tfh[7:10])

    # 左下角的点坐标（最小经度和最大纬度）
    x_min = (b - 31) * 6 + (e - 1) * lat_lon_gap[c][1]
    x_min_DD = D2Dms(x_min)
    y_min = (a - 1) * 4 + ((4 / lat_lon_gap[c][0]) - d) * lat_lon_gap[c][0]
    y_min_DD = D2Dms(y_min)
    # 右上角的点坐标
    x_max = x_min + lat_lon_gap[c][1]
    x_max_DD = D2Dms(x_max)
    y_max = y_min + lat_lon_gap[c][0]
    y_max_DD = D2Dms(y_max)
    # print(x,y)
    dic_jwd = {"lon_min": x_min, "lat_min": y_min,
               "lon_max": x_max, "lat_max": y_max,
               "lon_min_DD": x_min_DD, "lat_min_DD": y_min_DD,
               "lon_max_DD": x_max_DD, "lat_max_DD": y_max_DD}
    return dic_jwd


# 十进制与经纬度转换
def D2Dms(data):
    if not is_number(data):
        return
    else:
        data = float(data)
        d = int(data)
        m = int((data - d) * 60)
        s = int(((data - d) * 60 - m) * 60)
        return "%s°%s′%s″" % (str(d), str(m), str(s))


# 度分秒转化为十进制
def DD_Decimal(d, f, m):
    if not is_number(d):
        return
    elif not is_number(f):
        return
    elif not is_number(m):
        return
    elif float(d) < 0 or float(d) > 360:
        return
    elif float(f) < 0 or float(f) > 60:
        return
    elif float(m) < 0 or float(m) > 60:
        return
    else:
        result = int(d) + float(f) / 60 + float(m) / 360
        return result


# 判断是否为图幅号
def is_tfh(tfh):
    # "J50B001001"
    # 判断长度为3的图幅号，
    if len(tfh) == 3:
        if 86 >= ord(tfh[0]) >= 65:
            if is_number(tfh[1:3]):
                return True
    # 当不为百万分幅时，则长度需要为10
    if len(tfh) != 10:
        return False
    if tfh[3] not in ['B', 'C', 'D', 'E', 'F', 'G', 'H']:
        return False
    elif not ord(tfh[0]) < 86 and ord(tfh[0]) > 65:
        return False
    elif not is_number(tfh[1:3]) and is_number(tfh[4:7]) and is_number(tfh[7:10]):
        return False
    else:
        return True


# 判断经纬度是否在中国范围内
def is_lon_lat(lon, lat):
    if not (70 <= lon <= 150):
        return False
    elif not (0 <= lat <= 56):
        return False
    else:
        return True


# 判断是否为数值
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    main()
