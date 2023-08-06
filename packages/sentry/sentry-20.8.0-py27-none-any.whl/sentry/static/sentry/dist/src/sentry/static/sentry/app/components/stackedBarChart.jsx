import { __assign, __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';
import moment from 'moment-timezone';
import isEqual from 'lodash/isEqual';
import styled from '@emotion/styled';
import Tooltip from 'app/components/tooltip';
import Count from 'app/components/count';
import { use24Hours, getTimeFormat } from 'app/utils/dates';
import theme from 'app/utils/theme';
import { formatFloat } from 'app/utils/formatters';
var StackedBarChart = /** @class */ (function (_super) {
    __extends(StackedBarChart, _super);
    function StackedBarChart(props) {
        var _a;
        var _this = _super.call(this, props) || this;
        _this.getInterval = function (series) {
            // TODO(dcramer): not guaranteed correct
            return series.length && series[0].data.length > 1
                ? series[0].data[1].x - series[0].data[0].x
                : null;
        };
        _this.pointsToSeries = function (points) {
            var series = [];
            points.forEach(function (p, _pIdx) {
                p.y.forEach(function (y, yIdx) {
                    if (!series[yIdx]) {
                        series[yIdx] = { data: [] };
                    }
                    series[yIdx].data.push({ x: p.x, y: y });
                });
            });
            return series;
        };
        _this.pointIndex = function (series) {
            var points = {};
            series.forEach(function (s) {
                s.data.forEach(function (p) {
                    if (!points[p.x]) {
                        points[p.x] = { y: [], x: p.x };
                    }
                    points[p.x].y.push(p.y);
                });
            });
            return points;
        };
        _this.renderTooltip = function (point, _pointIdx) {
            var timeLabel = _this.getTimeLabel(point);
            var totalY = point.y.reduce(function (a, b) { return a + b; });
            return (<React.Fragment>
        <div style={{ width: '130px' }}>
          <div className="time-label">{timeLabel}</div>
        </div>
        {_this.props.label && (<div className="value-label">
            {totalY.toLocaleString()} {_this.props.label}
          </div>)}
        {point.y.map(function (y, i) {
                var s = _this.state.series[i];
                if (s.label) {
                    return (<div>
                <span style={{ color: s.color }}>{s.label}:</span>{' '}
                {(y || 0).toLocaleString()}
              </div>);
                }
                return null;
            })}
      </React.Fragment>);
        };
        // massage points
        var series = props.series;
        if ((_a = props.points) === null || _a === void 0 ? void 0 : _a.length) {
            if (series === null || series === void 0 ? void 0 : series.length) {
                throw new Error('Only one of [points|series] should be specified.');
            }
            series = _this.pointsToSeries(props.points);
        }
        _this.state = {
            series: series,
            pointIndex: _this.pointIndex(series),
            interval: _this.getInterval(series),
        };
        return _this;
    }
    StackedBarChart.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        if (nextProps.points || nextProps.series) {
            var series = nextProps.series;
            if (nextProps.points.length) {
                if (series.length) {
                    throw new Error('Only one of [points|series] should be specified.');
                }
                series = this.pointsToSeries(nextProps.points);
            }
            this.setState({
                series: series,
                pointIndex: this.pointIndex(series),
                interval: this.getInterval(series),
            });
        }
    };
    StackedBarChart.prototype.shouldComponentUpdate = function (nextProps) {
        return !isEqual(this.props, nextProps);
    };
    StackedBarChart.prototype.timeLabelAsHour = function (point) {
        var timeMoment = moment(point.x * 1000);
        var nextMoment = timeMoment.clone().add(59, 'minute');
        var timeFormat = getTimeFormat();
        return (<span>
        {timeMoment.format('LL')}
        <br />
        {timeMoment.format(timeFormat)}
        &#8594;
        {nextMoment.format(timeFormat)}
      </span>);
    };
    StackedBarChart.prototype.timeLabelAsDay = function (point) {
        var timeMoment = moment(point.x * 1000);
        return <span>{timeMoment.format('LL')}</span>;
    };
    StackedBarChart.prototype.timeLabelAsRange = function (interval, point) {
        var timeMoment = moment(point.x * 1000);
        var nextMoment = timeMoment.clone().add(interval - 1, 'second');
        var format = "MMM Do, " + getTimeFormat();
        // e.g. Aug 23rd, 12:50 pm
        return (<span>
        {timeMoment.format(format)}
        &#8594
        {nextMoment.format(format)}
      </span>);
    };
    StackedBarChart.prototype.timeLabelAsFull = function (point) {
        var timeMoment = moment(point.x * 1000);
        var format = use24Hours() ? 'MMM D, YYYY HH:mm' : 'lll';
        return timeMoment.format(format);
    };
    StackedBarChart.prototype.getTimeLabel = function (point) {
        switch (this.state.interval) {
            case 3600:
                return this.timeLabelAsHour(point);
            case 86400:
                return this.timeLabelAsDay(point);
            case null:
                return this.timeLabelAsFull(point);
            default:
                return this.timeLabelAsRange(this.state.interval, point);
        }
    };
    StackedBarChart.prototype.maxPointValue = function () {
        return Math.max(10, this.state.series
            .map(function (s) { return Math.max.apply(Math, __spread(s.data.map(function (p) { return p.y; }))); })
            .reduce(function (a, b) { return a + b; }, 0));
    };
    StackedBarChart.prototype.renderMarker = function (marker, index, pointWidth) {
        var timeLabel = this.timeLabelAsFull(marker);
        var title = (<div style={{ width: '130px' }}>
        {marker.label}
        <br />
        {timeLabel}
      </div>);
        // example key: m-last-seen-22811123, m-first-seen-228191
        var key = ['m', marker.className, marker.x].join('-');
        var markerOffset = marker.offset || 0;
        return (<CircleSvg key={key} left={index * pointWidth} offset={markerOffset || 0} viewBox="0 0 10 10" size={10}>
        <Tooltip title={title} position="bottom">
          <circle data-test-id="chart-column" r="4" cx="50%" cy="50%" fill={marker.fill || theme.gray500} stroke="#fff" strokeWidth="2">
            {marker.label}
          </circle>
        </Tooltip>
      </CircleSvg>);
    };
    StackedBarChart.prototype.getMinHeight = function (index) {
        var minHeights = this.props.minHeights;
        return minHeights && (minHeights[index] || minHeights[index] === 0)
            ? minHeights[index]
            : 1;
    };
    StackedBarChart.prototype.renderChartColumn = function (point, maxval, pointWidth, index, _totalPoints) {
        var _this = this;
        var totalY = point.y.reduce(function (a, b) { return a + b; });
        var totalPct = totalY / maxval;
        // we leave a little extra space for bars with min-heights.
        var maxPercentage = 99;
        var prevPct = 0;
        var pts = point.y.map(function (y, i) {
            var pct = Math.max(totalY && formatFloat((y / totalY) * totalPct * maxPercentage, 2), _this.getMinHeight(i));
            var pt = (<rect key={i} x={index * pointWidth + '%'} y={100.0 - pct - prevPct + '%'} width={pointWidth - _this.props.gap + '%'} data-test-id="chart-column" height={pct + '%'} fill={_this.state.series[i].color} className={classNames(_this.props.barClasses[i], 'barchart-rect')}>
          {y}
        </rect>);
            prevPct += pct;
            return pt;
        });
        var pointIdx = point.x;
        var tooltipFunc = this.props.tooltip || this.renderTooltip;
        return (<Tooltip title={tooltipFunc(this.state.pointIndex[pointIdx], pointIdx, this)} position="bottom" key={point.x}>
        <g>
          <rect x={index * pointWidth - this.props.gap + '%'} width={pointWidth + this.props.gap + '%'} height="100%" opacity="0"/>
          {pts}
        </g>
      </Tooltip>);
    };
    StackedBarChart.prototype.renderChart = function () {
        var _this = this;
        var _a = this.state, pointIndex = _a.pointIndex, series = _a.series;
        var totalPoints = Math.max.apply(Math, __spread(series.map(function (s) { return s.data.length; })));
        // we expand the graph just a hair beyond 100% prevent a subtle white line on the edge
        var nudge = 0.1;
        var pointWidth = formatFloat((100.0 + this.props.gap + nudge) / totalPoints, 2);
        var maxval = this.maxPointValue();
        var markers = this.props.markers.slice();
        // group points, then resort
        var points = Object.keys(pointIndex)
            .map(function (k) {
            var p = pointIndex[k];
            return { x: p.x, y: p.y };
        })
            .sort(function (a, b) { return a.x - b.x; });
        markers.sort(function (a, b) { return a.x - b.x; });
        var children = [];
        var markerChildren = [];
        points.forEach(function (point, index) {
            while (markers.length && markers[0].x <= point.x) {
                markerChildren.push(_this.renderMarker(markers.shift(), index, pointWidth));
            }
            children.push(_this.renderChartColumn(point, maxval, pointWidth, index, totalPoints));
        });
        // in bizarre case where markers never got rendered, render them last
        // NOTE: should this ever happen?
        markers.forEach(function (marker) {
            markerChildren.push(_this.renderMarker(marker, points.length, pointWidth));
        });
        return (<SvgContainer>
        <StyledSvg viewBox="0 0 100 400" preserveAspectRatio="none" overflow="visible">
          {children}
        </StyledSvg>
        {markerChildren.length ? markerChildren : null}
      </SvgContainer>);
    };
    StackedBarChart.prototype.render = function () {
        var _a = this.props, className = _a.className, style = _a.style, height = _a.height, width = _a.width;
        var figureClass = [className, 'barchart'].join(' ');
        var maxval = this.maxPointValue();
        return (<StyledFigure className={figureClass} style={__assign({ height: height, width: width }, style)}>
        <span className="max-y">
          <Count value={maxval}/>
        </span>
        <span className="min-y">0</span>
        {this.renderChart()}
      </StyledFigure>);
    };
    StackedBarChart.propTypes = {
        // TODO(dcramer): DEPRECATED, use series instead
        points: PropTypes.arrayOf(PropTypes.shape({
            x: PropTypes.number.isRequired,
            y: PropTypes.array.isRequired,
            label: PropTypes.string,
        })),
        series: PropTypes.arrayOf(PropTypes.shape({
            data: PropTypes.arrayOf(PropTypes.shape({
                x: PropTypes.number.isRequired,
                y: PropTypes.number,
            })),
            label: PropTypes.string,
        })),
        height: PropTypes.number,
        width: PropTypes.number,
        label: PropTypes.string,
        markers: PropTypes.arrayOf(PropTypes.shape({
            x: PropTypes.number.isRequired,
            label: PropTypes.string,
        })),
        tooltip: PropTypes.func,
        barClasses: PropTypes.array,
        /* Some bars need to be visible and interactable even if they are
        empty. Use minHeights for that. Units are in svg points */
        minHeights: PropTypes.arrayOf(PropTypes.number),
        /* the amount of space between bars. Also represents an svg point */
        gap: PropTypes.number,
    };
    StackedBarChart.defaultProps = {
        label: '',
        points: [],
        series: [],
        markers: [],
        barClasses: ['chart-bar'],
        gap: 0.5,
        className: 'sparkline',
    };
    return StackedBarChart;
}(React.Component));
var StyledSvg = styled('svg')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  width: 100%;\n  height: 100%;\n  /* currently, min-heights are not calculated into maximum bar height, so\n  we need the svg to allow elements to exceed the container. This overrides\n  the global overflow: hidden declaration. Eventually, we should factor minimum\n  bar heights into the overall chart height and remove this */\n  overflow: visible !important;\n"], ["\n  width: 100%;\n  height: 100%;\n  /* currently, min-heights are not calculated into maximum bar height, so\n  we need the svg to allow elements to exceed the container. This overrides\n  the global overflow: hidden declaration. Eventually, we should factor minimum\n  bar heights into the overall chart height and remove this */\n  overflow: visible !important;\n"])));
var StyledFigure = styled('figure')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: block;\n  position: relative;\n"], ["\n  display: block;\n  position: relative;\n"])));
var SvgContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: relative;\n  width: 100%;\n  height: 100%;\n"], ["\n  position: relative;\n  width: 100%;\n  height: 100%;\n"])));
var CircleSvg = styled('svg')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  width: ", "px;\n  height: ", "px;\n  position: absolute;\n  bottom: -", "px;\n  transform: translate(", "px, 0);\n  left: ", "%;\n\n  &:hover circle {\n    fill: ", ";\n  }\n"], ["\n  width: ", "px;\n  height: ", "px;\n  position: absolute;\n  bottom: -", "px;\n  transform: translate(", "px, 0);\n  left: ", "%;\n\n  &:hover circle {\n    fill: ", ";\n  }\n"])), function (p) { return p.size; }, function (p) { return p.size; }, function (p) { return p.size / 2; }, function (p) { return (p.offset || 0) - p.size / 2; }, function (p) { return p.left; }, function (p) { return p.theme.purple400; });
export default StackedBarChart;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=stackedBarChart.jsx.map