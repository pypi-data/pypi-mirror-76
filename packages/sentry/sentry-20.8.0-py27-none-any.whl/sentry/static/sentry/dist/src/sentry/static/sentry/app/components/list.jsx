import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import theme from 'app/utils/theme';
import space from 'app/styles/space';
export var List = styled('ul')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  list-style: none;\n  padding: 0;\n  margin-bottom: ", ";\n\n  ol& {\n    counter-reset: numberedList;\n  }\n"], ["\n  list-style: none;\n  padding: 0;\n  margin-bottom: ", ";\n\n  ol& {\n    counter-reset: numberedList;\n  }\n"])), space(2));
var IconWrapper = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  margin-right: ", ";\n\n  /* Give the wrapper an explicit height so icons are line height with the\n   * (common) line height. */\n  height: 16px;\n  align-items: center;\n"], ["\n  display: flex;\n  margin-right: ", ";\n\n  /* Give the wrapper an explicit height so icons are line height with the\n   * (common) line height. */\n  height: 16px;\n  align-items: center;\n"])), space(1));
export var ListItem = styled(function (_a) {
    var icon = _a.icon, className = _a.className, children = _a.children;
    return (<li className={className}>
    {icon && <IconWrapper>{icon}</IconWrapper>}
    {children}
  </li>);
})(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  position: relative;\n  padding-left: 34px;\n  margin-bottom: ", ";\n\n  &:before,\n  & > ", " {\n    position: absolute;\n    left: 0;\n  }\n\n  ul & {\n    color: ", ";\n    &:before {\n      content: '';\n      width: 6px;\n      height: 6px;\n      border-radius: 50%;\n      margin-right: ", ";\n      border: 1px solid ", ";\n      background-color: transparent;\n      left: 5px;\n      top: 10px;\n    }\n\n    ", "\n  }\n\n  ol & {\n    &:before {\n      counter-increment: numberedList;\n      content: counter(numberedList);\n      top: 3px;\n      display: flex;\n      align-items: center;\n      justify-content: center;\n      text-align: center;\n      width: 18px;\n      height: 18px;\n      font-size: 10px;\n      font-weight: 600;\n      border: 1px solid ", ";\n      border-radius: 50%;\n      background-color: transparent;\n      margin-right: ", ";\n    }\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  position: relative;\n  padding-left: 34px;\n  margin-bottom: ", ";\n\n  &:before,\n  & > ", " {\n    position: absolute;\n    left: 0;\n  }\n\n  ul & {\n    color: ", ";\n    &:before {\n      content: '';\n      width: 6px;\n      height: 6px;\n      border-radius: 50%;\n      margin-right: ", ";\n      border: 1px solid ", ";\n      background-color: transparent;\n      left: 5px;\n      top: 10px;\n    }\n\n    ",
    "\n  }\n\n  ol & {\n    &:before {\n      counter-increment: numberedList;\n      content: counter(numberedList);\n      top: 3px;\n      display: flex;\n      align-items: center;\n      justify-content: center;\n      text-align: center;\n      width: 18px;\n      height: 18px;\n      font-size: 10px;\n      font-weight: 600;\n      border: 1px solid ", ";\n      border-radius: 50%;\n      background-color: transparent;\n      margin-right: ", ";\n    }\n  }\n"])), space(0.5), IconWrapper, theme.gray700, space(2), theme.gray700, function (p) {
    return p.icon &&
        "\n      & > " + IconWrapper + " {\n        top: 4px;\n      }\n\n      &:before {\n        content: none;\n      }\n    ";
}, theme.gray700, space(2));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=list.jsx.map