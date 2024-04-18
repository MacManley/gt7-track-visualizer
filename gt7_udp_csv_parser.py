from datetime import datetime as dt
import socket
import struct
from Crypto.Cipher import Salsa20
import csv
import time
import ctypes

# ports for send and receive data
SendPort = 33739
ReceivePort = 33740
print("Enter PS4/PS5 IP Address:")
ip = input()

# Create a UDP socket and bind it
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', ReceivePort))
sock.settimeout(10)
start_time = time.time()

class GT7Packet(ctypes.Structure):
	_fields_ = [
		("magic", ctypes.c_int32),
		("position", ctypes.c_float * 3),
		("worldVelocity", ctypes.c_float * 3),
		("rotation", ctypes.c_float * 3),
		("orientationReltoNorth", ctypes.c_float),
		("angularVelocity", ctypes.c_float * 3),
		("bodyHeight", ctypes.c_float),
		("engineRPM", ctypes.c_float),
		("iv", ctypes.c_ubyte * 4),
		("fuelLevel", ctypes.c_float),
		("fuelCapacity", ctypes.c_float),
		("speed", ctypes.c_float),
		("boost", ctypes.c_float),
		("oilPressure", ctypes.c_float),
		("waterTemp", ctypes.c_float),
		("oilTemp", ctypes.c_float),
		("tyreTemp", ctypes.c_float * 4),
		("packetID", ctypes.c_int32),
		("lapCount", ctypes.c_int16),
		("totalLaps", ctypes.c_int16),
		("bestLaptime", ctypes.c_int32),
		("lastLaptime", ctypes.c_int32),
		("dayProgression", ctypes.c_int32),
		("raceStartPosition", ctypes.c_int16),
		("preraceNumCars", ctypes.c_int16),
		("minAlertRPM", ctypes.c_int16),
		("maxAlertRPM", ctypes.c_int16),
		("calcMaxSpeed", ctypes.c_int16),
		("flags", ctypes.c_int16),
		("gears", ctypes.c_ubyte),
		("throttle", ctypes.c_ubyte),
		("brake", ctypes.c_ubyte),
		("paddingByte", ctypes.c_ubyte),
		("roadPlane", ctypes.c_float * 3),
		("roadPlaneDist", ctypes.c_float),
		("wheelRPS", ctypes.c_float * 4),
		("tyreRadius", ctypes.c_float * 4),
		("suspHeight", ctypes.c_float * 4),
		("unknownFloat", ctypes.c_float * 8),
		("clutch", ctypes.c_float),
		("clutchEngagement", ctypes.c_float),
		("RPMFromClutchToGearbox", ctypes.c_float),
		("transMaxSpeed", ctypes.c_float),
		("gearRatios", ctypes.c_float * 8),
		("carCode", ctypes.c_int32),
	]

# data stream decoding
def salsa20_decrypt(dat):
	KEY = b'Simulator Interface Packet GT7 ver 0.0'
	# Seed IV is always located here
	oiv = dat[0x40:0x44]
	iv1 = int.from_bytes(oiv, byteorder='little')
	# Notice DEADBEAF, not DEADBEEF
	iv2 = iv1 ^ 0xDEADBEAF
	IV = bytearray()
	IV.extend(iv2.to_bytes(4, 'little'))
	IV.extend(iv1.to_bytes(4, 'little'))
	cipher = Salsa20.new(KEY[0:32], bytes(IV))
	ddata = cipher.decrypt(dat);
	magic = int.from_bytes(ddata[0:4], byteorder='little')
	if magic != 0x47375330:
		return bytearray(b'')
	return ddata

# send heartbeat
def send_hb(s):
	send_data = 'A'
	s.sendto(send_data.encode('utf-8'), (ip, SendPort))
	#print('send heartbeat')

# generic print function

def secondsToLaptime(seconds):
	remaining = seconds
	minutes = seconds // 60
	remaining = seconds % 60
	return '{:01.0f}:{:06.3f}'.format(minutes, remaining)

def get_elapsed_time(start_time):
	return time.time() - start_time


# start by sending heartbeat
send_hb(sock)

filename = 'data.csv'
csv_file = open(filename, mode='a', newline='')
csv_writer = csv.writer(csv_file)

# Write header row
headers = ['timeElapsed', 'dayProgression', 'isPaused', 'onTrack', 'carID', 'currentGear', 'suggestedGear', 'throttle', 'brake', 'clutch', 'clutchEngagement', 'engineRPM', 'speedKMH', 'speedMPH', 'tyreTempFL', 'tyreTempFR', 'tyreTempRL', 'tyreTempRR', 'posX', 'posY', 'posZ', 'rotX', 'rotY', 'rotZ', 'worldVelocityX', 'worldVelocityY', 'worldVelocityZ', 'angularVelocityX', 'angularVelocityY', 'angularVelocityZ', 'roadPlaneX', 'roadPlaneY', 'roadPlaneZ', 'roadplaneDist', 'orientationRelativeToNorth', 'bestLap', 'totalLaps', 'lastLaptime', 'ongoingLap']

csv_writer.writerow(headers)
time.sleep(1)
print("Logging Started")

