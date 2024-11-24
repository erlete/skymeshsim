# SkyMesh Simulator

> [!IMPORTANT]
> This repository was created as part of the 8th [Cassini Hackaton](https://www.cassini.eu/hackathons/), so it does not yet represent a fully functional application. The goal is to create a simulator that can be used to test the SkyMesh network in different scenarios.

SkyMesh provides solution for network coverage in emergency situations. The solution is based on the use of drones to create a mesh network in the sky, providing internet access to the affected population. The project is part of the [Cassini Hackaton](https://www.cassini.eu/hackathons/), which aims to develop innovative solutions for the European Space Agency (ESA).

The simulator makes use of multiple resources (see [resources section](#resources)) to create a realistic scenario. The main goal is to simulate the SkyMesh network in different scenarios, such as natural disasters, to evaluate the network coverage and performance. In a typical simulation, a server-based network is set up locally, initializing the server itself, a control system for events and command communication, a data system for traces, logs and general data transmission and processing, and 0 or more independent drone clients that can be controlled by the control system and managed by the server.

## Server

The server is responsible for managing the network, receiving and sending commands to the drones, and processing the data. The server is implemented in Python using sockets for communication.

## Control System

The control system is responsible for managing the events and commands that are sent to the drones. It is user-interactive and CLI-based, so there is a set of known commands that the user can use to interact with the drones and the server. Of course, there is a `help` command that lists all available commands and their descriptions.

## Data System

The data system is responsible for storing the traces, logs, and general data transmission and processing. The endpoint is the system itself, allowing data visualization through the terminal interface and also data representation in the form of graphs and maps, using the `matplotlib` library.

## Drone

The drone is responsible for flying over the affected area and creating the mesh network. As of now, the drone is implemented in the 2D space, but the goal is to extend it to the 3D space. It simulates semi-realistic dynamic behavior, such as battery consumption, speed, and altitude control.

## Other systems

There are more systems, such as the weather, population density, and terrain systems, that are responsible for providing the necessary data for the simulation. The weather system provides the weather status in a given latitude and longitude, the population density system provides the population density of the affected area, and the terrain system provides a terrain visualization of the affected area using OpenEO systems.

## Resources

* [World population geographic data](https://hub.worldpop.org/geodata/summary?id=43889)
* [EarthEngine API](https://earthengine.openeo.org/.well-known/openeo)
* [Natural Earth Data](https://www.naturalearthdata.com/110m-cultural-vectors/)
* [Copernicus DEM](https://spacedata.copernicus.eu/es/collections/copernicus-digital-elevation-model)
* [OpenEO GitHub](https://github.com/Open-EO/openeo-community-examples/tree/main/python)
* [Python Robotics GitHub](https://github.com/AtsushiSakai/PythonRobotics/tree/master?tab=readme-ov-file#drone-3d-trajectory-following)
* [Copernicus Sentinel L2](https://sentiwiki.copernicus.eu/web/s2-applications#S2-Applications-Emergency-Management)

## Citations

Regarding the usage of WorldPop resources, please refer to the following citation:

```
WorldPop (www.worldpop.org - School of Geography and Environmental Science, University of Southampton; Department of Geography and Geosciences, University of Louisville; Departement de Geographie, Universite de Namur) and Center for International Earth Science Information Network (CIESIN), Columbia University (2018). Global High Resolution Population Denominators Project - Funded by The Bill and Melinda Gates Foundation (OPP1134076). https://dx.doi.org/10.5258/SOTON/WP00674
```

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
