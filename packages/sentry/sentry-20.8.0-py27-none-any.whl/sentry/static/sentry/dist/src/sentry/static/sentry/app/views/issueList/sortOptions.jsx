import { __makeTemplateObject } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import styled from '@emotion/styled';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import { t } from 'app/locale';
import space from 'app/styles/space';
var IssueListSortOptions = function (_a) {
    var onSelect = _a.onSelect, sort = _a.sort;
    var sortKey = sort || 'date';
    var getSortLabel = function (key) {
        switch (key) {
            case 'new':
                return t('First Seen');
            case 'priority':
                return t('Priority');
            case 'freq':
                return t('Frequency');
            case 'user':
                return t('Users');
            case 'date':
            default:
                return t('Last Seen');
        }
    };
    var getMenuItem = function (key) { return (<DropdownItem onSelect={onSelect} eventKey={key} isActive={sortKey === key}>
      {getSortLabel(key)}
    </DropdownItem>); };
    return (<Container>
      <DropdownControl buttonProps={{ prefix: t('Sort by') }} label={getSortLabel(sortKey)}>
        {getMenuItem('priority')}
        {getMenuItem('date')}
        {getMenuItem('new')}
        {getMenuItem('freq')}
        {getMenuItem('user')}
      </DropdownControl>
    </Container>);
};
IssueListSortOptions.propTypes = {
    sort: PropTypes.string.isRequired,
    onSelect: PropTypes.func.isRequired,
};
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(0.5));
export default IssueListSortOptions;
var templateObject_1;
//# sourceMappingURL=sortOptions.jsx.map