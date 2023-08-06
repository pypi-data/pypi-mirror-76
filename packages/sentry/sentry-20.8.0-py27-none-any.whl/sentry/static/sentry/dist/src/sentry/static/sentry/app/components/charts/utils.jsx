import moment from 'moment';
import { DEFAULT_STATS_PERIOD } from 'app/constants';
import { parsePeriodToHours } from 'app/utils/dates';
import { escape } from 'app/utils';
var DEFAULT_TRUNCATE_LENGTH = 80;
// In minutes
var THIRTY_DAYS = 43200;
var TWENTY_FOUR_HOURS = 1440;
var ONE_HOUR = 60;
export function truncationFormatter(value, truncate) {
    if (!truncate) {
        return escape(value);
    }
    var truncationLength = truncate && typeof truncate === 'number' ? truncate : DEFAULT_TRUNCATE_LENGTH;
    var truncated = value.length > truncationLength ? value.substring(0, truncationLength) + '…' : value;
    return escape(truncated);
}
/**
 * Use a shorter interval if the time difference is <= 24 hours.
 */
export function useShortInterval(datetimeObj) {
    var diffInMinutes = getDiffInMinutes(datetimeObj);
    return diffInMinutes <= TWENTY_FOUR_HOURS;
}
export function getInterval(datetimeObj, highFidelity) {
    if (highFidelity === void 0) { highFidelity = false; }
    var diffInMinutes = getDiffInMinutes(datetimeObj);
    if (diffInMinutes >= THIRTY_DAYS) {
        // Greater than or equal to 30 days
        if (highFidelity) {
            return '1h';
        }
        else {
            return '24h';
        }
    }
    if (diffInMinutes > TWENTY_FOUR_HOURS) {
        // Greater than 24 hours
        if (highFidelity) {
            return '30m';
        }
        else {
            return '24h';
        }
    }
    if (diffInMinutes <= ONE_HOUR) {
        // Less than or equal to 1 hour
        if (highFidelity) {
            return '1m';
        }
        else {
            return '5m';
        }
    }
    // Between 1 hour and 24 hours
    if (highFidelity) {
        return '5m';
    }
    else {
        return '15m';
    }
}
export function getDiffInMinutes(datetimeObj) {
    var period = datetimeObj.period, start = datetimeObj.start, end = datetimeObj.end;
    if (start && end) {
        return moment(end).diff(start, 'minutes');
    }
    return (parsePeriodToHours(typeof period === 'string' ? period : DEFAULT_STATS_PERIOD) * 60);
}
// Max period (in hours) before we can no long include previous period
var MAX_PERIOD_HOURS_INCLUDE_PREVIOUS = 45 * 24;
export function canIncludePreviousPeriod(includePrevious, period) {
    if (!includePrevious) {
        return false;
    }
    if (period && parsePeriodToHours(period) > MAX_PERIOD_HOURS_INCLUDE_PREVIOUS) {
        return false;
    }
    // otherwise true
    return !!includePrevious;
}
//# sourceMappingURL=utils.jsx.map