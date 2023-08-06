import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import ConfigStore from 'app/stores/configStore';
import ExternalLink from 'app/components/links/externalLink';
import { IconSentry } from 'app/icons';
import Hook from 'app/components/hook';
import getDynamicText from 'app/utils/getDynamicText';
import space from 'app/styles/space';
function Footer() {
    var config = ConfigStore.getConfig();
    return (<footer>
      <div className="container">
        <div className="pull-right">
          <FooterLink className="hidden-xs" href="/api/">
            {t('API')}
          </FooterLink>
          <FooterLink href="/docs/">{t('Docs')}</FooterLink>
          <FooterLink className="hidden-xs" href="https://github.com/getsentry/sentry">
            {t('Contribute')}
          </FooterLink>
          {config.isOnPremise && (<FooterLink className="hidden-xs" href="/out/">
              {t('Migrate to SaaS')}
            </FooterLink>)}
        </div>
        {config.isOnPremise && (<div className="version pull-left">
            {'Sentry '}
            {getDynamicText({
        fixed: 'Acceptance Test',
        value: config.version.current,
    })}
            <Build>
              {getDynamicText({
        fixed: 'test',
        value: config.version.build.substring(0, 7),
    })}
            </Build>
          </div>)}
        <LogoLink />
        <Hook name="footer"/>
      </div>
    </footer>);
}
var FooterLink = styled(ExternalLink)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  &.focus-visible {\n    outline: none;\n    box-shadow: ", " 0 2px 0;\n  }\n"], ["\n  &.focus-visible {\n    outline: none;\n    box-shadow: ", " 0 2px 0;\n  }\n"])), function (p) { return p.theme.blue400; });
var LogoLink = styled(function (props) { return (<a href="/" tabIndex={-1} {...props}>
    <IconSentry size="xl"/>
  </a>); })(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: block;\n  width: 32px;\n  height: 32px;\n  margin: 0 auto;\n"], ["\n  display: block;\n  width: 32px;\n  height: 32px;\n  margin: 0 auto;\n"])));
var Build = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n  font-weight: bold;\n  margin-left: ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n  font-weight: bold;\n  margin-left: ", ";\n"])), function (p) { return p.theme.fontSizeRelativeSmall; }, function (p) { return p.theme.gray400; }, space(1));
export default Footer;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=footer.jsx.map