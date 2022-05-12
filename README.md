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

#### Exposed metrics

- `{}_collateral_percentage{zone=<zone>}` is computed percent of collaterals in the given zone
- `{}_parser_last_fetched` is timestamp of the last metrics update

#### Configuration

Configure bot via the following environment variables:

- `NODE_ENDPOINT` is Infura endpoint to fetch data from Etherium node
- `FLIPSIDE_ENDPOINT` is used to fetch indexed data from Flipside (subject to change)
- `EXPORTER_PORT` is the port to expose metrics on
- `LOG_TO_JSON` set log output in JSON

#### Visualisation

Sandbox available at the moment [here](https://grafana.testnet.fi/d/STQ5KYQ7k/maker?orgId=2).
