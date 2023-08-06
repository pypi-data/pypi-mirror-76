import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
var NoEvents = function () { return (<Container>
    <EmptyText>{t('No activity yet.')}</EmptyText>
  </Container>); };
export default NoEvents;
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  left: 0;\n  right: 0;\n"], ["\n  position: absolute;\n  top: 0;\n  left: 0;\n  right: 0;\n"])));
var EmptyText = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  margin-left: 4px;\n  margin-right: 4px;\n  height: 68px;\n  color: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  margin-left: 4px;\n  margin-right: 4px;\n  height: 68px;\n  color: ", ";\n"])), function (p) { return p.theme.gray500; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=noEvents.jsx.map