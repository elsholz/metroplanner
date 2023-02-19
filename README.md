# Metroplanner

The Metroplanner is a webtool for creating simple and readable public transport maps in a diagram-like style.
It utilizes Javascript to render the transit maps in plain HTML.
The goal for the maps is to have small file sizes while maintaining high readability by supporting different zoom levels.
Additionally, the simplistic layout is supposed to make editing the maps easy and intuitive, thereby enabling anyone to create transit diagrams for their city, area or municipality.

One instance of the Metroplanner is currently hosted under [ich-hab-plan.de](https://ich-hab-plan.de).

## State of Development

The project is currently in its early state of development.
Implementation fo the following features is aimed at:

1. Plan Viewer:
    - fast loading times
2. Plan Editor:
    - edit plans
    - recover past plan state
3. Listing Plans by following criteria:
    - Match search term
    - Show most popular
    - Show highlighted plans
4. Link Sharing:
    - Create links to publicly share plans

## Tech Stack

- Frontend: VueJS + Quasar
- Backend: Node + ExpressJS
- Database: MongoDB
- Authentication: Auth0

## Class Diagram

![Class Diagram](http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/elsholz/metroplanner/puml_simple/docs/metroplanner.puml)

## API

The REST API is started by running `npm start` in the `backend` directory and then runs on port `3000`.
The API is separated into 2 access classes: the public API and the private API.
 API Documentation can be found [here](https://app.swaggerhub.com/apis/elsholz/metroplanner/1.0.0).
