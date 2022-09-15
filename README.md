### Maker collaterals monitoring bot

Parse loans data from Maker protocol and calculate risks distribution
based on collateral to loan ratio, see zones definition below.

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

#### The most important exposed metrics

- `{}_collateral_percentage{ilk=<ilk>, zone=<zone>}` is computed percent of collaterals in the given zone
- `{}_processing_finished_seconds{ilk=<ilk>` is timestamp of the last metrics update
- `{}_bot_last_block_num` is the last block parser results was updated against
- `{}_eth_latest_block_num` is the latest block available for the parser

#### Configuration

Configure bot via the following environment variables:

- `NODE_ENDPOINT` is Infura endpoint to fetch data from Etherium node
- `PARSE_INTERVAL` is a delay in seconds between API fetches
- `EXPORTER_PORT` is the port to expose metrics on
- `LOG_FORMAT` is one of {"simple", "json"}

#### Visualisation

Sandbox available at the moment [here](https://grafana.testnet.fi/d/STQ5KYQ7k/maker?orgId=2).
