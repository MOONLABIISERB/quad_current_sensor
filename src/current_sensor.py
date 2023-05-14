#!/usr/bin/env python3
import rospy
from px4_current_sensor.msg import Current
import math
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


if __name__=="__main__":
    i2c = busio.I2C(board.SCL, board.SDA)

    
    ads = ADS.ADS1115(i2c, gain=1)
    
    chan0 = AnalogIn(ads, ADS.P0)
    chan1 = AnalogIn(ads, ADS.P1)
    chan2 = AnalogIn(ads, ADS.P2)
    chan3 = AnalogIn(ads, ADS.P3)

    rospy.init_node('motor_currents', anonymous=True)
    current_topic='/quad/current'
    current_publisher = rospy.Publisher(current_topic, Current, queue_size=10)
    msg = Current()
    rate = rospy.Rate(10)

    print("Publishing")
    while not rospy.is_shutdown():
        msg.stamp = rospy.Time.now()
        msg.m1 = (chan0.voltage-2.37)/0.1
        msg.m2 = (chan1.voltage-2.37)/0.1
        msg.m3 = (chan2.voltage-2.37)/0.1
        msg.m4 = (chan3.voltage-2.37)/0.1
        msg.raw_v_1 = chan0.voltage
        msg.raw_v_2 = chan1.voltage
        msg.raw_v_3 = chan2.voltage
        msg.raw_v_4 = chan3.voltage
        current_publisher.publish(msg)
        rate.sleep()