import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import DocumentTitle from 'react-document-title';
import React from 'react';
import flatten from 'lodash/flatten';
import omit from 'lodash/omit';
import styled from '@emotion/styled';
import { IconAdd, IconInfo, IconSettings, IconCheckmark } from 'app/icons';
import { PageContent, PageHeader } from 'app/styles/organization';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import { navigateTo } from 'app/actionCreators/navigation';
import { t, tct } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import Alert from 'app/components/alert';
import AsyncComponent from 'app/components/asyncComponent';
import FeatureBadge from 'app/components/featureBadge';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import ExternalLink from 'app/components/links/externalLink';
import LoadingIndicator from 'app/components/loadingIndicator';
import PageHeading from 'app/components/pageHeading';
import Pagination from 'app/components/pagination';
import Projects from 'app/utils/projects';
import space from 'app/styles/space';
import withOrganization from 'app/utils/withOrganization';
import Access from 'app/components/acl/access';
import ConfigStore from 'app/stores/configStore';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import { promptsUpdate } from 'app/actionCreators/prompts';
import { TableLayout, TitleAndSparkLine } from './styles';
import AlertListRow from './row';
import Onboarding from './onboarding';
var DEFAULT_QUERY_STATUS = 'open';
var DOCS_URL = 'https://docs.sentry.io/workflow/alerts-notifications/alerts/?_ga=2.21848383.580096147.1592364314-1444595810.1582160976';
var trackDocumentationClicked = function (org) {
    return trackAnalyticsEvent({
        eventKey: 'alert_stream.documentation_clicked',
        eventName: 'Alert Stream: Documentation Clicked',
        organization_id: org.id,
        user_id: ConfigStore.get('user').id,
    });
};
function getQueryStatus(status) {
    return ['open', 'closed'].includes(status) ? status : DEFAULT_QUERY_STATUS;
}
var IncidentsList = /** @class */ (function (_super) {
    __extends(IncidentsList, _super);
    function IncidentsList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * Incidents list is currently at the organization level, but the link needs to
         * go down to a specific project scope.
         */
        _this.handleNavigateToSettings = function (e) {
            var _a = _this.props, router = _a.router, params = _a.params;
            e.preventDefault();
            navigateTo("/settings/" + params.orgId + "/projects/:projectId/alerts/", router);
        };
        return _this;
    }
    IncidentsList.prototype.getEndpoints = function () {
        var _a = this.props, params = _a.params, location = _a.location;
        var query = location.query;
        var status = getQueryStatus(query.status);
        return [
            [
                'incidentList',
                "/organizations/" + (params && params.orgId) + "/incidents/",
                { query: __assign(__assign({}, query), { status: status }) },
            ],
        ];
    };
    /**
     * If our incidentList is empty, determine if we've configured alert rules or
     * if the user has seen the welcome prompt.
     */
    IncidentsList.prototype.onLoadAllEndpointsSuccess = function () {
        var _a;
        return __awaiter(this, void 0, void 0, function () {
            var incidentList, _b, params, location, organization, alertRules, hasAlertRule, prompt, firstVisitShown;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        incidentList = this.state.incidentList;
                        if (incidentList.length !== 0) {
                            this.setState({ hasAlertRule: true, firstVisitShown: false });
                            return [2 /*return*/];
                        }
                        this.setState({ loading: true });
                        _b = this.props, params = _b.params, location = _b.location, organization = _b.organization;
                        return [4 /*yield*/, this.api.requestPromise("/organizations/" + (params === null || params === void 0 ? void 0 : params.orgId) + "/alert-rules/", {
                                method: 'GET',
                                query: location.query,
                            })];
                    case 1:
                        alertRules = _c.sent();
                        hasAlertRule = alertRules.length > 0;
                        // We've already configured alert rules, no need to check if we should show
                        // the "first time welcome" prompt
                        if (hasAlertRule) {
                            this.setState({ hasAlertRule: hasAlertRule, firstVisitShown: false, loading: false });
                            return [2 /*return*/];
                        }
                        return [4 /*yield*/, this.api.requestPromise('/promptsactivity/', {
                                query: {
                                    organization_id: organization.id,
                                    feature: 'alert_stream',
                                },
                            })];
                    case 2:
                        prompt = _c.sent();
                        firstVisitShown = !((_a = prompt === null || prompt === void 0 ? void 0 : prompt.data) === null || _a === void 0 ? void 0 : _a.dismissed_ts);
                        if (firstVisitShown) {
                            // Prompt has not been seen, mark the prompt as seen immediately so they
                            // don't see it again
                            promptsUpdate(this.api, {
                                feature: 'alert_stream',
                                organizationId: organization.id,
                                status: 'dismissed',
                            });
                        }
                        this.setState({ hasAlertRule: hasAlertRule, firstVisitShown: firstVisitShown, loading: false });
                        return [2 /*return*/];
                }
            });
        });
    };
    IncidentsList.prototype.tryRenderOnboarding = function () {
        var firstVisitShown = this.state.firstVisitShown;
        if (!firstVisitShown) {
            return null;
        }
        var actions = (<React.Fragment>
        <Button size="small" external href={DOCS_URL}>
          {t('View Features')}
        </Button>
        <AddAlertRuleButton {...this.props}/>
      </React.Fragment>);
        return <Onboarding actions={actions}/>;
    };
    IncidentsList.prototype.tryRenderEmpty = function () {
        var _a = this.state, hasAlertRule = _a.hasAlertRule, incidentList = _a.incidentList;
        var status = getQueryStatus(this.props.location.query.status);
        if (incidentList.length > 0) {
            return null;
        }
        return (<EmptyMessage size="medium" icon={<IconCheckmark isCircled size="48"/>} title={!hasAlertRule
            ? t('No metric alert rules exist for these projects.')
            : status === 'open'
                ? t('Everything’s a-okay. There are no unresolved metric alerts in these projects.')
                : t('There are no resolved metric alerts in these projects.')} description={tct('Learn more about [link:Metric Alerts]', {
            link: <ExternalLink href={DOCS_URL}/>,
        })}/>);
    };
    IncidentsList.prototype.renderLoading = function () {
        return this.renderBody();
    };
    IncidentsList.prototype.renderList = function () {
        var _a, _b;
        var _c = this.state, loading = _c.loading, incidentList = _c.incidentList, incidentListPageLinks = _c.incidentListPageLinks, hasAlertRule = _c.hasAlertRule;
        var orgId = this.props.params.orgId;
        var allProjectsFromIncidents = new Set(flatten(incidentList === null || incidentList === void 0 ? void 0 : incidentList.map(function (_a) {
            var projects = _a.projects;
            return projects;
        })));
        var checkingForAlertRules = incidentList && incidentList.length === 0 && hasAlertRule === undefined
            ? true
            : false;
        var showLoadingIndicator = loading || checkingForAlertRules;
        var status = getQueryStatus(this.props.location.query.status);
        return (<React.Fragment>
        {(_a = this.tryRenderOnboarding()) !== null && _a !== void 0 ? _a : (<Panel>
            {!loading && (<StyledPanelHeader>
                <TableLayout status={status}>
                  <PaddedTitleAndSparkLine status={status}>
                    <div>{t('Alert')}</div>
                    {status === 'open' && <div>{t('Graph')}</div>}
                  </PaddedTitleAndSparkLine>
                  <div>{t('Project')}</div>
                  <div>{t('Triggered')}</div>
                  {status === 'closed' && <div>{t('Duration')}</div>}
                  {status === 'closed' && <div>{t('Resolved')}</div>}
                </TableLayout>
              </StyledPanelHeader>)}
            {showLoadingIndicator ? (<LoadingIndicator />) : ((_b = this.tryRenderEmpty()) !== null && _b !== void 0 ? _b : (<PanelBody>
                  <Projects orgId={orgId} slugs={Array.from(allProjectsFromIncidents)}>
                    {function (_a) {
            var initiallyLoaded = _a.initiallyLoaded, projects = _a.projects;
            return incidentList.map(function (incident) { return (<AlertListRow key={incident.id} projectsLoaded={initiallyLoaded} projects={projects} incident={incident} orgId={orgId} filteredStatus={status}/>); });
        }}
                  </Projects>
                </PanelBody>))}
          </Panel>)}
        <Pagination pageLinks={incidentListPageLinks}/>
      </React.Fragment>);
    };
    IncidentsList.prototype.renderBody = function () {
        var _a = this.state, loading = _a.loading, firstVisitShown = _a.firstVisitShown;
        var _b = this.props, params = _b.params, location = _b.location, organization = _b.organization;
        var pathname = location.pathname, query = location.query;
        var orgId = params.orgId;
        var openIncidentsQuery = omit(__assign(__assign({}, query), { status: 'open' }), 'cursor');
        var closedIncidentsQuery = omit(__assign(__assign({}, query), { status: 'closed' }), 'cursor');
        var status = getQueryStatus(query.status);
        return (<DocumentTitle title={"Alerts- " + orgId + " - Sentry"}>
        <GlobalSelectionHeader organization={organization} showDateSelector={false}>
          <PageContent>
            <PageHeader>
              <StyledPageHeading>
                {t('Alerts')} <FeatureBadge type="beta"/>
              </StyledPageHeading>

              {!loading && !firstVisitShown ? (<Actions gap={1}>
                  <AddAlertRuleButton {...this.props}/>

                  <Button onClick={this.handleNavigateToSettings} href="#" size="small" icon={<IconSettings size="xs"/>}>
                    {t('View Rules')}
                  </Button>

                  <ButtonBar merged active={status}>
                    <Button to={{ pathname: pathname, query: openIncidentsQuery }} barId="open" size="small">
                      {t('Active')}
                    </Button>
                    <Button to={{ pathname: pathname, query: closedIncidentsQuery }} barId="closed" size="small">
                      {t('Resolved')}
                    </Button>
                  </ButtonBar>
                </Actions>) : (
        // Keep an empty Actions container around to keep the height of
        // the header correct so we don't jitter between loading
        // states.
        <Actions>{null}</Actions>)}
            </PageHeader>

            <Alert type="info" icon={<IconInfo size="md"/>}>
              {tct('This page is in beta and currently only shows [link:metric alerts]. [contactLink:Please contact us if you have any feedback.]', {
            link: (<ExternalLink onClick={function () { return trackDocumentationClicked(organization); }} href={DOCS_URL}/>),
            contactLink: (<ExternalLink href="mailto:alerting-feedback@sentry.io">
                      {t('Please contact us if you have any feedback.')}
                    </ExternalLink>),
        })}
            </Alert>
            {this.renderList()}
          </PageContent>
        </GlobalSelectionHeader>
      </DocumentTitle>);
    };
    return IncidentsList;
}(AsyncComponent));
var IncidentsListContainer = /** @class */ (function (_super) {
    __extends(IncidentsListContainer, _super);
    function IncidentsListContainer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    IncidentsListContainer.prototype.componentDidMount = function () {
        this.trackView();
    };
    IncidentsListContainer.prototype.componentDidUpdate = function (nextProps) {
        var _a, _b;
        if (((_a = nextProps.location.query) === null || _a === void 0 ? void 0 : _a.status) !== ((_b = this.props.location.query) === null || _b === void 0 ? void 0 : _b.status)) {
            this.trackView();
        }
    };
    IncidentsListContainer.prototype.trackView = function () {
        var _a = this.props, location = _a.location, organization = _a.organization;
        var status = getQueryStatus(location.query.status);
        trackAnalyticsEvent({
            eventKey: 'alert_stream.viewed',
            eventName: 'Alert Stream: Viewed',
            organization_id: organization.id,
            status: status,
        });
    };
    IncidentsListContainer.prototype.render = function () {
        return <IncidentsList {...this.props}/>;
    };
    return IncidentsListContainer;
}(React.Component));
var AddAlertRuleButton = function (_a) {
    var router = _a.router, params = _a.params, organization = _a.organization;
    return (<Access organization={organization} access={['project:write']}>
    {function (_a) {
        var hasAccess = _a.hasAccess;
        return (<Button disabled={!hasAccess} title={!hasAccess
            ? t('Users with admin permission or higher can create alert rules.')
            : undefined} onClick={function (e) {
            e.preventDefault();
            navigateTo("/settings/" + params.orgId + "/projects/:projectId/alerts/new/?referrer=alert_stream", router);
        }} priority="primary" href="#" size="small" icon={<IconAdd isCircled size="xs"/>}>
        {t('Add Alert Rule')}
      </Button>);
    }}
  </Access>);
};
var StyledPageHeading = styled(PageHeading)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var PaddedTitleAndSparkLine = styled(TitleAndSparkLine)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding-left: ", ";\n"], ["\n  padding-left: ", ";\n"])), space(2));
var StyledPanelHeader = styled(PanelHeader)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  /* Match table row padding for the grid to align */\n  padding: ", " ", " ", " 0;\n"], ["\n  /* Match table row padding for the grid to align */\n  padding: ", " ", " ", " 0;\n"])), space(1.5), space(2), space(1.5));
var Actions = styled(ButtonBar)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  height: 32px;\n"], ["\n  height: 32px;\n"])));
export default withOrganization(IncidentsListContainer);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=index.jsx.map