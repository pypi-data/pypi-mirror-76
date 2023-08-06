import { __makeTemplateObject } from "tslib";
import { css, keyframes } from '@emotion/core';
var topLeftIn = keyframes(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n    0% {\n        transform:translate(-5%,-5%)\n    }\n    to {\n        transform:translate(0%,0%)\n    }\n"], ["\n    0% {\n        transform:translate(-5%,-5%)\n    }\n    to {\n        transform:translate(0%,0%)\n    }\n"])));
var bottomRightIn = keyframes(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  0% {\n    transform: translate(5%, 5%);\n  }\n  to {\n    transform: translate(0%, 0%);\n  }\n"], ["\n  0% {\n    transform: translate(5%, 5%);\n  }\n  to {\n    transform: translate(0%, 0%);\n  }\n"])));
var animateTopLeftIn = css(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  animation: 0.5s ", " cubic-bezier(0.68, -0.55, 0.265, 1.55);\n  transform-origin: center center;\n"], ["\n  animation: 0.5s ", " cubic-bezier(0.68, -0.55, 0.265, 1.55);\n  transform-origin: center center;\n"])), topLeftIn);
var animateBottomRightIn = css(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  animation: 0.5s ", " cubic-bezier(0.68, -0.55, 0.265, 1.55);\n"], ["\n  animation: 0.5s ", " cubic-bezier(0.68, -0.55, 0.265, 1.55);\n"])), bottomRightIn);
export { animateBottomRightIn, animateTopLeftIn };
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=styles.jsx.map