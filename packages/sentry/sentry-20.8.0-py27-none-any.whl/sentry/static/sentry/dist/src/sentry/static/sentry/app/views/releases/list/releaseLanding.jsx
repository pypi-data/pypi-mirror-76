import { __extends } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import { analytics } from 'app/utils/analytics';
import Placeholder from 'app/components/placeholder';
import withOrganization from 'app/utils/withOrganization';
import withProject from 'app/utils/withProject';
import ReleaseLandingCard from './releaseLandingCard';
function Illustration(_a) {
    var children = _a.children;
    return <React.Suspense fallback={<Placeholder />}>{children}</React.Suspense>;
}
var IllustrationContributors = React.lazy(function () {
    return import(
    /* webpackChunkName: "IllustrationContributors" */ './illustrations/contributors');
});
var IllustrationSuggestedAssignees = React.lazy(function () {
    return import(
    /* webpackChunkName: "IllustrationSuggestedAssignees" */ './illustrations/suggestedAssignees');
});
var IllustrationIssues = React.lazy(function () {
    return import(/* webpackChunkName: "IllustrationIssues" */ './illustrations/issues');
});
var IllustrationMinified = React.lazy(function () {
    return import(/* webpackChunkName: "IllustrationMinified" */ './illustrations/minified');
});
var IllustrationEmails = React.lazy(function () {
    return import(/* webpackChunkName: "IllustrationEmails" */ './illustrations/emails');
});
var cards = [
    {
        title: t("You Haven't Set Up Releases!"),
        disclaimer: t('(you made no releases in 30 days)'),
        message: t('Releases provide additional context, with rich commits, so you know which errors were addressed and which were introduced in a release'),
        svg: (<Illustration>
        <IllustrationContributors />
      </Illustration>),
    },
    {
        title: t('Suspect Commits'),
        message: t('Sentry suggests which commit caused an issue and who is likely responsible so you can triage'),
        svg: (<Illustration>
        <IllustrationSuggestedAssignees />
      </Illustration>),
    },
    {
        title: t('Release Stats'),
        message: t('See the commits in each release, and which issues were introduced or fixed in the release'),
        svg: (<Illustration>
        <IllustrationIssues />
      </Illustration>),
    },
    {
        title: t('Easy Resolution'),
        message: t('Automatically resolve issues by including the issue number in your commit message'),
        svg: (<Illustration>
        <IllustrationMinified />
      </Illustration>),
    },
    {
        title: t('Deploy Emails'),
        message: t('Receive email notifications when your code gets deployed'),
        svg: (<Illustration>
        <IllustrationEmails />
      </Illustration>),
    },
];
var ReleaseLanding = withOrganization(withProject(/** @class */ (function (_super) {
    __extends(ReleaseLanding, _super);
    function ReleaseLanding() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            stepId: 0,
        };
        _this.handleClick = function () {
            var stepId = _this.state.stepId;
            var _a = _this.props, organization = _a.organization, project = _a.project;
            var title = cards[stepId].title;
            if (stepId >= cards.length - 1) {
                return;
            }
            _this.setState(function (state) { return ({
                stepId: state.stepId + 1,
            }); });
            analytics('releases.landing_card_clicked', {
                org_id: parseInt(organization.id, 10),
                project_id: project && parseInt(project.id, 10),
                step_id: stepId,
                step_title: title,
            });
        };
        _this.getCard = function (stepId) { return cards[stepId]; };
        return _this;
    }
    ReleaseLanding.prototype.componentDidMount = function () {
        var _a = this.props, organization = _a.organization, project = _a.project;
        analytics('releases.landing_card_viewed', {
            org_id: parseInt(organization.id, 10),
            project_id: project && parseInt(project.id, 10),
        });
    };
    ReleaseLanding.prototype.render = function () {
        var stepId = this.state.stepId;
        var card = this.getCard(stepId);
        return (<ReleaseLandingCard onClick={this.handleClick} card={card} step={stepId} cardsLength={cards.length}/>);
    };
    return ReleaseLanding;
}(React.Component))));
export default ReleaseLanding;
//# sourceMappingURL=releaseLanding.jsx.map