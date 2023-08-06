import { __assign } from "tslib";
import theme from 'app/utils/theme';
export default function YAxis(props) {
    if (props === void 0) { props = {}; }
    return __assign({ axisLine: {
            show: false,
        }, axisTick: {
            show: false,
        }, axisLabel: {
            color: theme.gray400,
        }, splitLine: {
            lineStyle: {
                color: theme.borderLighter,
            },
        } }, props);
}
//# sourceMappingURL=yAxis.jsx.map