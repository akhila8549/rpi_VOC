import board
import busio
from adafruit_pm25.i2c import PM25_I2C
import adafruit_bme680
import adafruit_scd30
import time
import plotly.graph_objs as go
import dash
from dash.dependencies import Output, Input
from dash import dcc
from dash import html
from collections import deque
import csv
import pandas as pd

bme680_i2c = board.I2C()
pm25_i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
pth_data = 'PTH_data.csv'
pm25_data = 'AQ_data.csv'
co2_data = 'CO2_data.csv'
pth_y = []
# wiping the files clean each time sensors start
with(
    open(pth_data, 'w+') as pth_file,
    open(pm25_data, 'w+') as pm25_file,
    open(co2_data, 'w+') as co2_file
    ):
    pth_file.close()
    pm25_file.close()
    co2_file.close()
    
def pth(pth_file):
    try: # checking for bme680 sensor
        sensor = adafruit_bme680.Adafruit_BME680_I2C(bme680_i2c)
    except Exception as e:
        sensor = 0
    if sensor != 0:
        #if n_clicks % 2 ==0: # press Stop once to stop, press again to resume
            writer = csv.writer(pth_file)
            pth_line = []                        
            pth_line.append(sensor.gas)
            pth_line.append(sensor.temperature)
            pth_line.append(sensor.humidity)
            pth_line.append(sensor.pressure)
            pth_line.append(sensor.altitude)
            writer.writerow(pth_line)
    
def pm25(pm25_file):
    try: # checking for pm25 sensor
        pm25 = adafruit_pm25.i2c.PM25(pm25_i2c)
    except Exception as e:
        pm25 = 0
    if pm25 != 0:
        #if n_clicks % 2 ==0: # press Stop once to stop, press again to resume
            writer = csv.writer(pm25_file)
            pm25_line = []
            aqdata = pm25.read()
            pm25_line.append(aqdata['particles 03um'])
            pm25_line.append(aqdata['particles 05um'])
            pm25_line.append(aqdata['particles 10um'])
            pm25_line.append(aqdata['particles 25um'])
            pm25_line.append(aqdata['particles 50um'])
            pm25_line.append(aqdata['particles 100um'])
            writer.writerow(pm25_line)

def co2(co2_file):         
    try: # checking for a co2 sensor
        scd = adafruit_scd30.SCD30(board.I2C())
    except Exception as e: 
        scd = 0
    if scd != 0:
        #if n_clicks % 2 ==0: # press Stop once to stop, press again to resume
        
        writer = csv.writer(co2_file)
        co2_line = []
        co2_line.append(scd.CO2)
        writer.writerow(co2_line)
    
        

while True:
    app = dash.Dash(__name__) 
    app.layout = html.Div(
        [
            html.Button ('Stop', id='stop_btn', n_clicks=0),
            dcc.Graph(id = 'live-graph',
                      animate = True),
            dcc.Interval(
                id = 'graph-update',
    #             time between data updates
                interval = 5000,
    #             number of intervals completed
                n_intervals = 0
                ),
            html.Button("Download CSV", id='btn'),
            dcc.Download(id='download')           
            ]
        )
    # callbacks
    @app.callback(
            Output('live-graph', 'figure'),
            #Output('download_aq', 'data'),
            #Output('download_pth', 'data'),
            #Output('download_co2', 'data'),
            #Input('graph-update', 'n_intervals'),
            #Input('aqbtn', 'n_clicks'),
            #Input('pthbtn', 'n_clicks'),
            #Input('co2btn', 'n_clicks'),
            Input('stop_btn', 'n_clicks')
    )
    def update_graph(n_clicks):
            print(n_clicks)

            while True:

                if n_clicks % 2 ==0: # press Stop once to stop, press again to resume
                    with(
                        open(pth_data, 'a', newline='') as pth_file,
                        open(pm25_data, 'a', newline='') as pm25_file,
                        open(co2_data, 'a', newline='') as co2_file
                        ):
                        pth(pth_file)
                        pm25(pm25_file)
                        co2(co2_file)
                    with open(pth_data,'r') as pth_file:
                        reader = list(csv.reader(pth_file, delimiter=','))
                        for row in reader:
                            pass
                        pth_y.append(row[0])
                            
                        voc_data = go.Scatter(
                            x = list(range(0, len(list(reader)))),
                            y = pth_y,
                            name = 'VOC (resistance, in Ohms)',
                            mode = 'lines',
                            )
                    print(voc_data)
            return {'data':voc_data,
                        'layout': go.Layout(xaxis = dict(
                                range = [0, 15]), xaxis_title = dict(text='Time (seconds)'), clickmode = 'event+select'
                                            
                                )}
    
    if __name__ == '__main__':
        app.run_server()
    
                