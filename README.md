# Mira

Mira is an ephemeral communication app.

Features:

- Share messages and drawings with another person.
- Canvas contents slowly fade over the course of hours.
- Optionally keep a history of snapshots.

## Development

## Front end

The web front end is served by GitHub Pages at https://mk12.github.io/mira/.

The code lives in the `docs` directory (it's not documentation, that's just the name GitHub requires). It uses jQuery and [Fabric.js](http://fabricjs.com).

For development, just open [index.html](docs/index.html) in your browser.

## Back end

The back end is served by Heroku.

The code lives in the `master` branch. It uses Python 3, [Flask](http://flask.pocoo.org), and PostgreSQL.

For development, use [install_deps.sh](install_deps.sh) and [run.sh](run.sh).

## License

© 2019 Mitchell Kember

Mira is available under the MIT License; see [LICENSE](LICENSE.md) for details.
