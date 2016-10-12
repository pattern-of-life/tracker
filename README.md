# Project Name: TrackerPy

## Project Team Members: Victor Benavente, David Banks, Justin Lange, Derek Hewitt

## Project Summary:

The goal of this project is to demonstrate proof-of-concept for a small form factor python based hardware tracking device.

Minimum Viable Product Goals:
- Transmit GPS data in realtime from a hardware device
- Store GPS data for later transmission on said device if transmission is not possible at a given time
- Log said data as it's received by our server's API endpoint
- Allow user to create a new account, add and remove devices, data points, routes, etc
- Display tracking and site data in an attractive, professional format

Stretch Goals:
- Finely grained control of device via front end, to include:
  - Adjustment of 'blackout' periods
  - Adjustment of logging/transmission intervals
  - Automatic logging/termination of signal based on position or 'fences'
- Additional battery sources
- Improve device packaging and presentation

See Github Issues for additional Stretch Goal information.  Issues marked 'S#' are stretch goals, with the # denoting the difficuty of the task.


## Work Flow
* Once MVP is achieved Master should represent a viable production product at all times.
* All work will be done from a branch off the development branch, or a sub branch off of development branch.

## Agile Tool
* Our team has elected to use Github Issues to track our progress and project status.
* We also made extensive use of whiteboards and TODO lists.

## API Documentation
* Our trackers hit an external API endpoint that allows them to update us of their status in a RESTful manner.

PATH: /device/data/create
POST with fields:
time: mm/dd/yyyy hh:mm:ss
lat: float
lon: float
elevation: float
uuid: UUID
