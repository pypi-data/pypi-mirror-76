import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import { t } from 'app/locale';
import { getFieldRenderer } from 'app/utils/discover/fieldRenderers';
import { getTermHelp } from 'app/views/performance/data';
import DiscoverQuery from 'app/utils/discover/discoverQuery';
import QuestionTooltip from 'app/components/questionTooltip';
import { SectionHeading } from 'app/components/charts/styles';
import UserMisery from 'app/components/userMisery';
var UserStats = /** @class */ (function (_super) {
    __extends(UserStats, _super);
    function UserStats() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    UserStats.prototype.generateUserStatsEventView = function (eventView) {
        // narrow the search conditions of the Performance Summary event view
        // by modifying the columns to only show user misery and apdex scores
        var organization = this.props.organization;
        var threshold = organization.apdexThreshold.toString();
        eventView = eventView.withColumns([
            {
                kind: 'function',
                function: ['apdex', threshold, undefined],
            },
            {
                kind: 'function',
                function: ['user_misery', threshold, undefined],
            },
            {
                kind: 'function',
                function: ['count_unique', 'user', undefined],
            },
        ]);
        eventView.sorts = [];
        return eventView;
    };
    UserStats.prototype.renderContents = function (row) {
        var _a;
        var userMisery = <StatNumber>{'\u2014'}</StatNumber>;
        var _b = this.props, organization = _b.organization, location = _b.location;
        var threshold = organization.apdexThreshold;
        var apdex = <StatNumber>{'\u2014'}</StatNumber>;
        if (row) {
            var miserableUsers = Number(row["user_misery_" + threshold]);
            var totalUsers = Number(row.count_unique_user);
            if (!isNaN(miserableUsers) && !isNaN(totalUsers)) {
                userMisery = (<UserMisery bars={40} barHeight={30} miseryLimit={threshold} totalUsers={totalUsers} miserableUsers={miserableUsers}/>);
            }
            var apdexKey = "apdex_" + threshold;
            var formatter = getFieldRenderer(apdexKey, (_a = {}, _a[apdexKey] = 'number', _a));
            apdex = formatter(row, { organization: organization, location: location });
        }
        return (<Container>
        <div>
          <SectionHeading>{t('Apdex Score')}</SectionHeading>
          <StatNumber>{apdex}</StatNumber>
        </div>
        
        <UserMiseryContainer>
          <SectionHeading>
            {t('User Misery')}
            <QuestionTooltip position="top" title={getTermHelp(organization, 'userMisery')} size="sm"/>
          </SectionHeading>
          {userMisery}
        </UserMiseryContainer>
      </Container>);
    };
    UserStats.prototype.render = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, location = _a.location;
        var eventView = this.generateUserStatsEventView(this.props.eventView);
        return (<DiscoverQuery eventView={eventView} orgSlug={organization.slug} location={location} limit={1}>
        {function (_a) {
            var tableData = _a.tableData, isLoading = _a.isLoading;
            var hasResults = tableData && tableData.data && tableData.meta && tableData.data.length > 0;
            if (isLoading ||
                !tableData ||
                !tableData.meta ||
                !hasResults ||
                !eventView.isValid()) {
                return _this.renderContents(null);
            }
            var row = tableData.data[0];
            return _this.renderContents(row);
        }}
      </DiscoverQuery>);
    };
    return UserStats;
}(React.Component));
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr 1fr;\n  grid-row-gap: ", ";\n  margin-bottom: 40px;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr 1fr;\n  grid-row-gap: ", ";\n  margin-bottom: 40px;\n"])), space(4));
var UserMiseryContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  grid-column: 1/3;\n"], ["\n  grid-column: 1/3;\n"])));
var StatNumber = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: 32px;\n  color: ", ";\n\n  > div {\n    text-align: left;\n  }\n"], ["\n  font-size: 32px;\n  color: ", ";\n\n  > div {\n    text-align: left;\n  }\n"])), function (p) { return p.theme.gray700; });
export default UserStats;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=userStats.jsx.map