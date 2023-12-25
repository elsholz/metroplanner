# Metroplanner

The Metroplanner is a webtool for creating simple and readable public transport maps in a diagram-like style.
It utilizes Javascript to render the transit maps in plain HTML.
The goal for the maps is to have small file sizes while maintaining high readability by supporting different zoom levels.
Additionally, the simplistic layout is supposed to make editing the maps easy and intuitive, thereby enabling anyone to create transit diagrams for their city, area or municipality.

The development instance of the Metroplanner is currently hosted under [dev.ich-hab-plan.de](https://dev.ich-hab-plan.de).

You can find more information about the project on [dev.ich-hab-plan.de/project](https://dev.ich-hab-plan.de/project) (in German)

## Tech Stack

- Frontend: VueJS + Quasar <br>See directory `q-frontend`
- Backend: Serverless AWS API Gateway + Lambda <br>See directory `api`
- Database: MongoDB
- Authentication: Auth0
- Deployment: AWS SAM, GitHub Actions
