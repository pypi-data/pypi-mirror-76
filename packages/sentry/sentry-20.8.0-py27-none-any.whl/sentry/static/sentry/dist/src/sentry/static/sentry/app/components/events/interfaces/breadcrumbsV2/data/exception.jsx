import React from 'react';
import omit from 'lodash/omit';
import { getMeta } from 'app/components/events/meta/metaProxy';
import { defined } from 'app/utils';
import Highlight from 'app/components/highlight';
import getBreadcrumbCustomRendererValue from '../../breadcrumbs/getBreadcrumbCustomRendererValue';
import Summary from './summary';
var Exception = function (_a) {
    var breadcrumb = _a.breadcrumb, searchTerm = _a.searchTerm;
    var data = breadcrumb.data;
    var dataValue = data === null || data === void 0 ? void 0 : data.value;
    return (<Summary kvData={omit(data, ['type', 'value'])} searchTerm={searchTerm}>
      {(data === null || data === void 0 ? void 0 : data.type) &&
        getBreadcrumbCustomRendererValue({
            value: (<strong>
              <Highlight text={searchTerm}>{data.type + ": "}</Highlight>
            </strong>),
            meta: getMeta(data, 'type'),
        })}
      {defined(dataValue) &&
        getBreadcrumbCustomRendererValue({
            value: (<Highlight text={searchTerm}>
              {(breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.message) ? dataValue + ". " : dataValue}
            </Highlight>),
            meta: getMeta(data, 'value'),
        })}
      {(breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.message) &&
        getBreadcrumbCustomRendererValue({
            value: <Highlight text={searchTerm}>{breadcrumb.message}</Highlight>,
            meta: getMeta(breadcrumb, 'message'),
        })}
    </Summary>);
};
export default Exception;
//# sourceMappingURL=exception.jsx.map