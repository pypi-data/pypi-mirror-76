import { __assign, __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import pick from 'lodash/pick';
import { t, tct } from 'app/locale';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import Button from 'app/components/button';
import DiscoverButton from 'app/components/discoverButton';
import GroupList from 'app/components/issues/groupList';
import space from 'app/styles/space';
import { Panel, PanelBody } from 'app/components/panels';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import { DEFAULT_RELATIVE_PERIODS } from 'app/constants';
import Feature from 'app/components/acl/feature';
import { URL_PARAM } from 'app/constants/globalSelectionHeader';
import ButtonBar from 'app/components/buttonBar';
import { stringifyQueryObject, QueryResults } from 'app/utils/tokenizeSearch';
import { getReleaseEventView } from './chart/utils';
var IssuesType;
(function (IssuesType) {
    IssuesType["NEW"] = "new";
    IssuesType["RESOLVED"] = "resolved";
    IssuesType["ALL"] = "all";
})(IssuesType || (IssuesType = {}));
var Issues = /** @class */ (function (_super) {
    __extends(Issues, _super);
    function Issues() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            issuesType: IssuesType.NEW,
        };
        _this.handleIssuesTypeSelection = function (issuesType) {
            _this.setState({ issuesType: issuesType });
        };
        _this.renderEmptyMessage = function () {
            var selection = _this.props.selection;
            var issuesType = _this.state.issuesType;
            var selectedTimePeriod = DEFAULT_RELATIVE_PERIODS[selection.datetime.period];
            var displayedPeriod = selectedTimePeriod
                ? selectedTimePeriod.toLowerCase()
                : t('given timeframe');
            return (<Panel>
        <PanelBody>
          <EmptyStateWarning small withIcon={false}>
            {issuesType === IssuesType.NEW &&
                tct('No new issues in this release for the [timePeriod].', {
                    timePeriod: displayedPeriod,
                })}
            {issuesType === IssuesType.RESOLVED &&
                t('No resolved issues in this release.')}
            {issuesType === IssuesType.ALL &&
                tct('No issues in this release for the [timePeriod].', {
                    timePeriod: displayedPeriod,
                })}
          </EmptyStateWarning>
        </PanelBody>
      </Panel>);
        };
        return _this;
    }
    Issues.prototype.getDiscoverUrl = function () {
        var _a = this.props, version = _a.version, orgId = _a.orgId, selection = _a.selection;
        var discoverView = getReleaseEventView(selection, version);
        return discoverView.getResultsViewUrlTarget(orgId);
    };
    Issues.prototype.getIssuesUrl = function () {
        var _a = this.props, version = _a.version, orgId = _a.orgId;
        var issuesType = this.state.issuesType;
        var queryParams = this.getIssuesEndpoint().queryParams;
        var query = new QueryResults([]);
        if (issuesType === IssuesType.NEW) {
            query.setTag('firstRelease', [version]);
        }
        else {
            query.setTag('release', [version]);
        }
        return {
            pathname: "/organizations/" + orgId + "/issues/",
            query: __assign(__assign({}, queryParams), { query: stringifyQueryObject(query) }),
        };
    };
    Issues.prototype.getIssuesEndpoint = function () {
        var _a = this.props, version = _a.version, orgId = _a.orgId, location = _a.location;
        var issuesType = this.state.issuesType;
        var queryParams = __assign(__assign({}, pick(location.query, __spread(Object.values(URL_PARAM), ['cursor']))), { limit: 50, sort: 'new' });
        switch (issuesType) {
            case IssuesType.ALL:
                return {
                    path: "/organizations/" + orgId + "/issues/",
                    queryParams: __assign(__assign({}, queryParams), { query: "release:\"" + version + "\"" }),
                };
            case IssuesType.RESOLVED:
                return {
                    path: "/organizations/" + orgId + "/releases/" + version + "/resolved/",
                    queryParams: __assign(__assign({}, queryParams), { query: '' }),
                };
            case IssuesType.NEW:
            default:
                return {
                    path: "/organizations/" + orgId + "/issues/",
                    queryParams: __assign(__assign({}, queryParams), { query: "first-release:\"" + version + "\"" }),
                };
        }
    };
    Issues.prototype.render = function () {
        var _this = this;
        var _a;
        var issuesType = this.state.issuesType;
        var orgId = this.props.orgId;
        var _b = this.getIssuesEndpoint(), path = _b.path, queryParams = _b.queryParams;
        var issuesTypes = [
            { value: 'new', label: t('New Issues') },
            { value: 'resolved', label: t('Resolved Issues') },
            { value: 'all', label: t('All Issues') },
        ];
        return (<React.Fragment>
        <ControlsWrapper>
          <DropdownControl buttonProps={{ prefix: t('Filter'), size: 'small' }} label={(_a = issuesTypes.find(function (i) { return i.value === issuesType; })) === null || _a === void 0 ? void 0 : _a.label}>
            {issuesTypes.map(function (_a) {
            var value = _a.value, label = _a.label;
            return (<StyledDropdownItem key={value} onSelect={_this.handleIssuesTypeSelection} eventKey={value} isActive={value === issuesType}>
                {label}
              </StyledDropdownItem>);
        })}
          </DropdownControl>

          <OpenInButtonBar gap={1}>
            <Feature features={['discover-basic']}>
              <DiscoverButton to={this.getDiscoverUrl()} size="small">
                {t('Open in Discover')}
              </DiscoverButton>
            </Feature>

            <Button to={this.getIssuesUrl()} size="small">
              {t('Open in Issues')}
            </Button>
          </OpenInButtonBar>
        </ControlsWrapper>
        <TableWrapper data-test-id="release-wrapper">
          <GroupList orgId={orgId} endpointPath={path} queryParams={queryParams} query="" canSelectGroups={false} withChart={false} renderEmptyMessage={this.renderEmptyMessage}/>
        </TableWrapper>
      </React.Fragment>);
    };
    return Issues;
}(React.Component));
var ControlsWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n  @media (max-width: ", ") {\n    display: block;\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n  @media (max-width: ", ") {\n    display: block;\n  }\n"])), space(1), function (p) { return p.theme.breakpoints[0]; });
var OpenInButtonBar = styled(ButtonBar)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  @media (max-width: ", ") {\n    margin-top: ", ";\n  }\n"], ["\n  @media (max-width: ", ") {\n    margin-top: ", ";\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, space(1));
var StyledDropdownItem = styled(DropdownItem)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  white-space: nowrap;\n"], ["\n  white-space: nowrap;\n"])));
var TableWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  ", " {\n    /* smaller space between table and pagination */\n    margin-bottom: -", ";\n  }\n"], ["\n  margin-bottom: ", ";\n  ", " {\n    /* smaller space between table and pagination */\n    margin-bottom: -", ";\n  }\n"])), space(4), Panel, space(1));
export default Issues;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=issues.jsx.map