import { __makeTemplateObject } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import styled from '@emotion/styled';
import BarChart from 'app/components/barChart';
var Chart = function (_a) {
    var _b = _a.stats, stats = _b === void 0 ? [] : _b;
    var data = stats.map(function (d) { return ({ x: d[0], y: d[1] }); });
    return <StyledBarChart points={data} label="events" height={60} gap={1.5}/>;
};
Chart.propTypes = {
    stats: PropTypes.array,
};
export default Chart;
var StyledBarChart = styled(BarChart)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  a {\n    &:not(:first-child) {\n      border-left: 2px solid transparent;\n    }\n    &:not(:last-child) {\n      border-right: 2px solid transparent;\n    }\n    > span {\n      left: 0;\n      right: 0;\n    }\n  }\n"], ["\n  a {\n    &:not(:first-child) {\n      border-left: 2px solid transparent;\n    }\n    &:not(:last-child) {\n      border-right: 2px solid transparent;\n    }\n    > span {\n      left: 0;\n      right: 0;\n    }\n  }\n"])));
var templateObject_1;
//# sourceMappingURL=chart.jsx.map