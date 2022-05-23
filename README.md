### Maker collaterals monitoring bot

Parse loans data from Maker protocol and calculate risks distribution 
based on collateral to loan ratio, see zones definition below.

#### Data sources

Vaults collected from [Maker Data API](https://data-api.makerdao.network).

Additional information about single vault collected via direct requests to ETH1 node.

#### Zones definition

Risk zones defined as a ranges of collateral to loan ration


| Zone        | >    | <    |
|-------------|------|------|
| A           | 2.50 | ∞    |
| B+          | 1.75 | 2.50 |
| B           | 1.50 | 1.75 |
| B-          | 1.25 | 1.50 |
| C           | 1.10 | 1.25 |
| D           | 1.00 | 1.10 |
| Liquidation | 0    | 1.00 |

#### Exposed metrics

- `{}_collateral_percentage{zone=<zone>}` is computed percent of collaterals in the given zone
- `{}_parser_last_fetched` is timestamp of the last metrics update
- `{}_parser_last_block` is the last block Maker database was updated against

#### Configuration

Configure bot via the following environment variables:

- `NODE_ENDPOINT` is Infura endpoint to fetch data from Etherium node
- `MAKER_DATAAPI_USERNAME` is the https://data-api.makerdao.network user's username
- `MAKER_DATAAPI_PASSWORD` is the https://data-api.makerdao.network user's password
- `PARSE_INTERVAL` is a delay in seconds between API fetches
- `EXPORTER_PORT` is the port to expose metrics on
- `LOG_FORMAT` is one of {"simple", "json"}

#### Visualisation

Sandbox available at the moment [here](https://grafana.testnet.fi/d/STQ5KYQ7k/maker?orgId=2).
