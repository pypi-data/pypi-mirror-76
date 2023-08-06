import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import OnboardingPanel from 'app/components/onboardingPanel';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import { t } from 'app/locale';
import emptyStateImg from '../../../images/spot/performance-empty-state.svg';
function Onboarding() {
    return (<OnboardingPanel image={<PerfImage src={emptyStateImg}/>}>
      <h3>{t('Pinpoint problems')}</h3>
      <p>
        {t('Something seem slow? Track down transactions to connect the dots between 10-second page loads and poor-performing API calls or slow database queries.')}
      </p>
      <ButtonList gap={1}>
        <Button priority="default" target="_blank" href="https://docs.sentry.io/performance-monitoring/performance/">
          {t('Learn More')}
        </Button>
        <Button priority="primary" target="_blank" href="https://docs.sentry.io/performance-monitoring/getting-started/">
          {t('Start Setup')}
        </Button>
      </ButtonList>
    </OnboardingPanel>);
}
var PerfImage = styled('img')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  @media (min-width: ", ") {\n    max-width: unset;\n    user-select: none;\n    position: absolute;\n    top: 50px;\n    bottom: 0;\n    width: 450px;\n    margin-top: auto;\n    margin-bottom: auto;\n  }\n\n  @media (min-width: ", ") {\n    width: 480px;\n  }\n\n  @media (min-width: ", ") {\n    width: 600px;\n  }\n"], ["\n  @media (min-width: ", ") {\n    max-width: unset;\n    user-select: none;\n    position: absolute;\n    top: 50px;\n    bottom: 0;\n    width: 450px;\n    margin-top: auto;\n    margin-bottom: auto;\n  }\n\n  @media (min-width: ", ") {\n    width: 480px;\n  }\n\n  @media (min-width: ", ") {\n    width: 600px;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.breakpoints[2]; });
var ButtonList = styled(ButtonBar)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  grid-template-columns: repeat(auto-fit, minmax(130px, max-content));\n"], ["\n  grid-template-columns: repeat(auto-fit, minmax(130px, max-content));\n"])));
export default Onboarding;
var templateObject_1, templateObject_2;
//# sourceMappingURL=onboarding.jsx.map