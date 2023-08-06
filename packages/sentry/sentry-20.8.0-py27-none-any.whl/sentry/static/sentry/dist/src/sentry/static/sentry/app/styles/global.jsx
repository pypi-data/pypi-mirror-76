import { __makeTemplateObject } from "tslib";
import React from 'react';
import { Global, css } from '@emotion/core';
import { IS_CI } from 'app/constants';
var styles = function (theme) { return css(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  body {\n    .sentry-error-embed-wrapper {\n      z-index: ", ";\n    }\n  }\n\n  abbr {\n    border-bottom: 1px dotted ", ";\n  }\n\n  /**\n   * See https://web.dev/prefers-reduced-motion/\n   */\n  @media (prefers-reduced-motion) {\n    *,\n    ::before,\n    ::after {\n      animation-delay: -1ms !important;\n      animation-duration: 0ms !important;\n      animation-iteration-count: 1 !important;\n      background-attachment: initial !important;\n      scroll-behavior: auto !important;\n      transition-duration: 0s !important;\n      transition-delay: 0s !important;\n    }\n  }\n\n  ", "\n"], ["\n  body {\n    .sentry-error-embed-wrapper {\n      z-index: ", ";\n    }\n  }\n\n  abbr {\n    border-bottom: 1px dotted ", ";\n  }\n\n  /**\n   * See https://web.dev/prefers-reduced-motion/\n   */\n  @media (prefers-reduced-motion) {\n    *,\n    ::before,\n    ::after {\n      animation-delay: -1ms !important;\n      animation-duration: 0ms !important;\n      animation-iteration-count: 1 !important;\n      background-attachment: initial !important;\n      scroll-behavior: auto !important;\n      transition-duration: 0s !important;\n      transition-delay: 0s !important;\n    }\n  }\n\n  ",
    "\n"])), theme.zIndex.sentryErrorEmbed, theme.gray500, IS_CI
    ? css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n        input,\n        select {\n          caret-color: transparent;\n        }\n      "], ["\n        input,\n        select {\n          caret-color: transparent;\n        }\n      "]))) : ''); };
/**
 * Renders an emotion global styles injection component
 */
var GlobalStyles = function (_a) {
    var theme = _a.theme;
    return <Global styles={styles(theme)}/>;
};
export default GlobalStyles;
var templateObject_1, templateObject_2;
//# sourceMappingURL=global.jsx.map