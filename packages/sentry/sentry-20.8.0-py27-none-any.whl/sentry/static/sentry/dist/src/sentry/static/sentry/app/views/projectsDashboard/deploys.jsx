import { __assign, __makeTemplateObject, __read } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import Button from 'app/components/button';
import SentryTypes from 'app/sentryTypes';
import TextOverflow from 'app/components/textOverflow';
import TimeSince from 'app/components/timeSince';
import Version from 'app/components/version';
import space from 'app/styles/space';
import getDynamicText from 'app/utils/getDynamicText';
var DEPLOY_COUNT = 2;
var Deploys = function (_a) {
    var project = _a.project;
    var flattenedDeploys = Object.entries(project.latestDeploys || {}).map(function (_a) {
        var _b = __read(_a, 2), environment = _b[0], value = _b[1];
        return (__assign({ environment: environment }, value));
    });
    var deploys = (flattenedDeploys || [])
        .sort(function (a, b) { return new Date(b.dateFinished).getTime() - new Date(a.dateFinished).getTime(); })
        .slice(0, DEPLOY_COUNT);
    if (!deploys.length) {
        return <NoDeploys />;
    }
    return (<DeployContainer>
      {deploys.map(function (deploy) { return (<Deploy key={deploy.environment + "-" + deploy.version} deploy={deploy} project={project}/>); })}
    </DeployContainer>);
};
Deploys.propTypes = {
    project: SentryTypes.Project.isRequired,
};
export default Deploys;
var Deploy = function (_a) {
    var deploy = _a.deploy, project = _a.project;
    return (<DeployRow>
    <Environment>{deploy.environment}</Environment>

    <StyledTextOverflow>
      <Version version={deploy.version} projectId={project.id} tooltipRawVersion truncate/>
    </StyledTextOverflow>

    <DeployTimeWrapper>
      {getDynamicText({
        fixed: '3 hours ago',
        value: <TimeSince date={deploy.dateFinished}/>,
    })}
    </DeployTimeWrapper>
  </DeployRow>);
};
Deploy.propTypes = {
    deploy: SentryTypes.Deploy.isRequired,
    project: SentryTypes.Project.isRequired,
};
var NoDeploys = function () { return (<DeployContainer>
    <Background>
      <Button size="xsmall" href="https://docs.sentry.io/learn/releases/" external>
        {t('Track deploys')}
      </Button>
    </Background>
  </DeployContainer>); };
var DeployRow = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  color: ", ";\n  font-size: ", ";\n\n  &:not(:last-of-type) {\n    margin-top: ", ";\n  }\n"], ["\n  display: flex;\n  justify-content: space-between;\n  color: ", ";\n  font-size: ", ";\n\n  &:not(:last-of-type) {\n    margin-top: ", ";\n  }\n"])), function (p) { return p.theme.gray500; }, function (p) { return p.theme.fontSizeSmall; }, space(1));
var Environment = styled(TextOverflow)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: ", ";\n  text-transform: uppercase;\n  width: 80px;\n  border: 1px solid ", ";\n  margin-right: ", ";\n  background-color: ", ";\n  text-align: center;\n  border-radius: ", ";\n  flex-shrink: 0;\n"], ["\n  font-size: ", ";\n  text-transform: uppercase;\n  width: 80px;\n  border: 1px solid ", ";\n  margin-right: ", ";\n  background-color: ", ";\n  text-align: center;\n  border-radius: ", ";\n  flex-shrink: 0;\n"])), function (p) { return p.theme.fontSizeExtraSmall; }, function (p) { return p.theme.borderLight; }, space(1), function (p) { return p.theme.gray100; }, function (p) { return p.theme.borderRadius; });
var StyledTextOverflow = styled(TextOverflow)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
var DeployTimeWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  overflow: hidden;\n  text-overflow: ellipsis;\n  white-space: nowrap;\n  width: 90px;\n  flex-grow: 1;\n  flex-shrink: 0;\n  text-align: right;\n"], ["\n  overflow: hidden;\n  text-overflow: ellipsis;\n  white-space: nowrap;\n  width: 90px;\n  flex-grow: 1;\n  flex-shrink: 0;\n  text-align: right;\n"])));
var DeployContainer = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  height: 92px;\n  padding: ", ";\n"], ["\n  height: 92px;\n  padding: ", ";\n"])), space(2));
var Background = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: flex;\n  height: 100%;\n  background-color: ", ";\n  align-items: center;\n  justify-content: center;\n"], ["\n  display: flex;\n  height: 100%;\n  background-color: ", ";\n  align-items: center;\n  justify-content: center;\n"])), function (p) { return p.theme.gray100; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=deploys.jsx.map