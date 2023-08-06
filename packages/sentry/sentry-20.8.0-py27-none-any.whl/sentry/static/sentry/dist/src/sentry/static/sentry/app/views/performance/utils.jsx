import { __assign } from "tslib";
import getCurrentSentryReactTransaction from 'app/utils/getCurrentSentryReactTransaction';
import { statsPeriodToDays } from 'app/utils/dates';
export function getPerformanceLandingUrl(organization) {
    return "/organizations/" + organization.slug + "/performance/";
}
export function getTransactionDetailsUrl(organization, eventSlug, transaction, query) {
    return {
        pathname: "/organizations/" + organization.slug + "/performance/" + eventSlug + "/",
        query: __assign(__assign({}, query), { transaction: transaction }),
    };
}
export function getTransactionComparisonUrl(_a) {
    var organization = _a.organization, baselineEventSlug = _a.baselineEventSlug, regressionEventSlug = _a.regressionEventSlug, transaction = _a.transaction, query = _a.query;
    return {
        pathname: "/organizations/" + organization.slug + "/performance/compare/" + baselineEventSlug + "/" + regressionEventSlug + "/",
        query: __assign(__assign({}, query), { transaction: transaction }),
    };
}
export function addRoutePerformanceContext(selection) {
    var transaction = getCurrentSentryReactTransaction();
    var days = statsPeriodToDays(selection.datetime.period, selection.datetime.start, selection.datetime.end);
    var seconds = Math.floor(days * 86400);
    transaction === null || transaction === void 0 ? void 0 : transaction.setTag('statsPeriod', seconds.toString());
}
//# sourceMappingURL=utils.jsx.map