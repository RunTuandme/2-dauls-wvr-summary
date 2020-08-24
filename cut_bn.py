from wreader import wvrfile
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import pandas as pd
import os
from tqdm import tqdm

def find_first_txt(pathdir: str) -> str:
    for i in os.listdir(pathdir):
        if i[-4:] == '.txt':
            return i
    return None

if __name__ == '__main__':
    pathdir = '../Estimate/prod_vs_cal/'

    # 获取所有已经计算好的csv文件
    allfiles = []
    for i in os.listdir(pathdir):
        if i[-4:] == '.csv':
            allfiles.append(i)

    for i in allfiles:
        # 读取cut_csv文件
        df = pd.read_csv(pathdir + i)
        dif = df['pc_cut'].tolist()
        cut_time = df['time'].tolist()

        # 读取对应日期的wvr文件
        wvrdir = '../RawDatas/WVR_raw_data/20' + i[:6] + '/'
        aimfile = find_first_txt(wvrdir)
        wf = wvrfile(wvrdir + aimfile)
        T = wf.T0()
        RHO = wf.e()
        wvr_time = wf.Time()

        # 建立画布
        fig = plt.figure()

        # 画第一个子图：cut
        ax1 = fig.add_subplot(211)
        ax1.plot(cut_time, dif, label='dif')
        ax1.set_title('Difference between products and marco calculates')
        ax1.set_ylabel('Difference of ZWD (mm)')
        ax1.set_xlabel('time')
        ax1.set_xlim(0, 86400)
        ax1.set_xticks([0, 21600, 43200, 64800, 86400])
        ax1.set_xticklabels(['0:00', '6:00', '12:00', '18:00', '24:00'])
        ax1.xaxis.set_minor_locator(AutoMinorLocator(6))
        ax1.tick_params(
            axis='x',
            which='both',
            bottom=True,
            top=False,
            labelbottom=False,
            direction='in'
            ) 
        ax1.tick_params(
            axis='y',
            which='both',
            direction='in'
            ) 
        ax1.legend()
        ax1.spines['top'].set_linewidth(1.5)
        ax1.spines['bottom'].set_linewidth(1.5)
        ax1.spines['left'].set_linewidth(1.5)
        ax1.spines['right'].set_linewidth(1.5)

        # 画第二个子图：T、e
        ax2 = fig.add_subplot(212)
        ax2_l1, = ax2.plot(wvr_time, [i*100 for i in RHO], label='Relative humidity')
        ax2.set_xlabel('time')
        ax2.set_ylabel('Relative humidity (%)')
        ax2.set_xlim(0,86400)
        ax2.set_xticks([0, 21600, 43200, 64800, 86400])
        ax2.set_xticklabels(['0:00', '6:00', '12:00', '18:00', '24:00'])
        ax2.tick_params(
            axis='x',
            which='both',
            bottom=True,
            top=True,
            labeltop=False,
            direction='in'
            ) 
        ax2.tick_params(
            axis='y',           # changes apply to the x-axis
            which='both',       # both major and minor ticks are affected
            direction='in'
            ) 
        ax2.spines['top'].set_linewidth(1.5)
        ax2.spines['bottom'].set_linewidth(1.5)
        ax2.spines['left'].set_linewidth(1.5)
        ax2.spines['right'].set_linewidth(1.5)

        # 画第二个子图的同x轴双y轴子图
        ax3 = ax2.twinx()
        ax2_l2, = ax3.plot(wvr_time, T,color='#ff7f0e',label='Temperature')
        ax3.set_ylabel('Temperature (K)')
        ax2.legend(handles=[ax2_l1, ax2_l2], labels=['Relative humidity', 'Temperature'], loc='best')

        plt.subplots_adjust(left=0.115,bottom=0.05,top=0.95,right=0.8,hspace=0)

        plt.savefig('../Estimate/prod_vs_cal/putoget/20'+i[:6]+'.png', dpi=500)
        plt.close('all')


""" if __name__ == '__main__':
    pathdir = '../Estimate/prod_vs_cal/'

    # 获取所有已经计算好的txt文件
    allfiles = []
    for i in os.listdir(pathdir):
        if i != '180121_cruz492.txt' and i[-4:] == '.txt':
            allfiles.append(i)

    for i in tqdm(allfiles):
        df = pd.read_csv(pathdir + i, header=None)
        cal_zwd = df[0].tolist()
        wvrdir = '../RawDatas/WVR_raw_data/20' + i[:6] + '/'
        for j in os.listdir(wvrdir):
            if j[-4:] == '.txt':     
                Wf = wvrfile(wvrdir + j)
                wvr_zwd = Wf.ZWD()
                wvr_time = Wf.Time()
                cal_time = wvr_time
                cut = [a-b for a,b in zip(wvr_zwd,cal_zwd)]
                cut_data = pd.core.frame.DataFrame({'time': cal_time, 'pc_cut': cut})
                cut_data.to_csv('../Estimate/prod_vs_cal/' + i[:6] + '_cut.csv')

                if len(cal_zwd) > len(wvr_zwd):
                    cal_zwd = cal_zwd[:len(wvr_zwd)-len(cal_zwd)]
                plt.cla()
                plt.plot(wvr_time, wvr_zwd, label='product')
                plt.plot(cal_time, cal_zwd, label='calculate')
                plt.title('Products compare with marco calculates')
                plt.ylabel('zenith wet delay (mm)')
                plt.savefig('../Estimate/prod_vs_cal/' + i[:6] + '_cmp.png', dpi=500)
                plt.close('all')
                plt.cla()
                plt.plot(cal_time, cut)
                plt.title('Difference between products and marco calculates')
                plt.ylabel('zenith wet delay (mm)')
                plt.savefig('../Estimate/prod_vs_cal/' + i[:6] + '_cut.png', dpi=500)
                plt.close('all') """
