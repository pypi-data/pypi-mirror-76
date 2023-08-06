import { __assign, __rest } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import StackedBarChart from 'app/components/stackedBarChart';
var BarChart = function (_a) {
    var _b = _a.points, points = _b === void 0 ? [] : _b, rest = __rest(_a, ["points"]);
    var formattedPoints = points.map(function (point) { return ({ x: point.x, y: [point.y] }); });
    var props = __assign(__assign({}, rest), { points: formattedPoints });
    return <StackedBarChart {...props}/>;
};
BarChart.propTypes = {
    points: PropTypes.arrayOf(PropTypes.shape({
        x: PropTypes.number.isRequired,
        y: PropTypes.number.isRequired,
        label: PropTypes.string,
    })),
    interval: PropTypes.string,
    height: PropTypes.number,
    width: PropTypes.number,
    label: PropTypes.string,
    markers: PropTypes.arrayOf(PropTypes.shape({
        x: PropTypes.number.isRequired,
        label: PropTypes.string,
    })),
};
export default BarChart;
//# sourceMappingURL=barChart.jsx.map