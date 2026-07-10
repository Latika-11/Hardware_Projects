 Smart Step – Footstep Energy Harvesting System using STM32

Overview
Smart Step is an energy harvesting system that converts mechanical energy generated from human footsteps into electrical energy. A rack-and-gear mechanism rotates two DC geared motors, which act as generators. The generated electrical energy is filtered, stored, regulated, and monitored using an STM32 NUCLEO-C051C8 development board.
The project demonstrates renewable energy harvesting for low-power electronic applications such as LED lighting, IoT sensor nodes, and smart public infrastructure.

Features

- Converts footstep energy into electrical energy
- Dual DC motor generator configuration
- Rack-and-two-gear mechanical transmission
- Energy storage using Super Capacitor
- Voltage regulation using 7805 regulator
- Real-time voltage monitoring using STM32 ADC
- LED indication for generated power
- Expandable for IoT applications

Working Principle

1. A person steps on the Smart Step tile.
2. The tile moves downward.
3. The downward movement drives a rack.
4. The rack rotates two spur gears.
5. Each gear rotates a 12V DC geared motor.
6. The motors operate as DC generators.
7. Generated voltage is filtered using a 4700µF capacitor.
8. Energy is temporarily stored in a 5.5V supercapacitor.
9. The 7805 regulator provides a stable 5V supply for the STM32 board.
10. STM32 measures the generated voltage through its ADC.
11. The LED turns ON when sufficient voltage is generated.

Circuit Description
Energy Generation
Two 12V DC geared motors are mechanically coupled to two spur gears driven by a rack.
The motors generate DC voltage whenever the Smart Step tile is pressed.

Power Conditioning
The outputs of both generators are combined using Schottky diodes.
A 4700µF capacitor smooths the generated voltage.
A supercapacitor stores the harvested energy.

Voltage Regulation
The stored voltage is supplied to a 7805 voltage regulator.
The regulator provides a stable 5V supply for the STM32 NUCLEO board.

Voltage Sensing
A resistor divider scales the generated voltage to the STM32 ADC input range (0–3.3V).
STM32 continuously measures the generated voltage.

Output Indication
The STM32 controls a green LED.
Whenever the generated voltage exceeds a predefined threshold, the LED turns ON.

Future Improvements
- OLED Display
- ESP8266 Wi-Fi Monitoring
- Battery Charging Circuit
- USB Output
- Energy Logging
- IoT Dashboard
- Mobile App Monitoring
