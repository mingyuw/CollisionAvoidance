import airsim
import time
import sys
import threading
from getch import pause

def runSingleCar(id: int):
    client = airsim.CarClient()
    client.confirmConnection()

    vehicle_name = f"Car_{id}"
    pose = airsim.Pose(airsim.Vector3r(68, -20, 0),
                       airsim.Quaternionr(0, 0, 0, 0))

    print(f"Creating {vehicle_name}")
    success = client.simAddVehicle(vehicle_name, "Physxcar", pose)

    if not success:
        print(f"Falied to create {vehicle_name}")
        return

    # Sleep for some time to wait for other vehicles to be created
    time.sleep(1)

    # driveCar(vehicle_name, client)
    print(f"Driving {vehicle_name}...")
    client.enableApiControl(True, vehicle_name)

    car_controls = airsim.CarControls()
    time.sleep(2.1)
    # go reverse
    car_controls.throttle = -1
    car_controls.is_manual_gear = True
    car_controls.manual_gear = -1
    car_controls.steering = 1
    client.setCarControls(car_controls, vehicle_name)
    time.sleep(2)
    car_controls.steering = 0
    client.setCarControls(car_controls, vehicle_name)
    car_controls.is_manual_gear = False  # change back gear to auto
    car_controls.manual_gear = 0
    time.sleep(3.59)   # let car drive a bit

    while (True):
        # Read current position
        time.sleep(2)
        pose = client.simGetVehiclePose(vehicle_name)
        print(f"{vehicle_name}: ")
        print(pose.position)

def runMainCar():

    # connect to the main car 
    client = airsim.CarClient()
    client.confirmConnection()
    client.reset()
    print('Connected')
    client.enableApiControl(True)
    car_controls = airsim.CarControls()

    print("Driving main car...")

    car_controls.throttle = 2
    car_controls.steering = 0
    client.setCarControls(car_controls)
  
    while (True):
        # Read current position
        time.sleep(2)
        pose = client.simGetVehiclePose()
        # print("main car: ")
        # print(pose.position)
   

if __name__ == "__main__":

    num_vehicles = 1
    if len(sys.argv) == 2:
        num_vehicles = int(sys.argv[1])

    print(f"Creating {num_vehicles} vehicles")

    threads = []
    
    t = threading.Thread(target=runMainCar, args=())
    threads.append(t)
    t.start() 

    for id in range(num_vehicles, 0, -1):
        t = threading.Thread(target=runSingleCar, args=(id,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
