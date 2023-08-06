import { t } from 'app/locale';
export var DEFAULT_EVENT_VIEW = {
    id: undefined,
    name: t('All Events'),
    query: '',
    projects: [],
    fields: ['title', 'event.type', 'project', 'user', 'timestamp'],
    orderby: '-timestamp',
    version: 2,
    range: '24h',
};
export var TRANSACTION_VIEWS = [
    {
        id: undefined,
        name: t('Transactions by Volume'),
        fields: [
            'transaction',
            'project',
            'count()',
            'avg(transaction.duration)',
            'p75()',
            'p95()',
        ],
        orderby: '-count',
        query: 'event.type:transaction',
        projects: [],
        version: 2,
        range: '24h',
    },
];
export var ALL_VIEWS = [
    DEFAULT_EVENT_VIEW,
    {
        id: undefined,
        name: t('Errors by Title'),
        fields: ['title', 'count()', 'count_unique(user)', 'project'],
        orderby: '-count',
        query: 'event.type:error',
        projects: [],
        version: 2,
        range: '24h',
        display: 'top5',
    },
    {
        id: undefined,
        name: t('Errors by URL'),
        fields: ['url', 'count()', 'count_unique(issue)'],
        orderby: '-count',
        query: 'event.type:error has:url',
        projects: [],
        version: 2,
        range: '24h',
        display: 'top5',
    },
];
//# sourceMappingURL=data.jsx.map