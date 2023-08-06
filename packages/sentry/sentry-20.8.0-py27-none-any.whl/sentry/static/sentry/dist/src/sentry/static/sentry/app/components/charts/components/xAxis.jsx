import { __assign, __rest } from "tslib";
import { getFormattedDate, getTimeFormat } from 'app/utils/dates';
import theme from 'app/utils/theme';
import { truncationFormatter, useShortInterval } from '../utils';
export default function XAxis(_a) {
    if (_a === void 0) { _a = {}; }
    var isGroupedByDate = _a.isGroupedByDate, useShortDate = _a.useShortDate, axisLabel = _a.axisLabel, axisTick = _a.axisTick, axisLine = _a.axisLine, start = _a.start, end = _a.end, period = _a.period, utc = _a.utc, props = __rest(_a, ["isGroupedByDate", "useShortDate", "axisLabel", "axisTick", "axisLine", "start", "end", "period", "utc"]);
    var axisLabelFormatter = function (value, index) {
        if (isGroupedByDate) {
            var timeFormat = getTimeFormat();
            var dateFormat = useShortDate ? 'MMM Do' : "MMM D " + timeFormat;
            var firstItem = index === 0;
            var format = useShortInterval({ start: start, end: end, period: period }) && !firstItem ? timeFormat : dateFormat;
            return getFormattedDate(value, format, { local: !utc });
        }
        else if (props.truncate) {
            return truncationFormatter(value, props.truncate);
        }
        else {
            return undefined;
        }
    };
    return __assign({ type: isGroupedByDate ? 'time' : 'category', boundaryGap: false, axisLine: {
            lineStyle: __assign({ color: theme.gray400 }, (axisLine || {})),
        }, axisTick: __assign({ lineStyle: {
                color: theme.gray400,
            } }, (axisTick || {})), splitLine: {
            show: false,
        }, axisLabel: __assign({ margin: 12, 
            // This was default with ChartZoom, we are making it default for all charts now
            // Otherwise the xAxis can look congested when there is always a min/max label
            showMaxLabel: false, showMinLabel: false, formatter: axisLabelFormatter }, (axisLabel || {})), axisPointer: {
            show: true,
            type: 'line',
            label: {
                show: false,
            },
            lineStyle: {
                width: 0.5,
            },
        } }, props);
}
//# sourceMappingURL=xAxis.jsx.map