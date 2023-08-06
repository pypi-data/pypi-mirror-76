import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import omit from 'lodash/omit';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import space from 'app/styles/space';
import { generateQueryWithTag } from 'app/utils';
import * as Layout from 'app/components/layouts/thirds';
import Tags from 'app/views/eventsV2/tags';
import SearchBar from 'app/views/events/searchBar';
import { decodeScalar } from 'app/utils/queryString';
import CreateAlertButton from 'app/components/createAlertButton';
import withProjects from 'app/utils/withProjects';
import ButtonBar from 'app/components/buttonBar';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import TransactionList from './transactionList';
import UserStats from './userStats';
import KeyTransactionButton from './keyTransactionButton';
import TransactionSummaryCharts from './charts';
import RelatedIssues from './relatedIssues';
import SidebarCharts from './sidebarCharts';
import Breadcrumb from '../breadcrumb';
var SummaryContent = /** @class */ (function (_super) {
    __extends(SummaryContent, _super);
    function SummaryContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            incompatibleAlertNotice: null,
        };
        _this.handleSearch = function (query) {
            var location = _this.props.location;
            var queryParams = getParams(__assign(__assign({}, (location.query || {})), { query: query }));
            // do not propagate pagination when making a new search
            var searchQueryParams = omit(queryParams, 'cursor');
            browserHistory.push({
                pathname: location.pathname,
                query: searchQueryParams,
            });
        };
        _this.generateTagUrl = function (key, value) {
            var location = _this.props.location;
            var query = generateQueryWithTag(location.query, { key: key, value: value });
            return __assign(__assign({}, location), { query: query });
        };
        _this.handleIncompatibleQuery = function (incompatibleAlertNoticeFn, errors) {
            _this.trackAlertClick(errors);
            var incompatibleAlertNotice = incompatibleAlertNoticeFn(function () {
                return _this.setState({ incompatibleAlertNotice: null });
            });
            _this.setState({ incompatibleAlertNotice: incompatibleAlertNotice });
        };
        _this.handleCreateAlertSuccess = function () {
            _this.trackAlertClick();
        };
        return _this;
    }
    SummaryContent.prototype.trackAlertClick = function (errors) {
        var organization = this.props.organization;
        trackAnalyticsEvent({
            eventKey: 'performance_views.summary.create_alert_clicked',
            eventName: 'Performance Views: Create alert clicked',
            organization_id: organization.id,
            status: errors ? 'error' : 'success',
            errors: errors,
            url: window.location.href,
        });
    };
    SummaryContent.prototype.renderCreateAlertButton = function () {
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, projects = _a.projects;
        return (<CreateAlertButton eventView={eventView} organization={organization} projects={projects} onIncompatibleQuery={this.handleIncompatibleQuery} onSuccess={this.handleCreateAlertSuccess} referrer="performance"/>);
    };
    SummaryContent.prototype.renderKeyTransactionButton = function () {
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, transactionName = _a.transactionName;
        return (<KeyTransactionButton transactionName={transactionName} eventView={eventView} organization={organization}/>);
    };
    SummaryContent.prototype.render = function () {
        var _a = this.props, transactionName = _a.transactionName, location = _a.location, eventView = _a.eventView, organization = _a.organization, totalValues = _a.totalValues;
        var incompatibleAlertNotice = this.state.incompatibleAlertNotice;
        var query = decodeScalar(location.query.query) || '';
        return (<React.Fragment>
        <Layout.Header>
          <Layout.HeaderContent>
            <Breadcrumb organization={organization} location={location} transactionName={transactionName}/>
            <Layout.Title>{transactionName}</Layout.Title>
          </Layout.HeaderContent>
          <Layout.HeaderActions>
            <ButtonBar gap={1}>
              {this.renderCreateAlertButton()}
              {this.renderKeyTransactionButton()}
            </ButtonBar>
          </Layout.HeaderActions>
        </Layout.Header>
        <Layout.Body>
          {incompatibleAlertNotice && (<Layout.Main fullWidth>{incompatibleAlertNotice}</Layout.Main>)}
          <Layout.Main>
            <StyledSearchBar organization={organization} projectIds={eventView.project} query={query} fields={eventView.fields} onSearch={this.handleSearch}/>
            <TransactionSummaryCharts organization={organization} location={location} eventView={eventView} totalValues={totalValues}/>
            <TransactionList organization={organization} transactionName={transactionName} location={location} eventView={eventView}/>
            <RelatedIssues organization={organization} location={location} transaction={transactionName} start={eventView.start} end={eventView.end} statsPeriod={eventView.statsPeriod}/>
          </Layout.Main>
          <Layout.Side>
            <UserStats organization={organization} location={location} eventView={eventView}/>
            <SidebarCharts organization={organization} eventView={eventView}/>
            <Tags generateUrl={this.generateTagUrl} totalValues={totalValues} eventView={eventView} organization={organization} location={location}/>
          </Layout.Side>
        </Layout.Body>
      </React.Fragment>);
    };
    return SummaryContent;
}(React.Component));
var StyledSearchBar = styled(SearchBar)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(1));
export default withProjects(SummaryContent);
var templateObject_1;
//# sourceMappingURL=content.jsx.map