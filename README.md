### Maker collaterals monitoring bot

The bot is a Prometheus exporter which parses loan data from Maker protocol and calculates risk distribution based on
collateral to loan ratio, see [zones definition](#zones-definition) below.

#### Run

`docker compose`

- Create a `.env` file from `.env.example` and fill in the required variables.
- Execute command:

```bash
docker compose up -d bot
```

`docker`

- Create a `.env` file from `.env.example` and fill in the required variables.
- Build image:

```bash
docker build -t maker-risks-bot .
```

- Run container:

```bash
docker run -d -P --env-file ./.env maker-risks-bot
```

`dev`

- Expose environment variables presented at `.env.example`.
- Install dependencies via poetry:

```bash
poetry install
```

- Execute command:

```bash
python src/main.py
```

#### Zones definition

Risk zones are defined as ranges of collateral to loan ration

| Zone        | >    | <    |
| ----------- | ---- | ---- |
| A           | 2.50 | ∞    |
| B+          | 1.75 | 2.50 |
| B           | 1.50 | 1.75 |
| B-          | 1.25 | 1.50 |
| C           | 1.10 | 1.25 |
| D           | 1.00 | 1.10 |
| Liquidation | 0    | 1.00 |

#### The most essential exposed metrics

- `{}_collateral_percentage{ilk=<ilk>, zone=<zone>}` is computed percent of collaterals in the given zone
- `{}_collateral_value{ilk=<ilk>, zone=<zone>}` is computed value of collaterals in the given zone
- `{}_processing_finished_seconds{ilk=<ilk>` is timestamp of the last metrics update
- `{}_bot_last_block_num` is the last block parser results was updated against
- `{}_eth_latest_block_num` is the latest block available for the parser

#### Visualization

Pre-built Grafana dashboards are available in the `./grafana` directory. The dashboards use Prometheus as a source of
data. To run via docker compose use: `docker compose up -d bot prometheus grafana`

#### Alerting

The exporter was built primarily for alerting purposes. Therefore, in the `./prometheus` directory, predefined rules and
the related tests are located. `status.rule` is created for monitoring the status of the exporter. `zones_changes.rule`
defines rules for monitoring collaterals.

docker-compose configuration allows running the setup for alerting via Alertmanager by sending alerts to Discord.
Configure webhook parameters in `./alertmanager-discord/alertmanager-discord.yml` and start the full docker-compose
stack via command `docker compose up -d`.

## Release flow

To create new release:

1. Merge all changes to the `master` branch
1. Navigate to Repo => Actions
1. Run action "Prepare release" action against `master` branch
1. When action execution is finished, navigate to Repo => Pull requests
1. Find pull request named "chore(release): X.X.X" review and merge it with "Rebase and merge" (or "Squash and merge")
1. After merge release action will be triggered automatically
1. Navigate to Repo => Actions and see last actions logs for further details
