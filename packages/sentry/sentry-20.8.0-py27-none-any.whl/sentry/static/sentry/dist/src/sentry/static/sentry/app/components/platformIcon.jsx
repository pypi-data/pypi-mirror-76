import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import PlatformIconTile from './platformIconTile';
var PLATFORM_TO_ICON = {
    apple: 'apple',
    cocoa: 'apple',
    cordova: 'cordova',
    csharp: 'csharp',
    elixir: 'elixir',
    electron: 'electron',
    go: 'go',
    java: 'java',
    'java-android': 'java',
    'java-appengine': 'app-engine',
    'java-log4j': 'java',
    'java-log4j2': 'java',
    'java-logback': 'java',
    'java-logging': 'java',
    javascript: 'javascript',
    'javascript-angular': 'angularjs',
    'javascript-backbone': 'javascript',
    'javascript-ember': 'ember',
    'javascript-react': 'react',
    'javascript-vue': 'vue',
    node: 'nodejs',
    'node-connect': 'nodejs',
    'node-express': 'nodejs',
    'node-koa': 'nodejs',
    'objective-c': 'apple',
    perl: 'perl',
    php: 'php',
    'php-laravel': 'laravel',
    'php-monolog': 'php',
    'php-symfony2': 'php',
    python: 'python',
    'python-flask': 'flask',
    'python-sanic': 'python',
    'python-bottle': 'bottle',
    'python-celery': 'python',
    'python-django': 'django',
    'python-pylons': 'python',
    'python-pyramid': 'python',
    'python-rq': 'python',
    'python-tornado': 'python',
    'python-pythonawslambda': 'python',
    ruby: 'ruby',
    'ruby-rack': 'ruby',
    'ruby-rails': 'rails',
    'react-native': 'react-native',
    rust: 'rust',
    swift: 'swift',
};
export function getIcon(platform) {
    var icon = PLATFORM_TO_ICON[platform];
    if (!icon) {
        return 'generic';
    }
    return icon;
}
var PlatformIcon = function (_a) {
    var platform = _a.platform, size = _a.size, props = __rest(_a, ["platform", "size"]);
    var width = props.width || size || '1em';
    var height = props.height || size || '1em';
    if (platform === 'react-native') {
        // TODO(Priscila): find a better way to do it, maybe by removing the react svg path fill attributes
        return (<StyledPlatformIconTile platform={platform} width={width} height={height} {...props}/>);
    }
    var icon = getIcon(platform);
    return (<img src={require("platformicons/svg/" + icon + ".svg")} width={width} height={height} {...props}/>);
};
export default PlatformIcon;
// TODO(color): theme doesn't have the color #625471
var StyledPlatformIconTile = styled(PlatformIconTile, {
    shouldForwardProp: function (prop) { return prop !== 'width' && prop !== 'height'; },
})(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  width: ", ";\n  height: ", ";\n  position: relative;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  :before {\n    position: absolute;\n  }\n"], ["\n  width: ", ";\n  height: ", ";\n  position: relative;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  :before {\n    position: absolute;\n  }\n"])), function (p) { return p.width; }, function (p) { return p.height; });
var templateObject_1;
//# sourceMappingURL=platformIcon.jsx.map