[![Build Status](https://travis-ci.org/kaelzhang/compton-futu.svg?branch=master)](https://travis-ci.org/kaelzhang/compton-futu)
[![Coverage](https://codecov.io/gh/kaelzhang/compton-futu/branch/master/graph/badge.svg)](https://codecov.io/gh/kaelzhang/compton-futu)
<!-- optional appveyor tst
[![Windows Build Status](https://ci.appveyor.com/api/projects/status/github/kaelzhang/compton-futu?branch=master&svg=true)](https://ci.appveyor.com/project/kaelzhang/compton-futu)
-->
<!-- optional npm version
[![NPM version](https://badge.fury.io/js/compton-futu.svg)](http://badge.fury.io/js/compton-futu)
-->
<!-- optional npm downloads
[![npm module downloads per month](http://img.shields.io/npm/dm/compton-futu.svg)](https://www.npmjs.org/package/compton-futu)
-->
<!-- optional dependency status
[![Dependency Status](https://david-dm.org/kaelzhang/compton-futu.svg)](https://david-dm.org/kaelzhang/compton-futu)
-->

# compton-futu

Ost.AI quant for futu

## Design

### Provides a restful API

> For now (2020-03-02), Python gRPC does **NOT** support asyncio
> So, we only provide a rest APIs

- subscribe to a new stock code

## ENV

> Actually, all ENV variables are of string type

- **SERVER_PORT?** `int=80` server port
- **FUTU_HOST** `str` host of FutuOpenD
- **FUTU_PORT** `str=11111` port of FutuOpenD

## License

[MIT](LICENSE)
