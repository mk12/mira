# Mira

Mira is an fun and simple communication app.

Think of Mira as a virtual notepad on your friend or loved one's desk. Leave a note or drawing to brighten their day. Check back later to see if they left a reply.

Mira is ...

- **personal**: It's just you and another person. How you use it is up to you.
- **ephemeral**: Whatever you draw will slowly fade away over the next 24 hours.
- **unobtrusive**: There are no notifications. Never worry about interrupting.

## Features

Current features:

- **Accounts**: Log in with a username and password.
- **Canvas**: Type or draw on the shared canvas (the "Mira").
- **Sync**: Syncing with the server happens periodically (not real time).
- **Fading**: Drawings fade slowly over the course of hours.
- **Friends**: You get a separate Mira for each friend you connect with.

Planned features:

- **Encryption**: User content should be encrypted in the database.

## Overview

This project has two parts:

1. Front end: a [SPA][] built with [Vue][], found in [web/](web).
2. Back end: a [Flask][] server, found in [mira/](mira).

In production, the back end serves both web pages and API endpoints.

## Getting started

First, you need to get the dependencies.
run.sh
venv
..

## Deployment

run prod

This repository is already set up to be deployed on [Heroku][].

## Why "Mira"?

In elementary school, we used a transparent mirror called a [Mira][] to draw symmetrical figures. This project is similar in that it both reflects your drawings and lets you see through to what someone else draws on the other side.

## License

© 2019 Mitchell Kember

Mira is available under the MIT License; see [LICENSE](LICENSE.md) for details.


---

## Development

OPTIONALLY
- pyenv
- virtualenv/venv

TODO

> ## Front end

> The code lives in the `docs` directory (it's not documentation, that's just the name GitHub requires). It uses jQuery and [Fabric.js](http://fabricjs.com).

> For development, just open [index.html](docs/index.html) in your browser.

> ## Back end

> The back end is served by Heroku.

> The code lives in the `master` branch. It uses Python 3, [Flask](http://flask.pocoo.org), and PostgreSQL.

> For development, use [install_deps.sh](install_deps.sh) and [run.sh](run.sh).

## UI
```
yarn install
```

### Compiles and hot-reloads for development
```
yarn run serve
```

### Compiles and minifies for production
```
yarn run build
```

### Run your tests
```
yarn run test
```

### Lints and fixes files
```
yarn run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

## License

© 2019 Mitchell Kember

Mira is available under the MIT License; see [LICENSE](LICENSE.md) for details.

[Fabric.js]: http://fabricjs.com
[Flask]: http://flask.pocoo.org
[Heroku]: https://heroku.com
[Mira]: https://www.mrlondonsclass.com/mira.html
[SPA]: https://en.wikipedia.org/wiki/Single-page_application
[Vue]: https://vuejs.org
