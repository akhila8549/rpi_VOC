# rpi_VOC
Dash server hosts a live-updating graph of multiple data traces from BME680 sensor &amp; writes data to csv file.

VOCs are inversely related to electrical resistance in the air and are indirectly measured as such, i.e. fewer VOCs mean more resistance while more VOCs mean less resistance. VOC stands for volatile organic compound; the less of them in the air the better, hence higher resistance readings mean cleaner air. 

Plotly graph autoscaling often means other data traces will appear to be zero simply because they have much smaller measurements compared to electrical resistance, which is in the hundreds of thousands of Ohms. Zoom in enough on the other traces and they will show readings.

Create a csv file named VOC_data.csv before running the code to ensure data is saved in the right place.


