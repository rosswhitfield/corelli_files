import matplotlib.pyplot as plt
import h5py
import numpy as np

cal_org = np.loadtxt('difc_org.txt')

with h5py.File('cal.h5', 'r') as f:
    cal1= f['calibration/difc'].value

with h5py.File('cal2.h5', 'r') as f:
    cal2= f['calibration/difc'].value

with h5py.File('cal3.h5', 'r') as f:
    cal3= f['calibration/difc'].value


plt.plot(cal1/cal_org,label='cal1')
plt.plot(cal2/cal_org,label='cal2')
plt.plot(cal3/cal_org,label='cal3')
plt.legend()
plt.show()
