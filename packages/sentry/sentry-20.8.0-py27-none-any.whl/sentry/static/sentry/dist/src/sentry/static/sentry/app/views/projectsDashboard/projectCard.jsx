import { __assign, __extends, __makeTemplateObject, __rest } from "tslib";
import PropTypes from 'prop-types';
import React from 'react';
import Reflux from 'reflux';
import createReactClass from 'create-react-class';
import styled from '@emotion/styled';
import BookmarkStar from 'app/components/projects/bookmarkStar';
import { loadStatsForProject } from 'app/actionCreators/projects';
import IdBadge from 'app/components/idBadge';
import Link from 'app/components/links/link';
import ProjectsStatsStore from 'app/stores/projectsStatsStore';
import SentryTypes from 'app/sentryTypes';
import space from 'app/styles/space';
import withOrganization from 'app/utils/withOrganization';
import withApi from 'app/utils/withApi';
import Chart from './chart';
import Deploys from './deploys';
import NoEvents from './noEvents';
var ProjectCard = /** @class */ (function (_super) {
    __extends(ProjectCard, _super);
    function ProjectCard() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectCard.prototype.componentDidMount = function () {
        var _a = this.props, organization = _a.organization, project = _a.project, api = _a.api;
        // fetch project stats
        loadStatsForProject(api, project.id, {
            orgId: organization.slug,
            projectId: project.id,
        });
    };
    ProjectCard.prototype.render = function () {
        var _a = this.props, organization = _a.organization, project = _a.project, hasProjectAccess = _a.hasProjectAccess;
        var id = project.id, firstEvent = project.firstEvent, stats = project.stats, slug = project.slug;
        return (<div data-test-id={slug}>
        {stats ? (<StyledProjectCard>
            <StyledProjectCardHeader>
              <StyledIdBadge project={project} avatarSize={18} displayName={hasProjectAccess ? (<Link to={"/organizations/" + organization.slug + "/issues/?project=" + id}>
                      <strong>{slug}</strong>
                    </Link>) : (<span>{slug}</span>)}/>
              <BookmarkStar organization={organization} project={project}/>
            </StyledProjectCardHeader>
            <ChartContainer>
              <Chart stats={stats}/>
              {!firstEvent && <NoEvents />}
            </ChartContainer>
            <Deploys project={project}/>
          </StyledProjectCard>) : (<LoadingCard />)}
      </div>);
    };
    ProjectCard.propTypes = {
        organization: SentryTypes.Organization.isRequired,
        project: SentryTypes.Project.isRequired,
        hasProjectAccess: PropTypes.bool,
    };
    return ProjectCard;
}(React.Component));
var ProjectCardContainer = createReactClass({
    propTypes: {
        project: SentryTypes.Project,
    },
    mixins: [Reflux.listenTo(ProjectsStatsStore, 'onProjectStoreUpdate')],
    getInitialState: function () {
        var project = this.props.project;
        var initialState = ProjectsStatsStore.getInitialState() || {};
        return {
            projectDetails: initialState[project.slug] || null,
        };
    },
    onProjectStoreUpdate: function (itemsBySlug) {
        var project = this.props.project;
        // Don't update state if we already have stats
        if (!itemsBySlug[project.slug]) {
            return;
        }
        if (itemsBySlug[project.slug] === this.state.projectDetails) {
            return;
        }
        this.setState({
            projectDetails: itemsBySlug[project.slug],
        });
    },
    render: function () {
        var _a = this.props, project = _a.project, props = __rest(_a, ["project"]);
        var projectDetails = this.state.projectDetails;
        return (<ProjectCard {...props} project={__assign(__assign({}, project), (projectDetails || {}))}/>);
    },
});
var ChartContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  background: ", ";\n  padding-top: ", ";\n"], ["\n  position: relative;\n  background: ", ";\n  padding-top: ", ";\n"])), function (p) { return p.theme.gray100; }, space(1));
var StyledProjectCardHeader = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  margin: 12px ", ";\n"], ["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n  margin: 12px ", ";\n"])), space(2));
var StyledProjectCard = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  background-color: white;\n  border: 1px solid ", ";\n  border-radius: ", ";\n  box-shadow: ", ";\n"], ["\n  background-color: white;\n  border: 1px solid ", ";\n  border-radius: ", ";\n  box-shadow: ", ";\n"])), function (p) { return p.theme.borderDark; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.dropShadowLight; });
var LoadingCard = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  border: 1px solid transparent;\n  background-color: ", ";\n  height: 210px;\n"], ["\n  border: 1px solid transparent;\n  background-color: ", ";\n  height: 210px;\n"])), function (p) { return p.theme.gray100; });
var StyledIdBadge = styled(IdBadge)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  overflow: hidden;\n  white-space: nowrap;\n"], ["\n  overflow: hidden;\n  white-space: nowrap;\n"])));
export { ProjectCard };
export default withOrganization(withApi(ProjectCardContainer));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=projectCard.jsx.map