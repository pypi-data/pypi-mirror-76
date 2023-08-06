import math

math.sqrt
def format_CablePeaksHCF():
    """
    | am_dst: 65535,|am_src: 11601,|am_len: 38,|am_grp: 0,|am_type: 213,|source: 17810,|re_trans: 0,|sid: 7,|seqno: 10923,|ttl: 59,|st_csdata: 38,|unix_time: 1593689711,|freq: 49.51,|average_power: 0.065806,|axis: z,|range: -2g to 2g,|values: 13,8,112,290,189,345,2788,82,132,30,|base_freq: 5.33,|error_t: 0,|extent: 0.492947,|node_id: 17810,|odr: 50Hz,|packet_version: 2,|peaks: 359,451,537,622,720,801,894,985,1084,1168,|peaks_num: 10,|quality: 69,|version: 0,|
    """
    data = {
        "values":[13,8,112,290,189,345,2788,82,132,30],
        "peaks_num":10,
        "quality":69,
        "peaks": [359,451,537,622,720,801,894,985,1084,1168],
        "frequency": 49.51
    }

    sensor = {
        "W": 15.849,
        "L": 101.524,
        "Ei":0.111099,
        "f1_avg":1.05923,
        "order":10,
        "n":1
    }

    calc_argu = sensor

    def func(m, l, fn, n, Ei):
        return (4*m*l*l*fn*fn/(n*n)) - (n*n*Ei*math.pi*math.pi/(l*l))

    try:
        m = float(calc_argu.get('W') or sensor.get('W'))
        l = float(calc_argu.get('L') or sensor.get('L'))
        Ei = float(calc_argu.get('Ei') or sensor.get('Ei') or 0)
        fn = float(calc_argu.get('f1_avg') or sensor.get('f1_avg'))
        order = int(float(calc_argu.get('order') or sensor.get('order') or 1))
        n = int(float(sensor.get('n') or 1))

        if not isinstance(data.get('peaks'), list): data['peaks'] = [data['peaks']]
        if not isinstance(data.get('values'), list): data['values'] = [data['values']]

        data['peaks'] = data.get('peaks')[0: data.get('peaks_num')]
        peaks = data.get('peaks')
        peaks = [p/4096.0 * data.get('frequency') for p in peaks]
        data['values'] = data.get('values')[0: data.get('peaks_num')]

        index = data['values'].index(max(data['values']))
        if peaks[index] < fn/2:
            data['val'] = -1
            return

        P = 4*m*l*l*l*l/math.pi/math.pi
        fr=[math.sqrt(fn*fn/n/n-(n*n-k*k)*Ei/P)*k for k in range(1, order+1)]

        hs = []
        for i in range(0, len(fr)):
            x = [abs(item - fr[i]) for item in peaks]
            fi = peaks[x.index(min(x))]
            hs.append([(abs(fi -fr[i])/fr[i]), fi, i])

        _x = [i[0] for i in hs]
        hs = hs[_x.index(min(_x))]

        data['val'] = func(m, l, hs[1], hs[2] + 1, Ei) / 1000
        data['base_freq'] = hs[1]/(hs[2] + 1)
        print(data['val'], data['base_freq'])
    except Exception as e:
        print(e)
        data['val'] = 0


if __name__ == "__main__":
    format_CablePeaksHCF()