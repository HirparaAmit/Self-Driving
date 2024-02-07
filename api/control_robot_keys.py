import sim
from time import sleep as delay
import numpy as np
import cv2, sys

print("Program Started")
sim.simxFinish(-1)
clientID = sim.simxStart('127.0.0.1', 19999, True, True, 5000, 5)

lspeed = 0
rspeed = 0

if(clientID != -1):
    print('Connected to remote API server')
else:
    sys.exit('Failed connecting to remote API server')

delay(1)

error_code, left_motor_handle = sim.simxGetObjectHandle(clientID, '/PioneerP3DX/leftMotor', sim.simx_opmode_oneshot_wait)
error_code, right_motor_handle = sim.simxGetObjectHandle(clientID, '/PioneerP3DX/rightMotor', sim.simx_opmode_oneshot_wait)

error_code, camera_handle = sim.simxGetObjectHandle(clientID, '/PioneerP3DX/cam1', sim.simx_opmode_oneshot_wait)
delay(1)

return_code, resolution, image = sim.simxGetVisionSensorImage(clientID, camera_handle, 0, sim.simx_opmode_streaming)
delay(1)

try:
    while(1):
        return_code, resolution, image = sim.simxGetVisionSensorImage(clientID, camera_handle, 0, sim.simx_opmode_buffer)
        im = np.array(image, dtype=np.uint8)
        im.resize([resolution[0], resolution[1], 3])

        im = cv2.flip(im, 0)
        im = cv2.resize(im, (512, 512))
        im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)

        error_code = sim.simxSetJointTargetVelocity(clientID, left_motor_handle, lspeed, sim.simx_opmode_streaming)
        error_code = sim.simxSetJointTargetVelocity(clientID, right_motor_handle, rspeed, sim.simx_opmode_streaming)

        cv2.imshow("data", im)
        com = cv2.waitKey(1)
        if (com == ord('q')):
            break
        elif (com == ord('w')):
            lspeed = 5
            rspeed = 5
        elif (com == ord('a')):
            lspeed = -2.5
            rspeed = 5
        elif (com == ord('d')):
            lspeed = 5
            rspeed = -2.5
        elif (com == ord('s')):
            lspeed = -5
            rspeed = -5
        else:
            lspeed = 0
            rspeed = 0
        com = 'o'

    cv2.destroyAllWindows()
except:
    cv2.destroyAllWindows()