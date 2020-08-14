from wreader import wvrfile
import matplotlib.pyplot as plt

if __name__ == '__main__':
    Wf = wvrfile('../RawDatas/WVR_raw_data/20180217/SH_FSJ_D1802170004.txt')
    wvr_zwd = Wf.ZWD()
    wvr_time = Wf.Time() 

    cal_zwd = []
    # -- 读取计算文件 -- #
    with open('prod_vs_cal/180217_cruz.txt','r') as f_cal:
        for line in f_cal:
            Arr = line.strip().split()
            cal_zwd.append(float(Arr[0]))

    cut = [a-b for a,b in zip(wvr_zwd,cal_zwd)]

    plt.plot(wvr_time, cut)
    plt.show()