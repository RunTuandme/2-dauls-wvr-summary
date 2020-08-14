
class wvrfile:
    
    def __init__(self, file_path: str):
        self.fp = file_path
        self.JudgeFile()
        self.datelist = self.date()

    def ReadAndGet(self, mode: str = 'NULL') -> list:
        if mode == 'NULL':
            raise ValueError('Missing mode parameters.')
        elif mode == 'tb1':
            dnum = 7
        elif mode == 'tb2':
            dnum = 8
        elif mode == 'ZWD':
            dnum = 3
        elif mode == 'ZTD':
            dnum = 4
        elif mode == 'T0':
            dnum = 9
        elif mode == 'e':
            dnum = 10
        elif mode == 'P0':
            dnum = 11
        
        temp = []
        with open(self.fp,'r',encoding='gbk') as fopen:
            read = False
            for line in fopen:
                if line in ['\n','\r\n']:
                    pass
                else:
                    Arr = line.strip().split()
                    if len(Arr[0]) > 4:
                        if ':' in Arr[3]:
                            del Arr[:2]
                        if Arr[0][:3] == '201':
                            temp.append(float(Arr[dnum]))
                            read = True
            if not read:
                pass
        return temp

    def Tb1(self) -> list:
        return self.clean(self.ReadAndGet('tb1'))

    def Tb2(self) -> list:
        return self.clean(self.ReadAndGet('tb2'))

    def ZWD(self) -> list:
        return self.clean(self.ReadAndGet('ZWD'))

    def ZTD(self) -> list:
        return self.clean([a*1e3 for a in self.ReadAndGet('ZTD')])

    def T0(self) -> list:
        return self.clean([a+273.15 for a in self.ReadAndGet('T0')])

    def e(self) -> list:
        return self.clean([a/100 for a in self.ReadAndGet('e')])

    def P0(self) -> list:
        return self.clean(self.ReadAndGet('P0'))

    def Time(self) -> list:
        temp = []
        with open(self.fp,'r',encoding='gbk') as fopen:
            read = False
            for line in fopen:
                if line in ['\n','\r\n']:
                    pass
                else:
                    Arr = line.strip().split()
                    if len(Arr[0]) > 4:
                        if ':' in Arr[3]:
                            del Arr[:2]
                        if Arr[0][:3] == '201':
                            temp.append(self.t2s(Arr[1]))
                            read = True
            if not read:
                pass
        return self.clean(temp)

    def date(self) -> list:
        temp = []
        with open(self.fp,'r',encoding='gbk') as fopen:
            read = False
            for line in fopen:
                if line in ['\n','\r\n']:
                    pass
                else:
                    Arr = line.strip().split()
                    if len(Arr[0]) > 4:
                        if ':' in Arr[3]:
                            del Arr[:2]
                        if Arr[0][:3] == '201':
                            temp.append(Arr[0])
                            read = True
            if not read:
                pass
        return temp

    def t2s(self, t: str) -> float:
        h,m,s = t.strip().split(":")
        return float(h) * 3600 + float(m) * 60 + float(s)

    def JudgeFile(self):
        try:
            fopen = open(self.fp,'r',encoding='gbk')
            fopen.close()
        except:
            print('Can\'t find ' + self.fp)

    def clean(self, aim: list) -> list:
        """ To remove the data of next day """ 
        dl = self.datelist
        aimc = aim

        if dl[0] == dl[1] == dl[2]:
            rec = dl[0]

        count = 0
        for i in dl:
            if i != rec:
                count += 1
                
        for i in range(count):
            aimc.pop()
        
        return aimc

