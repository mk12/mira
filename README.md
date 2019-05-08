# Mira

TODO: mention BEM, json response format.

Mira is an fun and simple communication app.

Think of Mira as a virtual notepad on your friend or loved one's desk. Leave a note or drawing to brighten their day. Check back later to see if they left a reply.

_Mira is …_

- **Personal**: It's just you and another person. How you use it is up to you.
- **Ephemeral**: Whatever you draw will slowly fade away over the next 24 hours.
- **Unobtrusive**: There are no notifications. Never worry about interrupting someone.

## Features

Current features:

- **Accounts**: Log in with a username and password.
- **Canvas**: Type or draw on the shared canvas (the "Mira").
- **Sync**: It syncs with the server periodically (not real-time).
- **Fading**: Drawings fade slowly over the course of hours.
- **Friends**: You get a separate Mira for each friend you connect with.

Planned features:

- **Encryption**: User content should be encrypted in the database.

## Overview

This project has two parts:

1. **Front end**: a [SPA][] built with [Vue][], found in [web/](web).
2. **Back end**: a [Flask][] server written in Python 3, found in [mira/](mira).

In production, the back end serves both web pages and API endpoints.

## Getting started

First, use `./run.sh install` to get the dependencies. On macOS, it will automatically install Python3, PostgreSQL, and Yarn if necessary using [Homebrew][]. On other platforms, it tells you what you need to install manually. Next, it will `pip install` Python dependencies and `yarn add` JavaScript dependencies.

> **Note**: If you don't want to pollute your system with extra Python packages, consider entering a virtual environment with [venv][] or [virtualenv][] before running the script.

Second, run `./run.sh db:create` to create a PostgreSQL database. It will store files in `database/` under the project root.

Finally, use `./run.sh dev` and `./run.sh web` to start up the Flask server and Vue server, respectively. In production there is only one server, but in development we use two in order to have hot reloading for both Flask and Vue. You can also run `vue ui` to use the Vue Web GUI instead of `./run.sh web`.

Check out `./run.sh -h` to see what else the script can do.

## Deployment

Use `./run.sh prod` to serve the site as it would be in production. In particular, this calls `yarn run build` to build the Vue app into static bundles and then serves the Flask app using [Waitress][].

This repository is already set up to be deployed on [Heroku][], so you can easily fork it and run your own instance.

_TODO: Explain other steps if there turn out to be any (secret key, migrations)._

## Why "Mira"?

In elementary school, we used a transparent mirror called a [Mira][] to draw symmetrical figures. This project is similar in that it both reflects your drawings and lets you see through to what someone else draws on the other side.

## License

© 2019 Mitchell Kember

Mira is available under the MIT License; see [LICENSE](LICENSE.md) for details.

[Flask]: http://flask.pocoo.org
[Heroku]: https://heroku.com
[Homebrew]: https://brew.sh
[Mira]: https://www.mrlondonsclass.com/mira.html
[SPA]: https://en.wikipedia.org/wiki/Single-page_application
[Vue]: https://vuejs.org
[Waitress]: https://docs.pylonsproject.org/projects/waitress/en/stable/
[venv]: https://docs.python.org/3/library/venv.html
[virtualenv]: https://virtualenv.pypa.io/en/latest/userguide/
