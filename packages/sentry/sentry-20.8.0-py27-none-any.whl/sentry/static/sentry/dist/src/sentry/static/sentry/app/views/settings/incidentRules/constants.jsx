var _a;
import { __assign } from "tslib";
import { AlertRuleThresholdType, Dataset, } from 'app/views/settings/incidentRules/types';
export var DEFAULT_AGGREGATE = 'count()';
export var DATASET_EVENT_TYPE_FILTERS = (_a = {},
    _a[Dataset.ERRORS] = 'event.type:error',
    _a[Dataset.TRANSACTIONS] = 'event.type:transaction',
    _a);
/**
 * Allowed error aggregations for alerts
 */
export var errorFieldConfig = {
    aggregations: ['count', 'count_unique'],
    fields: ['user'],
};
/**
 * Allowed transaction aggregations for alerts
 */
export var transactionFieldConfig = {
    aggregations: [
        'avg',
        'percentile',
        'failure_rate',
        'apdex',
        'count',
        'p50',
        'p75',
        'p95',
        'p99',
        'p100',
    ],
    fields: ['transaction.duration'],
};
export function createDefaultTrigger(label) {
    return {
        label: label,
        alertThreshold: '',
        actions: [],
    };
}
export function createDefaultRule() {
    return {
        dataset: Dataset.ERRORS,
        aggregate: DEFAULT_AGGREGATE,
        query: '',
        timeWindow: 1,
        triggers: [createDefaultTrigger('critical'), createDefaultTrigger('warning')],
        projects: [],
        environment: null,
        resolveThreshold: '',
        thresholdType: AlertRuleThresholdType.ABOVE,
    };
}
/**
 * Create an unsaved alert from a discover EventView object
 */
export function createRuleFromEventView(eventView) {
    return __assign(__assign({}, createDefaultRule()), { dataset: eventView.query.includes(DATASET_EVENT_TYPE_FILTERS[Dataset.TRANSACTIONS])
            ? Dataset.TRANSACTIONS
            : Dataset.ERRORS, query: eventView.query
            .slice()
            .replace(/event\.type:(transaction|error)/, '')
            .trim(), aggregate: eventView.getYAxis(), environment: eventView.environment.length ? eventView.environment[0] : null });
}
//# sourceMappingURL=constants.jsx.map