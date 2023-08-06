import { __extends } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import IncidentRulesCreate from 'app/views/settings/incidentRules/create';
import IssueEditor from 'app/views/settings/projectAlerts/issueEditor';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import withProject from 'app/utils/withProject';
import EventView from 'app/utils/discover/eventView';
import { uniqueId } from 'app/utils/guid';
import AlertTypeChooser from './alertTypeChooser';
var Create = /** @class */ (function (_super) {
    __extends(Create, _super);
    function Create() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            eventView: undefined,
            alertType: _this.props.location.pathname.includes('/alerts/rules/')
                ? 'issue'
                : _this.props.location.pathname.includes('/alerts/metric-rules/')
                    ? 'metric'
                    : null,
        };
        /** Used to track analytics within one visit to the creation page */
        _this.sessionId = uniqueId();
        _this.handleChangeAlertType = function (alertType) {
            // alertType should be `issue` or `metric`
            _this.setState({ alertType: alertType });
        };
        return _this;
    }
    Create.prototype.componentDidMount = function () {
        var _a;
        var _b = this.props, organization = _b.organization, project = _b.project, location = _b.location;
        trackAnalyticsEvent({
            eventKey: 'new_alert_rule.viewed',
            eventName: 'New Alert Rule: Viewed',
            organization_id: organization.id,
            project_id: project.id,
            session_id: this.sessionId,
        });
        if ((_a = location === null || location === void 0 ? void 0 : location.query) === null || _a === void 0 ? void 0 : _a.createFromDiscover) {
            var eventView = EventView.fromLocation(location);
            // eslint-disable-next-line react/no-did-mount-set-state
            this.setState({ alertType: 'metric', eventView: eventView });
        }
    };
    Create.prototype.render = function () {
        var _a = this.props, hasMetricAlerts = _a.hasMetricAlerts, organization = _a.organization;
        var projectId = this.props.params.projectId;
        var _b = this.state, alertType = _b.alertType, eventView = _b.eventView;
        var shouldShowAlertTypeChooser = hasMetricAlerts;
        var title = t('New Alert');
        return (<React.Fragment>
        <SentryDocumentTitle title={title} objSlug={projectId}/>
        <SettingsPageHeader title={title}/>

        {shouldShowAlertTypeChooser && (<AlertTypeChooser organization={organization} selected={alertType} onChange={this.handleChangeAlertType}/>)}

        {(!hasMetricAlerts || alertType === 'issue') && <IssueEditor {...this.props}/>}

        {hasMetricAlerts && alertType === 'metric' && (<IncidentRulesCreate {...this.props} eventView={eventView} sessionId={this.sessionId}/>)}
      </React.Fragment>);
    };
    return Create;
}(React.Component));
export default withProject(Create);
//# sourceMappingURL=create.jsx.map