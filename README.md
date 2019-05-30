# Mira

Mira is an fun and simple communication app.

Think of Mira as a virtual notepad on someone else's desk. Leave a note or drawing to brighten their day. Check back later to see if they left a reply.

_Mira is …_

- **Personal**: Share messages or doodles with a friend.
- **Ephemeral**: Drawings slowly fade away over 24 hours.
- **Unobtrusive**: No notifications. Just check when you want.

## Features

Current features:

- **Accounts**: Log in with a username and password.
- **Friends**: You get a separate Mira for each friend you connect with.
- **Canvas**: Draw on the shared canvas (the "Mira").
- **Sync**: It syncs with the server periodically (not real-time).
- **Fading**: Drawings fade slowly over the course of hours.

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

To deploy Mira on [Heroku][], follow these steps:

1. Sign into Heroku and create a new app.
2. In the "Resources" tab, add the free PostgreSQL add-on.
3. In the "Settings" tab, set the environment variable `FLASK_SECRET_KEY` to something secret.
4. Clone this repo and run `heroku git:remote -a NAME` where `NAME` is your Heroku app name.
5. Run `./run.sh deploy` on your local machine.
6. _TODO: explain initial migration._

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
