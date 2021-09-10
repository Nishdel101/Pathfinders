"""
import pandas as pd
from scipy.spatial.transform import Rotation
quat_df = [-0.5, 0.5, 0.5, 0.5]
rot = Rotation.from_quat(quat_df)
rot_euler = rot.as_euler('xyz', degrees=True)
euler_df = pd.DataFrame(data=rot_euler, columns=['x', 'y', 'z'])
print('euler_df')
"""
import numpy as np

def quaternion_to_euler_angle_vectorized1(w, x, y, z):
    ysqr = y * y

    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + ysqr)
    X = np.degrees(np.arctan2(t0, t1))

    t2 = +2.0 * (w * y - z * x)
    t2 = np.where(t2>+1.0,+1.0,t2)
    #t2 = +1.0 if t2 > +1.0 else t2

    t2 = np.where(t2<-1.0, -1.0, t2)
    #t2 = -1.0 if t2 < -1.0 else t2
    Y = np.degrees(np.arcsin(t2))

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (ysqr + z * z)
    Z = np.degrees(np.arctan2(t3, t4))

    return Z

print(quaternion_to_euler_angle_vectorized1( 0.6764436137689968, -0.001171904867342482, 0.0010740847202957095, 0.7364927089741866))
