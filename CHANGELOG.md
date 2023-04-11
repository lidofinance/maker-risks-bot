## [1.10.1](https://github.com/lidofinance/maker-risks-bot/compare/1.10.0...1.10.1) (2023-04-11)


### Bug Fixes

* allow retry on null transaction receipt ([47aac4f](https://github.com/lidofinance/maker-risks-bot/commit/47aac4fe89ec2e51d6f434ac0463473fc8c33041))
* use getLogs instead of createFilter ([fdf8258](https://github.com/lidofinance/maker-risks-bot/commit/fdf825839208a9ae3675a1b22ffb41e8ee419f20))



# [1.10.0](https://github.com/lidofinance/maker-risks-bot/compare/1.9.0...1.10.0) (2023-01-30)


### Features

* expose provider to RPC metrics ([3d918e8](https://github.com/lidofinance/maker-risks-bot/commit/3d918e8c408cad8e809b3bc7fb8b4b0e93102121))
* expose provider to RPC metrics ([2004764](https://github.com/lidofinance/maker-risks-bot/commit/200476444104ecaabf3e8f5f57dbb96d9a122cd4))



# [1.9.0](https://github.com/lidofinance/maker-risks-bot/compare/1.8.0...1.9.0) (2023-01-12)


### Bug Fixes

* add fallback for eth provider ([c5cad3d](https://github.com/lidofinance/maker-risks-bot/commit/c5cad3d9fc5fab7d93a35a7b66fba8eb832b0f6b))
* division by zero ([0bc90b4](https://github.com/lidofinance/maker-risks-bot/commit/0bc90b4662a8b8a317aa6c047d007166fae8bf49))
* fix main cycle's error handle ([9245d7b](https://github.com/lidofinance/maker-risks-bot/commit/9245d7bc6d90bc756fc8893ef46585cf7ad05041))
* remove unused computation ([0d9bac6](https://github.com/lidofinance/maker-risks-bot/commit/0d9bac6b1eef5fed09ce5b6e65f8f3623924fdf4))
* upd rules ([3f7c60d](https://github.com/lidofinance/maker-risks-bot/commit/3f7c60dc2f5af7cf656fffb762c9e4fce9b41b6e))
* use loan value round ([bb24b88](https://github.com/lidofinance/maker-risks-bot/commit/bb24b88dfdfce666cfd2286e46dcb442179735bd))


### Features

* add retryable middleware ([a90c8f3](https://github.com/lidofinance/maker-risks-bot/commit/a90c8f352a76512cbe0a6c0c0af385907daa1608))
* expose loans value to alerts ([56d7fff](https://github.com/lidofinance/maker-risks-bot/commit/56d7fff2e399e1d1defd3c5b91c7dd9c0d038de0))
* rethink main loop ([b5cc629](https://github.com/lidofinance/maker-risks-bot/commit/b5cc6295b89da4aa93ee60dbb6d557337bb7e422))
* update middleware ([5778d40](https://github.com/lidofinance/maker-risks-bot/commit/5778d40380efb254fe7d46cfd99eb067dc9a6bc3))



# [1.8.0](https://github.com/lidofinance/maker-risks-bot/compare/1.7.0...1.8.0) (2022-09-29)


### Bug Fixes

* upd rules ([e06aee9](https://github.com/lidofinance/maker-risks-bot/commit/e06aee9969f1b2aa5344e62df98c6b01d5762441))


### Features

* expose loans value to alerts ([6521035](https://github.com/lidofinance/maker-risks-bot/commit/6521035e56c3ac8079bf2a4f62354893d01e09e7))



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



