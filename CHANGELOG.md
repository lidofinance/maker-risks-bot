# [1.7.0](https://github.com/lidofinance/maker-risks-bot/compare/1.6.0...1.7.0) (2022-09-15)


### Bug Fixes

* **grafana:** fix timestamps metrics panels ([0ed067b](https://github.com/lidofinance/maker-risks-bot/commit/0ed067be39650d252eb89c55733d4975684f2ec3))
* passthrough log level ([ebcdd1f](https://github.com/lidofinance/maker-risks-bot/commit/ebcdd1fb19b21b502150e86c81c813fc669044b7))
* **prometheus:** update rules thresholds ([515e444](https://github.com/lidofinance/maker-risks-bot/commit/515e44490aa025313617de1e6aa750d8a010b38f))
* update curl version ([0feef9f](https://github.com/lidofinance/maker-risks-bot/commit/0feef9f67251fde6cd6d6bbd06755f69bb998093))
* update Dockerfile for the latest Debian ([3773c63](https://github.com/lidofinance/maker-risks-bot/commit/3773c631b1220563a5f9edcfdcdaefc315514004))


### Features

* add build-info parsing ([c3ed854](https://github.com/lidofinance/maker-risks-bot/commit/c3ed854a6f06ee53044931f6b15065fff8503e39))
* **grafana:** udpated blocks related panels ([a5bce64](https://github.com/lidofinance/maker-risks-bot/commit/a5bce64102194f53bfd56aa56721056cd05c0a68))
* **metrics:** improve status metrics and update prometheus rules ([e873605](https://github.com/lidofinance/maker-risks-bot/commit/e8736058561fec59a1661d3f035179ea637b868d))
* parse data onchain ([#37](https://github.com/lidofinance/maker-risks-bot/issues/37)) ([91b83f2](https://github.com/lidofinance/maker-risks-bot/commit/91b83f23a8e8d6ef0a9aa4a7af0374bb3be3fa13))
* remove Maker DataAPI parser ([aba077c](https://github.com/lidofinance/maker-risks-bot/commit/aba077c84be4501d08571c1a98c67c7df121e5a7))



# [1.6.0](https://github.com/lidofinance/maker-risks-bot/compare/1.5.0...1.6.0) (2022-08-11)


### Bug Fixes

* **grafana:** fix timestamps metrics panels ([ea1ab4f](https://github.com/lidofinance/maker-risks-bot/commit/ea1ab4fcce0ae9999267ce30437d64973f64a558))
* update curl version ([0006ebb](https://github.com/lidofinance/maker-risks-bot/commit/0006ebbffded4161f95ac0ac36196c3eab9e6989))


### Features

* **metrics:** improve status metrics and update prometheus rules ([e9374ec](https://github.com/lidofinance/maker-risks-bot/commit/e9374ecd4d854e6f2b8d9259f85a6d3d7bb16fa3))



# [1.5.0](https://github.com/lidofinance/maker-risks-bot/compare/1.4.0...1.5.0) (2022-07-29)


### Bug Fixes

* CI workflows ([1175abb](https://github.com/lidofinance/maker-risks-bot/commit/1175abb27a89f17b4dc7791c82350dfff0617ff0))
* **grafana:** one more datasource fix ([#8](https://github.com/lidofinance/maker-risks-bot/issues/8)) ([414aecf](https://github.com/lidofinance/maker-risks-bot/commit/414aecf9c0846cbffe2c7a56a96ae1534a0b16a9))
* retrieve token on demand only ([1cef262](https://github.com/lidofinance/maker-risks-bot/commit/1cef262e96fb2c17f64d40c1cd65e2ccde6b48e0))
* testnet deploy ([dd496ca](https://github.com/lidofinance/maker-risks-bot/commit/dd496ca27ed5bc6c9e72094dfb8526ce1ef86371))


### Features

* **grafana:** add status dashboard ([afdfa3f](https://github.com/lidofinance/maker-risks-bot/commit/afdfa3f2ca48bfda1fbb480712ac998e0b4f1f55))
* **metrics:** add BUILD_INFO metric ([#19](https://github.com/lidofinance/maker-risks-bot/issues/19)) ([69be2eb](https://github.com/lidofinance/maker-risks-bot/commit/69be2eba999fd0a7b92896fd2ca5197f7b46d70e))



# [1.4.0](https://github.com/lidofinance/maker-risks-bot/compare/1.3.2...1.4.0) (2022-06-07)


### Features

* **metrics:** add BUILD_INFO metric ([#19](https://github.com/lidofinance/maker-risks-bot/issues/19)) ([32311ca](https://github.com/lidofinance/maker-risks-bot/commit/32311caeb20ac24439aae77a6bf5fea45dc6566c))



## [1.3.2](https://github.com/lidofinance/maker-risks-bot/compare/1.3.1...1.3.2) (2022-06-03)


### Bug Fixes

* CI workflows ([4c93624](https://github.com/lidofinance/maker-risks-bot/commit/4c93624cbe141929d2d8220cd8aff69bbb0a266d))



## [1.3.1](https://github.com/lidofinance/maker-risks-bot/compare/1.3.0...1.3.1) (2022-06-03)


### Bug Fixes

* **grafana:** one more datasource fix ([#8](https://github.com/lidofinance/maker-risks-bot/issues/8)) ([#14](https://github.com/lidofinance/maker-risks-bot/issues/14)) ([2cb45ae](https://github.com/lidofinance/maker-risks-bot/commit/2cb45ae9d9ff55244ebbf8dd6586d93e98b858db))



# [1.3.0](https://github.com/lidofinance/maker-risks-bot/compare/1.2.1...1.3.0) (2022-06-03)


### Bug Fixes

* cleanup environment variables ([eec16de](https://github.com/lidofinance/maker-risks-bot/commit/eec16def08718b161537f717f72a3883caa5dacd))
* fix wrong time interval ([5cae0cf](https://github.com/lidofinance/maker-risks-bot/commit/5cae0cf20b8e718bea0ce9132546b478bba5cb6c))
* replace datasource with null ([1fc7490](https://github.com/lidofinance/maker-risks-bot/commit/1fc7490d2f14252f5edcd77335db6f087549945d))


### Features

* add wstETH_B ilk ([982e282](https://github.com/lidofinance/maker-risks-bot/commit/982e28241d48fb8cc72d6db8c3b490968f247155))
* **metrics:** add ETH RPC requests metrics ([e756df0](https://github.com/lidofinance/maker-risks-bot/commit/e756df01824f8f42fd02b42a23750370d131da3d))
* **metrics:** add HTTP requests metrics ([016818a](https://github.com/lidofinance/maker-risks-bot/commit/016818ac80a51d3b131df5bb4938ab1cc730c657))
* **metrics:** add misc metrics ([3e1e6f3](https://github.com/lidofinance/maker-risks-bot/commit/3e1e6f36fadfd36fa1f429dcd2d1d5ebc9685112))



# [1.1.0](https://github.com/lidofinance/maker-risks-bot/compare/e0d0e6fd3ff44802fb629e97eed4be549e46a0cb...1.1.0) (2022-05-20)


### Bug Fixes

* fix dev workflow name ([60353eb](https://github.com/lidofinance/maker-risks-bot/commit/60353eb669db0aee4905a63e68947628dc4cf8fe))
* fix workflows names ([9b8bb7a](https://github.com/lidofinance/maker-risks-bot/commit/9b8bb7a04d93f9c750a8b23ffcbc4928d31deda8))
* update prometheus rules for ilks sharding ([ac3ee81](https://github.com/lidofinance/maker-risks-bot/commit/ac3ee813fff80f2febf630bf40af904224c73314))


### Features

* add last updated at metric ([e0d0e6f](https://github.com/lidofinance/maker-risks-bot/commit/e0d0e6fd3ff44802fb629e97eed4be549e46a0cb))



