!function(modules){var installedModules={};function __webpack_require__(moduleId){if(installedModules[moduleId])return installedModules[moduleId].exports;var module=installedModules[moduleId]={i:moduleId,l:!1,exports:{}};return modules[moduleId].call(module.exports,module,module.exports,__webpack_require__),module.l=!0,module.exports}__webpack_require__.m=modules,__webpack_require__.c=installedModules,__webpack_require__.d=function(exports,name,getter){__webpack_require__.o(exports,name)||Object.defineProperty(exports,name,{enumerable:!0,get:getter})},__webpack_require__.r=function(exports){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(exports,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(exports,"__esModule",{value:!0})},__webpack_require__.t=function(value,mode){if(1&mode&&(value=__webpack_require__(value)),8&mode)return value;if(4&mode&&"object"==typeof value&&value&&value.__esModule)return value;var ns=Object.create(null);if(__webpack_require__.r(ns),Object.defineProperty(ns,"default",{enumerable:!0,value:value}),2&mode&&"string"!=typeof value)for(var key in value)__webpack_require__.d(ns,key,function(key){return value[key]}.bind(null,key));return ns},__webpack_require__.n=function(module){var getter=module&&module.__esModule?function(){return module.default}:function(){return module};return __webpack_require__.d(getter,"a",getter),getter},__webpack_require__.o=function(object,property){return Object.prototype.hasOwnProperty.call(object,property)},__webpack_require__.p="",__webpack_require__(__webpack_require__.s=2)}([function(module,__webpack_exports__,__webpack_require__){"use strict";(function(global){__webpack_exports__.a=(global.kolibriPluginDataGlobal||{})["kolibri.core.frontend_head_assets"]||{}}).call(this,__webpack_require__(1))},function(module,exports){var g;g=function(){return this}();try{g=g||new Function("return this")()}catch(e){"object"==typeof window&&(g=window)}module.exports=g},function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var NAME="name",VERSION="version",browserTests=[{test:/\s(opr)\/([\w.]+)/i,map:[[NAME,"Opera"],VERSION]},{tests:[/(?:ms|\()(ie)\s([\w.]+)/i,/(trident).+rv[:\s]([\w.]+).+like\sgecko/i],map:[[NAME,"IE"],VERSION]},{test:/(edge|edgios|edga)\/((\d+)?[\w.]+)/i,map:[[NAME,"Edge"],VERSION]},{test:/\swv\).+(chrome)\/([\w.]+)/i,map:[[NAME,/(.+)/,"$1 WebView"],VERSION]},{test:/android.+version\/([\w.]+)\s+(?:mobile\s?safari|safari)*/i,map:[VERSION,[NAME,"Android Browser"]]},{test:/(chrome)\/v?([\w.]+)/i,map:[NAME,VERSION]},{test:/((?:android.+)crmo|crios)\/([\w.]+)/i,map:[[NAME,"Chrome"],VERSION]},{test:/fxios\/([\w.-]+)/i,map:[VERSION,[NAME,"Firefox"]]},{test:/version\/([\w.]+).+?mobile\/\w+\s(safari)/i,map:[VERSION,[NAME,"Mobile Safari"]]},{test:/version\/([\w.]+).+?(mobile\s?safari|safari)/i,map:[VERSION,NAME]},{test:/(firefox)\/([\w.-]+)$/i,map:[NAME,VERSION]}];var userAgent=window&&window.navigator&&window.navigator.userAgent?window.navigator.userAgent:"",browser=(/Android/.test(userAgent)&&/wv/.test(userAgent)||/Version\/\d+\.\d+/.test(userAgent),/Macintosh/.test(userAgent)&&(/Safari/.test(userAgent)||/Chrome/.test(userAgent)||/Firefox/.test(userAgent)),function(userAgent){var browser={name:null,version:null},outputBrowser={name:null,major:null,minor:null,patch:null};if(userAgent)for(var val,i=0;i<browserTests.length;i++){var regex=void 0;if((val=browserTests[i]).test)val.test.test(userAgent)&&(regex=val.test);else if(val.tests)for(var j=0;j<val.tests.length;j++)if(val.tests[j].test(userAgent)){regex=val.tests[j];break}if(regex){for(var result=regex.exec(userAgent),k=0;k<val.map.length;k++)val.map[k]===NAME||val.map[k]===VERSION?browser[val.map[k]]=result[k+1]:2===val.map[k].length?browser[val.map[k][0]]=val.map[k][1]:3===val.map[k].length&&(browser[val.map[k][0]]=result[k+1].replace(val.map[k][1],val.map[k][2]));break}}if(browser[NAME]&&(outputBrowser.name=browser[NAME]),browser[VERSION]){var version=browser[VERSION].split(".");version[0]&&(outputBrowser.major=version[0],version[1]&&(outputBrowser.minor=version[1],version[2]&&(outputBrowser.patch=version[2])))}return outputBrowser}(userAgent)),plugin_data_src=__webpack_require__(0);(function(browser,requirements){if(browser.major&&browser.name){var entry=requirements[browser.name];if(entry){if(browser.major<entry.major)return!1;if(browser.major===entry.major){if(entry.minor&&(browser.minor<entry.minor||!browser.minor))return!1;if(entry.minor&&browser.minor===entry.minor&&entry.patch&&(browser.patch<entry.patch||!browser.patch))return!1}}}return!0})(browser,{IE:{major:11},Android:{major:4,minor:0,patch:2}})||(window.location.href=plugin_data_src.a.unsupportedUrl)}]);
//# sourceMappingURL=kolibri.core.frontend_head_assets-0.14.0rc1.js.map