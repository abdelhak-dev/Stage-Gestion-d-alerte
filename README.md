# Temperature and Humidity Monitoring & Alerting using Grafana 

This project hold 4 parts :
  - Temperature and Humidity Gathering using Arduino Yun From 3 Sensors DHT11 and PIR Sensor.
  - Sending Informations to The Raspberry Pi Server using RestAPI.
  - Display Temperature & Humidity & Date & Presence in the Server Room in Grafana Dashboard.
  - Alerting by Email The Temperature and Humidity 
  
  ## Python Modules and Framework :
  
  - Fastapi
  - Uvicorn
  - Sqlite3
  
  ## Installation 
  To install run the following commands
  ```docker
  1) $ sudo docker-compose build
  2) $ sudo docker-compose up
 ```
## API Queries

To consult the API documentation tape 127.0.0.3:8000/docs

- Add Sensor :
/add_Sensor/{SensorID}/{SensorRef}/{Type}

- To test the information sending from sensors use:

      /UpdateTempHumid/{SensorRef}/{SensorID}/{Temperature}/{Humidity}

      /UpdatePresence/{SensorRef}/{SensorID}/{Presence}
- To Check the Temperature :
    /AfficheTemp/
    
- To Check the Humidity :
    /AfficheHumid/
