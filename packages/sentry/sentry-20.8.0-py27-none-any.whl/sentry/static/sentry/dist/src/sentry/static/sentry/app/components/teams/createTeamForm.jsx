import { __extends } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import Form from 'app/views/settings/components/forms/form';
import TextField from 'app/views/settings/components/forms/textField';
import slugify from 'app/utils/slugify';
var CreateTeamForm = /** @class */ (function (_super) {
    __extends(CreateTeamForm, _super);
    function CreateTeamForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleCreateTeamSuccess = function (data) {
            var onSuccess = _this.props.onSuccess;
            if (typeof onSuccess !== 'function') {
                return;
            }
            onSuccess(data);
        };
        return _this;
    }
    CreateTeamForm.prototype.render = function () {
        var organization = this.props.organization;
        return (<React.Fragment>
        <p>
          {t("Teams group members' access to a specific focus, e.g. a major product or application that may have sub-projects.")}
        </p>

        <Form submitLabel={t('Create Team')} apiEndpoint={"/organizations/" + organization.slug + "/teams/"} apiMethod="POST" onSubmit={this.props.onSubmit} onSubmitSuccess={this.handleCreateTeamSuccess} requireChanges data-test-id="create-team-form" {...this.props.formProps}>
          <TextField name="slug" label={t('Team Slug')} placeholder={t('e.g. operations, web-frontend, desktop')} help={t('May contain lowercase letters, numbers, dashes and underscores.')} required stacked flexibleControlStateSize inline={false} transformInput={slugify}/>
        </Form>
      </React.Fragment>);
    };
    return CreateTeamForm;
}(React.Component));
export default CreateTeamForm;
//# sourceMappingURL=createTeamForm.jsx.map