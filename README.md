[![Build Status](https://travis-ci.org/kaelzhang/python-compton.svg?branch=master)](https://travis-ci.org/kaelzhang/python-compton)
[![Coverage](https://codecov.io/gh/kaelzhang/python-compton/branch/master/graph/badge.svg)](https://codecov.io/gh/kaelzhang/python-compton)
<!-- optional appveyor tst
[![Windows Build Status](https://ci.appveyor.com/api/projects/status/github/kaelzhang/python-compton?branch=master&svg=true)](https://ci.appveyor.com/project/kaelzhang/python-compton)
-->
<!-- optional npm version
[![NPM version](https://badge.fury.io/js/python-compton.svg)](http://badge.fury.io/js/python-compton)
-->
<!-- optional npm downloads
[![npm module downloads per month](http://img.shields.io/npm/dm/python-compton.svg)](https://www.npmjs.org/package/python-compton)
-->
<!-- optional dependency status
[![Dependency Status](https://david-dm.org/kaelzhang/python-compton.svg)](https://david-dm.org/kaelzhang/python-compton)
-->

# python-compton

An abstract data-flow framework for quantitative trading

## Design

### Provides a restful API

> For now (2020-03-02), Python gRPC does **NOT** support asyncio

> So, we only provide a rest APIs

- subscribe to a new stock code

## ENV

> Actually, all ENV variables are of string type

- **SERVER_PORT?** `int=80` server port
- **FUTU_HOST?** `str=localhost` host of FutuOpenD
- **FUTU_PORT?** `int=11111` port of FutuOpenD

## License

[MIT](LICENSE)