prevlap = -1
pktid = 0
hbInterval = 0
while True:
	try:
		data, address = sock.recvfrom(4096)
		hbInterval = hbInterval + 1
		ddata = salsa20_decrypt(data)
		if len(ddata) > 0 and struct.unpack('i', ddata[0x70:0x70+4])[0] > pktid:
			gt7_packet = GT7Packet.from_buffer_copy(ddata)

			if gt7_packet.lapCount > 0:
				dt_current = dt.now()
				if gt7_packet.lapCount != prevlap:
					prevlap = gt7_packet.lapCount
					dt_start = dt_current
				ongoingLap = dt_current - dt_start

			curGear = gt7_packet.gears & 0b00001111
			suggestedGear = gt7_packet.gears >> 4
			print(curGear)

			noActiveFlags = 0 if gt7_packet.flags != 0 else 1
			onTrack = 1 if gt7_packet.flags & 1 << 0 else 0
			paused = 1 if gt7_packet.flags & 1 << 1 else 0
			loading = 1 if gt7_packet.flags & 1 << 2 else 0
			inGear = 1 if gt7_packet.flags & 1 << 3 else 0
			hasTurbo = 1 if gt7_packet.flags & 1 << 4 else 0
			revLimAlert = 1 if gt7_packet.flags & 1 << 5 else 0
			handbrakeActive = 1 if gt7_packet.flags & 1 << 6 else 0
			lightsActive = 1 if gt7_packet.flags & 1 << 7 else 0
			highBeamsActive = 1 if gt7_packet.flags & 1 << 8 else 0
			lowBeamsActive = 1 if gt7_packet.flags & 1 << 9 else 0
			asmActive = 1 if gt7_packet.flags & 1 << 10 else 0
			tcsActive = 1 if gt7_packet.flags & 1 << 11 else 0

			speedKMH = gt7_packet.speed * 3.6
			speedMPH = gt7_packet.speed * 2.237

			tyreSpeedFL = abs(3.6 * gt7_packet.tyreRadius[0] * gt7_packet.wheelRPS[0])
			tyreSpeedFR = abs(3.6 * gt7_packet.tyreRadius[1] * gt7_packet.wheelRPS[1])
			tyreSpeedRL = abs(3.6 * gt7_packet.tyreRadius[2] * gt7_packet.wheelRPS[2])
			tyreSpeedRR = abs(3.6 * gt7_packet.tyreRadius[3] * gt7_packet.wheelRPS[3])

			if gt7_packet.speed > 0.0:
				tyreSlipRatioFL = tyreSpeedFL / speedKMH
				tyreSlipRatioFR = tyreSpeedFR / speedKMH
				tyreSlipRatioRL = tyreSpeedRL / speedKMH
				tyreSlipRatioRR = tyreSpeedRR / speedKMH
			else:
				tyreSlipRatioFL = 0.0
				tyreSlipRatioFR = 0.0
				tyreSlipRatioRL = 0.0
				tyreSlipRatioRR = 0.0

			# print(gt7_packet.tyreTemp[3])

			elapsed_time = get_elapsed_time(start_time)
			
			# data_row = {
            #     'timeElapsed': elapsed_time,
			# 	'isPaused': paused,
			# 	'onTrack': onTrack,
			# 	'carID': gt7_packet.carCode,
            #     'throttle': gt7_packet.throttle,
            #     'brake': gt7_packet.brake,
			# 	'clutch': gt7_packet.clutch,
			# 	'engineRPM': gt7_packet.engineRPM,
			# 	'speedKMH': gt7_packet.speed,
			# 	'bestLap': gt7_packet.bestLaptime,
			# 	'totalLaps': gt7_packet.totalLaps
            # }

			data_row = [
                elapsed_time,
				gt7_packet.dayProgression / 1000,
				paused,
				onTrack,
				gt7_packet.carCode,
				curGear,
				suggestedGear,
                gt7_packet.throttle / 2.55,
                gt7_packet.brake / 2.55,
				gt7_packet.clutch,
				gt7_packet.clutchEngagement,
				gt7_packet.engineRPM,
				speedKMH,
				speedMPH,
				gt7_packet.tyreTemp[0],
				gt7_packet.tyreTemp[1],
				gt7_packet.tyreTemp[2],
				gt7_packet.tyreTemp[3],
				gt7_packet.position[0],
				gt7_packet.position[1],
				gt7_packet.position[2],
				gt7_packet.rotation[0],
				gt7_packet.rotation[1],
				gt7_packet.rotation[2],
				gt7_packet.worldVelocity[0],
				gt7_packet.worldVelocity[1],
				gt7_packet.worldVelocity[2],
				gt7_packet.angularVelocity[0],
				gt7_packet.angularVelocity[1],
				gt7_packet.angularVelocity[2],
				gt7_packet.roadPlane[0],
				gt7_packet.roadPlane[1],
				gt7_packet.roadPlane[2],
				gt7_packet.roadPlaneDist,
				gt7_packet.orientationReltoNorth,
				gt7_packet.bestLaptime,
				gt7_packet.totalLaps,
				gt7_packet.lastLaptime,
				ongoingLap
			]
            # Write data to CSV
			csv_writer.writerow(data_row)


			# Writing data to CSV

		if hbInterval > 100:
			send_hb(sock)
			hbInterval = 0
	except Exception as e:
		send_hb(sock)
		hbInterval = 0
		pass