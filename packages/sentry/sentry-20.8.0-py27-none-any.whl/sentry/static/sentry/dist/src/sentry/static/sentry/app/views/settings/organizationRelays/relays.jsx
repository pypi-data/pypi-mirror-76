import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import omit from 'lodash/omit';
import theme from 'app/utils/theme';
import { openModal } from 'app/actionCreators/modal';
import { PanelTable } from 'app/components/panels';
import { t, tct } from 'app/locale';
import AsyncComponent from 'app/components/asyncComponent';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import ExternalLink from 'app/components/links/externalLink';
import Button from 'app/components/button';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import TextBlock from 'app/views/settings/components/text/textBlock';
import TextOverflow from 'app/components/textOverflow';
import Clipboard from 'app/components/clipboard';
import { IconAdd, IconCopy, IconEdit, IconDelete } from 'app/icons';
import DateTime from 'app/components/dateTime';
import space from 'app/styles/space';
import { defined } from 'app/utils';
import Tooltip from 'app/components/tooltip';
import QuestionTooltip from 'app/components/questionTooltip';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import Add from './modals/add';
import Edit from './modals/edit';
var RELAY_DOCS_LINK = 'https://getsentry.github.io/relay/';
var Relays = /** @class */ (function (_super) {
    __extends(Relays, _super);
    function Relays() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDelete = function (publicKey) { return function () { return __awaiter(_this, void 0, void 0, function () {
            var relays, trustedRelays, response, _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        relays = this.state.relays;
                        trustedRelays = relays
                            .filter(function (relay) { return relay.publicKey !== publicKey; })
                            .map(function (relay) { return omit(relay, ['created', 'lastModified']); });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/organizations/" + this.props.organization.slug + "/", {
                                method: 'PUT',
                                data: { trustedRelays: trustedRelays },
                            })];
                    case 2:
                        response = _b.sent();
                        addSuccessMessage(t('Successfully deleted Relay public key'));
                        this.setRelays(response.trustedRelays);
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        addErrorMessage(t('An unknown error occurred while deleting Relay public key'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); }; };
        _this.handleOpenEditDialog = function (publicKey) { return function () {
            var editRelay = _this.state.relays.find(function (relay) { return relay.publicKey === publicKey; });
            if (!editRelay) {
                return;
            }
            openModal(function (modalProps) { return (<Edit {...modalProps} savedRelays={_this.state.relays} api={_this.api} orgSlug={_this.props.organization.slug} relay={editRelay} onSubmitSuccess={function (response) {
                _this.successfullySaved(response, t('Successfully updated Relay public key'));
            }}/>); });
        }; };
        _this.handleOpenAddDialog = function () {
            openModal(function (modalProps) { return (<Add {...modalProps} savedRelays={_this.state.relays} api={_this.api} orgSlug={_this.props.organization.slug} onSubmitSuccess={function (response) {
                _this.successfullySaved(response, t('Successfully added Relay public key'));
            }}/>); });
        };
        return _this;
    }
    Relays.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { relays: this.props.organization.trustedRelays });
    };
    Relays.prototype.setRelays = function (trustedRelays) {
        this.setState({ relays: trustedRelays });
    };
    Relays.prototype.successfullySaved = function (response, successMessage) {
        addSuccessMessage(successMessage);
        this.setRelays(response.trustedRelays);
    };
    Relays.prototype.renderBody = function () {
        var _this = this;
        var relays = this.state.relays;
        var title = t('Relays');
        return (<React.Fragment>
        <SentryDocumentTitle title={title} objSlug={this.props.organization.slug}/>
        <SettingsPageHeader title={title} action={<Button priority="primary" size="small" icon={<IconAdd size="xs" isCircled/>} onClick={this.handleOpenAddDialog}>
              {t('New Relay Key')}
            </Button>}/>
        <TextBlock>
          {tct("Relay is a relay service built by Sentry. You can run this on-premise for your SDKs or server to customize data scrubbing, buffering retries and more. You can generate Relay keys for access. For more on how to set this up, read the [link:docs].", {
            link: <ExternalLink href={RELAY_DOCS_LINK}/>,
        })}
        </TextBlock>
        <StyledPanelTable isEmpty={relays.length === 0} emptyMessage={t('No relays keys have been added yet.')} headers={[t('Display Name'), t('Relay Key'), t('Date Created'), '']}>
          {relays.map(function (_a) {
            var key = _a.publicKey, name = _a.name, created = _a.created, description = _a.description;
            var maskedKey = '*************************';
            return (<React.Fragment key={key}>
                <Name>
                  <Text>{name}</Text>
                  {description && (<QuestionTooltip position="top" size="sm" title={description}/>)}
                </Name>
                <KeyWrapper>
                  <Key content={maskedKey}>{maskedKey}</Key>
                  <IconWrapper>
                    <Clipboard value={key}>
                      <Tooltip title={t('Click to copy')} containerDisplayMode="flex">
                        <IconCopy color="gray500"/>
                      </Tooltip>
                    </Clipboard>
                  </IconWrapper>
                </KeyWrapper>
                <Text>
                  {!defined(created) ? t('Unknown') : <DateTime date={created}/>}
                </Text>
                <Actions>
                  <Button size="small" title={t('Edit Key')} label={t('Edit Key')} icon={<IconEdit size="sm"/>} onClick={_this.handleOpenEditDialog(key)}/>
                  <Button size="small" title={t('Delete Key')} label={t('Delete Key')} onClick={_this.handleDelete(key)} icon={<IconDelete size="sm"/>}/>
                </Actions>
              </React.Fragment>);
        })}
        </StyledPanelTable>
      </React.Fragment>);
    };
    return Relays;
}(AsyncComponent));
export default Relays;
var StyledPanelTable = styled(PanelTable)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  grid-template-columns: repeat(3, auto) max-content;\n  > * {\n    @media (max-width: ", ") {\n      padding: ", ";\n    }\n  }\n"], ["\n  grid-template-columns: repeat(3, auto) max-content;\n  > * {\n    @media (max-width: ", ") {\n      padding: ", ";\n    }\n  }\n"])), theme.breakpoints[0], space(1));
var KeyWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto 1fr;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: auto 1fr;\n  grid-gap: ", ";\n  align-items: center;\n"])), space(1));
var IconWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  justify-content: flex-start;\n  display: flex;\n  cursor: pointer;\n"], ["\n  justify-content: flex-start;\n  display: flex;\n  cursor: pointer;\n"])));
var Text = styled(TextOverflow)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n  line-height: 30px;\n"], ["\n  color: ", ";\n  line-height: 30px;\n"])), function (p) { return p.theme.gray700; });
var Key = styled(Text)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  visibility: hidden;\n  position: relative;\n  :after {\n    position: absolute;\n    top: 4px;\n    left: 0;\n    content: '", "';\n    visibility: visible;\n    ", ";\n  }\n"], ["\n  visibility: hidden;\n  position: relative;\n  :after {\n    position: absolute;\n    top: 4px;\n    left: 0;\n    content: '", "';\n    visibility: visible;\n    ", ";\n  }\n"])), function (p) { return p.content; }, overflowEllipsis);
var Actions = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto 1fr;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: auto 1fr;\n  grid-gap: ", ";\n  align-items: center;\n"])), space(1));
var Name = styled(Actions)(templateObject_7 || (templateObject_7 = __makeTemplateObject([""], [""])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=relays.jsx.map