#!/usr/bin/env python
# coding: utf-8



class Clark: # 일단 CN을 아는 상황에 대한 코드!
    
    ''' time step은 1시간을 몇 개로 쪼갤 것이냐? '''
    
    def __init__(self, Tc, K, area, time_step):
        
        self.Tc = Tc
        self.K = K
        self.area = area
        self.time_step = time_step
        self.length = int(Tc*time_step*100)
        
    def make_Clark(self):
        
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        
        length = self.length
        Tc = self.Tc
        K = self.K
        area = self.area
        time_step = self.time_step
        
        # 단위도 만들기
        Clark = pd.DataFrame()
        Clark['time'] = np.arange(0, length)/time_step # time
        Clark['time_ratio'] = Clark['time']/Tc # time
        
        # 시간 비율에 따른 면적 비율 계산
        def cal_AI(ratio):
            AI = 0 
            if ratio<0.5:
                #count=count+1
                AI=1.414*(ratio**1.5)
            elif ratio>=0.5 and ratio<1.0:
                #count=count+1
                AI=1-1.414*((1-ratio)**1.5)
            elif ratio>=1:
                #count=count+1
                AI=1.000

            return AI
        
        # 계산!
        Clark['AI'] = Clark['time_ratio'].apply(cal_AI)  
        
        # 비율을 면적으로 cumulative area
        Clark['CA'] = Clark['AI']*area # 누가 면적
        
        # 구간별 면적을 구하기 위한 shift
        Clark['CA_shift'] = Clark['CA'].shift(1)
        Clark['CA_shift'] = Clark['CA_shift'].fillna(0)
        
        # 시간당 들어오는 면적 km2
        Clark['SA'] = Clark['CA'] - Clark['CA_shift'] 
        
        # 시간당 들어오는 것을 유량 단위로 변경 km2 10^6이고, h는 3600임, 1m -> 1cm로 변경! /100
        Clark['IH'] = Clark['SA']*1000000/3600/100*time_step 
        
        # 저수지 홍수추적을 위한 계수 산정
        c = 2/(2*(K*time_step)+1)
        
        # 순간단위도 계산
        count_IUH=0
        IUH = np.zeros(length)
        for i in range(1, length):
            count_IUH=count_IUH+1
            IUH[i]=c*(0.5*Clark['IH'][i] + 0.5*Clark['IH'][i-1]) + (1-c)*IUH[i-1]

            if IUH[i]<=0.000001:
                    break
        
        # 순간단위도 입력
        Clark['IUH'] = IUH
        
        # 순간단위도 그림으로 확인
        plt.plot(Clark['time'][:count_IUH], Clark['IUH'][:count_IUH], label = 'IUH')
        
        
        # 단위도 계산을 위한 shift
        Clark['IUH_shift'] = Clark['IUH'].shift(1)
        Clark['IUH_shift'] = Clark['IUH_shift'].fillna(0)
        
        # time-step에 대한 단위도 (ex. 0.01 h 단위라면 0.01 h 단위도)
        Clark['UH'] = (Clark['IUH'] + Clark['IUH_shift'])/2
        
        ## 1 h 단위도로 변경: 쪼갠만큼 다시 합쳐주는 거라고 봐야지~
        sum_UH = Clark['UH']
        for i in range(1, int(time_step/10)): # 100개로 쪼갰으니, 10개로 합쳐야 0.1 h
            sum_UH = sum_UH + Clark['UH'].shift(i).fillna(0) 
        
        # 개수만큼 나누어 주기! 
        Clark['UH_0.1hr'] = sum_UH/(time_step/10)    

        # 1 h 단위도 그림으로 확인
        import matplotlib.pyplot as plt
        print('UH_0.1hr')
        plt.plot(Clark['time'][:count_IUH], Clark['UH_0.1hr'][:count_IUH], label='UH_0.1hr')
        plt.legend()
        plt.xlabel('Time (h)')
        plt.ylabel('Discharge (cms)')
        plt.show()

        # 계산 편하게 1 mm 단위도도 구해주기
        Clark['UH_0.1hr_mm'] = Clark['UH_0.1hr']/10       
       
        # 유량 volume 확인(m3 단위)
        vol_dis = sum(Clark['UH_0.1hr_mm'])/time_step*3600 # m3 단위
        
        # 강우 volume 확인(m3 단위)
        vol_rain = (area*(10**6))*(1*(10**-3)) # 1 mm라고 하였을 때 
        
        print('총 강우(m3):', vol_rain, '총 유량(m3):', vol_dis, '차이:', abs(vol_rain-vol_dis))

        ## 결과 취하기
        self.count_IUH = count_IUH
        self.Clark = Clark    
        
    def Routing(self, rain_array, CN_value):
        
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        
        Clark = self.Clark
        length = self.length
        time_step = self.time_step
        area = self.area
        CN = CN_value
        Tc = self.Tc
        K = self.K
        count_IUH = self.count_IUH

        # table 생성
        rain_table = pd.DataFrame(np.arange(len(rain_array)), columns=['time'])
        rain_table['rain'] = rain_array
        rain_table['cum_rain'] = rain_table['rain'].cumsum()
        
        # 유효우량 구하기
        S = 25400/CN - 254
        initial_loss = 0.2*S
        
        # 유효우량 구하기 위한 모듈
        def cal_eff(cum_rain_element):

            if cum_rain_element >= initial_loss:
                cum_eff = (cum_rain_element - 0.2*S)**2 / (cum_rain_element + 0.8*S)    
            else:
                cum_eff = 0    

            return cum_eff        
        
        # 누가 유효우량 구하기
        rain_table['cum_eff'] = rain_table['cum_rain'].apply(cal_eff)
        
        # 구간별 유효우량 구하기 위한 shift
        rain_table['cum_eff_shift'] = rain_table['cum_eff'].shift(1)
        rain_table['cum_eff_shift'] = rain_table['cum_eff_shift'].fillna(0)
        
        # 구간별 유효우량
        rain_table['eff'] = rain_table['cum_eff'] - rain_table['cum_eff_shift']
               
        ## convolution! 
        discharge_table = pd.DataFrame( np.arange( (len(rain_array)*time_step + count_IUH) ) /time_step, columns=['time'])
        discharge_table['Q'] = 0
        discharge = np.zeros( len(discharge_table) ) #len(discharge_table) )
        for i in range(len(rain_table)):
            for j in range(count_IUH):
                discharge[(i)*time_step+j] += rain_table['eff'][i] * Clark['UH_0.1hr_mm'][j]
        discharge_table['Q'] = discharge

        ## 용량 확인
        # 총 유효강우(m3)
        vol_rain_final = area*(10**6)*(sum(rain_table['eff'])*(10**-3))
        
        # 총 직접유출(m3)
        vol_dis_final = sum(discharge_table['Q'])/time_step*3600

        print('총 유효강우(m3):', vol_rain_final, '총 직접유출(m3):', vol_dis_final, '차이:', abs(vol_rain_final-vol_dis_final))
        
        
        
        # 그림으로 확인
        plt.plot(discharge_table['time'][:count_IUH*len(rain_array)], discharge_table['Q'][:count_IUH*len(rain_array)])
        plt.xlabel('Time (h)')
        plt.ylabel('Discharge (cms)')
        plt.show()
        
        self.rain_table = rain_table
        self.discharge_table = discharge_table




