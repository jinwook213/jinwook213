#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy


# # CN과 관련된 계산을 수행하는 프로그램

# In[102]:




class CN_cal: 
    
    ''' 
    CN과 관련된 계산을 수행하는 프로그램
    '''
    def __init__(self):
        '''
        기본 매개변수 setting
        '''
      
        
#     def CN_change(self, condition):
        
        
    def p5_to_condition(self, p5, growing = 1):
        
        '''
        선행 5일 강수량을 이용하여 AMC 조건을 판단해주는 함수
        - p5: 선행 5일 강수량
        - growing: 성수기/비성수기(1/0) -> 기본값: 성수기
        '''
        if growing == 1:

            if p5>=53.34:
                self.condition = 3
            elif 53.34>p5>=35.56:
                self.condition = 2
            elif 35.56>p5:
                self.condition = 1
        
        elif growing == 0:
            
            if p5>=27.94:
                self.condition = 3
            elif 27.94>p5>=12.70:
                self.condition = 2
            elif 27.94>p5:
                self.condition = 1
    
    def CN_change(self, CN):
        '''
        1) p5_to_codition(p5) 모듈을 이용하여 -> condition 추출
        2) AMC 조건을 이용하여 CN 값을 변환해주는 함수(Hwakins et al., 1985)
        
        self.CN_re = 변환된 CN
        '''
        condition_after = self.condition
        self.CN = CN
        
        if condition_after == 1:
            self.CN_re = CN/(2.3-0.013*CN)
        elif condition_after == 3:       
            self.CN_re = CN/(0.43+0.0057*CN)
        else:
            self.CN_re = CN        

    def rain_to_eff_with_CN(self, rain, CN, initial_loss_rate = 0.2):
        '''
        총 강우를 유효우량으로 변환하는 프로그램     
        
        <입력>
        self.CN_re = AMC 조건에 맞는 CN
        rain = 총 강우량
        
        <출력>
        self.eff_rain = 유효우량
        self.C = 유출계수(유출률)
        '''
        
        self.CN = CN
        CN = self.CN
        total_rain = rain
        
        S = 25400/CN - 254
        total_initial_loss = initial_loss_rate*S
        C = ((total_rain-total_initial_loss)**2)/(total_rain*(total_rain+S-total_initial_loss))

        if total_rain < total_initial_loss:
            C = 0

        eff_rain = total_rain*C
        
        self.eff_rain = eff_rain
        self.C = C
        print('eff:', eff_rain)
        print('C:', C)

    def rain_to_eff(self, rain, initial_loss_rate = 0.2):
        '''
        총 강우를 유효우량으로 변환하는 프로그램     
        
        <입력>
        self.CN_re = AMC 조건에 맞는 CN
        rain = 총 강우량
        
        <출력>
        self.eff_rain = 유효우량
        self.C = 유출계수(유출률)
        '''
        
        CN = self.CN_re
        total_rain = rain
        
        S = 25400/CN - 254
        total_initial_loss = initial_loss_rate*S
        C = ((total_rain-total_initial_loss)**2)/(total_rain*(total_rain+S-total_initial_loss))

        if total_rain < total_initial_loss:
            C = 0

        eff_rain = total_rain*C
        
        self.eff_rain = eff_rain
        self.C = C
        print('eff:', eff_rain)
        print('C:', C)

    # def rain_array_to_eff_array(self, rain_array):
    #     '''
    #     총 강우 array를 유효우량으로 변환하는 프로그램     
        
    #     <입력>
    #     self.CN_re = AMC 조건에 맞는 CN
    #     rain = 총 강우 array
        
    #     <출력>
    #     self.eff_rain = 유효우량 array
    #     self.C = 유출계수(유출률)
    #     '''
        
    #     CN = self.CN_re
    #     total_rain = sum(rain_array)
        
    #     S = 25400/CN - 254
    #     C = 1/(1-254/total_rain + 25400/(total_rain*CN))
        
    #     # if total_rain < 0.2*S:
    #     #     C = 0
            
    #     eff_rain_array = rain_array*C
        
    #     self.rain_array = rain_array
    #     self.eff_rain_array = eff_rain_array
    #     self.C = C
    #     print('eff:', eff_rain_array)
    #     print('C:', C)

    def rain_array_to_eff_array(self, rain_array, initial_loss_rate = 0.2):
        '''
        총 강우 array를 유효우량으로 변환하는 프로그램     
        
        <입력>
        self.CN_re = AMC 조건에 맞는 CN
        rain = 총 강우 array
        
        <출력>
        self.eff_rain = 유효우량 array
        self.C = 유출계수(유출률)
        '''
        
        CN = self.CN_re
        total_rain = sum(rain_array)
        
        S = 25400/CN - 254
        total_initial_loss = initial_loss_rate*S
        C = ((total_rain-total_initial_loss)**2)/(total_rain*(total_rain+S-total_initial_loss))

        if total_rain < total_initial_loss:
            C = 0
            
        eff_rain_array = rain_array*C
        
        self.rain_array = rain_array
        self.eff_rain_array = eff_rain_array
        self.C = C
        print('eff:', eff_rain_array)
        print('C:', C)

    def rain_array_to_eff_array_CN(self, rain_array, initial_loss_rate = 0.2):
        
        import numpy as np
        '''
        총 강우 array를 유효우량으로 변환하는 프로그램  // NRCS-CN 방법 사용   
        
        <입력>
        self.CN_re = AMC 조건에 맞는 CN
        rain = 총 강우 array
        
        <출력>
        self.eff_rain = 유효우량 array
        self.C = 유출계수(유출률)
        '''
        
        CN = self.CN_re
        total_rain = sum(rain_array)
        
        S = 25400/CN - 254
        total_initial_loss = initial_loss_rate*S
        
        end = len(rain_array)
        cum_rain = np.zeros(end) # 누가 강우량(mm)
        cum_eff = np.zeros(end) # 누가 유효우량(mm)
        eff = np.zeros(end) # 누가 침투량(mm)
        # 누적 강우 계산
        for i in range(1, end):
            cum_rain[i] = cum_rain[i-1] + rain_array[i]
        
        # 누적 유효우량 계산
        for i in range(1, end):
            if cum_rain[i] >= total_initial_loss:
                cum_eff[i] = (cum_rain[i] - 0.2*S)**2 / (cum_rain[i] + 0.8*S)    
            else:
                cum_eff[i] = 0
        # 시간별 유효우량 계산
        for i in range(1, end):
            eff[i] = cum_eff[i] - cum_eff[i-1]    
       
        eff_rain_array = eff
        eff_rain_array = {'rain': eff_rain_array}
        import pandas as pd
        eff_rain_array = pd.DataFrame(eff_rain_array)
        eff_rain_array = eff_rain_array.rain
        self.rain_array = rain_array
        self.eff_rain_array = eff_rain_array
        # self.C = sum(eff_rain_array)/sum(cum_rain)
        print('eff:', eff_rain_array)
        # print('C:', C)






# %%
