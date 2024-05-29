# rpi_VOC
Dash server locally hosts a live-updating graph of multiple data traces from sensors connected to a Raspberry Pi and writes data to csv file. Compatible sensors are from Adafruit's portable environmental sensor collection, including the PM2.5 particulate air quality (multiple particle sizes), BME680 (pressure, temperature, humidity, altitude, VOC), and SCD-30 (CO2) sensors. 

All connected sensors are shown on the live-updating graph and legend; disconnected sensors are not shown. 
- Click on one data trace in the legend to hide it from the graph, and click again to show it.
- Double-click on the legend to hide all traces, and double-click again to show all.
- Click and drag on the graph to zoom in on a section, and double-click to zoom out again.
- Click the Stop button once to pause taking readings, and click again to resume taking readings.

VOCs are inversely related to electrical resistance in the air and are indirectly measured as such, i.e. fewer VOCs mean more resistance while more VOCs mean less resistance. VOC stands for volatile organic compound; the less of them in the air the better, hence higher resistance readings mean cleaner air. 

CSV files of data collected from each sensor are automatically created on the user's computer and data values are continually written to the files as the sensors run. The files can be accessed at any time while sensors are running or between sensor restarts, but will be wiped clean each time the sensors restart. To retain a file's data between sensor restarts, rename the file of interest before restarting the sensors, which allows the renamed file to remain intact although no new data values will be appended to it.

Plotly graph autoscaling often means other data traces will appear to be zero simply because they have much smaller measurements compared to electrical resistance, which is in the hundreds of thousands of Ohms. Zoom in enough on the other traces and they will show readings.
