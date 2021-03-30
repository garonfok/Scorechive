# Scorechive

Scorechive is a fast and lightweight CLI program that is designed to keep track of your music scores using SQLite.

## Summary

- [Scorechive](#scorechive)
  - [Summary](#summary)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installing](#installing)
    - [Usage](#usage)
      - [Options](#options)
      - [Commands](#commands)
  - [Built With](#built-with)
  - [Contributing](#contributing)
  - [Authors](#authors)
  - [Versioning](#versioning)
  - [License](#license)

## Getting Started

### Prerequisites

- Python 3.9.2+
- [pip](https://pypi.python.org/pypi/pip)

### Installing

```zsh
pip install -r requirements.txt
```

### Usage

```zsh
python scorechive [OPTIONS] COMMAND [ARGS]...
```

#### Options

```zsh
--help  Show this message and exit.
```

#### Commands

```zsh
add      Add a score.
create   Create a database.
delete   Delete a score.
insert   Insert instrumentation to a score.
version  Show version number.
view     View all scores.
```

## Built With

- [Contributor Covenant](https://www.contributor-covenant.org/) - Used for the Code of Conduct
- [MIT](https://opensource.org/licenses/MIT) - Used to choose the license

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code
of conduct, and the process for submitting pull requests to us.

## Authors

- **Garon Fok**
- **Billie Thompson** - *Provided README Template* - [PurpleBooth](https://github.com/PurpleBooth)

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions
available, see the [tags on this
repository](https://github.com/GaronFok/scorechive/tags).

## License

This project is licensed under the [MIT](LICENSE)
License - see the [LICENSE](LICENSE) file for
details
