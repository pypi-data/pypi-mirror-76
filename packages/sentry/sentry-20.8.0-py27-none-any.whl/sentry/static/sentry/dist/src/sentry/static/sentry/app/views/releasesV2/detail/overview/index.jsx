import { __assign, __extends, __rest } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
import withOrganization from 'app/utils/withOrganization';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withApi from 'app/utils/withApi';
import { formatVersion } from 'app/utils/formatters';
import routeTitleGen from 'app/utils/routeTitle';
import { Main, Side } from 'app/components/layouts/thirds';
import ReleaseChart from './chart/';
import Issues from './issues';
import CommitAuthorBreakdown from './commitAuthorBreakdown';
import ProjectReleaseDetails from './projectReleaseDetails';
import OtherProjects from './otherProjects';
import TotalCrashFreeUsers from './totalCrashFreeUsers';
import Deploys from './deploys';
import ReleaseStatsRequest from './releaseStatsRequest';
import { YAxis } from './chart/releaseChartControls';
import SwitchReleasesButton from '../../utils/switchReleasesButton';
import { ReleaseContext } from '..';
var ReleaseOverview = /** @class */ (function (_super) {
    __extends(ReleaseOverview, _super);
    function ReleaseOverview() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleYAxisChange = function (yAxis) {
            var _a = _this.props, location = _a.location, router = _a.router;
            router.push(__assign(__assign({}, location), { query: __assign(__assign({}, location.query), { yAxis: yAxis }) }));
        };
        return _this;
    }
    ReleaseOverview.prototype.getTitle = function () {
        var _a = this.props, params = _a.params, organization = _a.organization;
        return routeTitleGen(t('Release %s', formatVersion(params.release)), organization.slug, false);
    };
    ReleaseOverview.prototype.getYAxis = function (hasHealthData) {
        var yAxis = this.props.location.query.yAxis;
        if (typeof yAxis === 'string') {
            return yAxis;
        }
        if (hasHealthData) {
            return YAxis.SESSIONS;
        }
        return YAxis.EVENTS;
    };
    ReleaseOverview.prototype.render = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, selection = _a.selection, location = _a.location, api = _a.api, router = _a.router;
        return (<ReleaseContext.Consumer>
        {function (_a) {
            var release = _a.release, project = _a.project, deploys = _a.deploys, releaseMeta = _a.releaseMeta;
            var commitCount = release.commitCount, version = release.version;
            var hasHealthData = (project.healthData || {}).hasHealthData;
            var hasDiscover = organization.features.includes('discover-basic');
            var yAxis = _this.getYAxis(hasHealthData);
            return (<ReleaseStatsRequest api={api} orgId={organization.slug} projectSlug={project.slug} version={version} selection={selection} location={location} yAxis={yAxis} hasHealthData={hasHealthData} hasDiscover={hasDiscover}>
              {function (_a) {
                var crashFreeTimeBreakdown = _a.crashFreeTimeBreakdown, releaseStatsProps = __rest(_a, ["crashFreeTimeBreakdown"]);
                return (<React.Fragment>
                  <Main>
                    {(hasDiscover || hasHealthData) && (<ReleaseChart {...releaseStatsProps} selection={selection} yAxis={yAxis} onYAxisChange={_this.handleYAxisChange} router={router} organization={organization} hasHealthData={hasHealthData} location={location} api={api} version={version} hasDiscover={hasDiscover}/>)}

                    <Issues orgId={organization.slug} selection={selection} version={version} location={location}/>
                  </Main>
                  <Side>
                    <ProjectReleaseDetails release={release} releaseMeta={releaseMeta} orgSlug={organization.slug} projectSlug={project.slug}/>
                    {commitCount > 0 && (<CommitAuthorBreakdown version={version} orgId={organization.slug} projectSlug={project.slug}/>)}
                    {releaseMeta.projects.length > 1 && (<OtherProjects projects={releaseMeta.projects.filter(function (p) { return p.slug !== project.slug; })} location={location}/>)}
                    {hasHealthData && (<TotalCrashFreeUsers crashFreeTimeBreakdown={crashFreeTimeBreakdown}/>)}
                    {deploys.length > 0 && (<Deploys version={version} orgSlug={organization.slug} deploys={deploys}/>)}
                  </Side>

                  <SwitchReleasesButton version="1" orgId={organization.id}/>
                </React.Fragment>);
            }}
            </ReleaseStatsRequest>);
        }}
      </ReleaseContext.Consumer>);
    };
    return ReleaseOverview;
}(AsyncView));
export default withApi(withGlobalSelection(withOrganization(ReleaseOverview)));
//# sourceMappingURL=index.jsx.map