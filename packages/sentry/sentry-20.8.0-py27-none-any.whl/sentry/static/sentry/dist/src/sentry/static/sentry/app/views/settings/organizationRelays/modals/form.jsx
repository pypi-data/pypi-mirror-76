import { __awaiter, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import QuestionTooltip from 'app/components/questionTooltip';
import Input from 'app/views/settings/components/forms/controls/input';
import Textarea from 'app/views/settings/components/forms/controls/textarea';
import Field from 'app/views/settings/components/forms/field';
import TextCopyInput from 'app/views/settings/components/forms/textCopyInput';
import space from 'app/styles/space';
var Form = function (_a) {
    var values = _a.values, onChange = _a.onChange, errors = _a.errors, onValidate = _a.onValidate, disables = _a.disables, onValidateKey = _a.onValidateKey;
    var handleChange = function (field) { return function (event) {
        onChange(field, event.target.value);
    }; };
    // code below copied from src/sentry/static/sentry/app/views/organizationIntegrations/SplitInstallationIdModal.tsx
    // TODO: fix the common method selectText
    var onCopy = function (value) { return function () { return __awaiter(void 0, void 0, void 0, function () { return __generator(this, function (_a) {
        switch (_a.label) {
            case 0: 
            //This hack is needed because the normal copying methods with TextCopyInput do not work correctly
            return [4 /*yield*/, navigator.clipboard.writeText(value)];
            case 1: 
            //This hack is needed because the normal copying methods with TextCopyInput do not work correctly
            return [2 /*return*/, _a.sent()];
        }
    }); }); }; };
    return (<React.Fragment>
      <Field flexibleControlStateSize label={t('Display Name')} error={errors.name} inline={false} stacked>
        <Input type="text" name="name" onChange={handleChange('name')} value={values.name} onBlur={onValidate('name')} disabled={disables.name}/>
      </Field>

      {disables.publicKey ? (<Field flexibleControlStateSize label={t('Relay Key')} inline={false} stacked>
          <TextCopyInput onCopy={onCopy(values.publicKey)}>
            {values.publicKey}
          </TextCopyInput>
        </Field>) : (<Field flexibleControlStateSize label={<Label>
              <div>{t('Relay Key')}</div>
              <QuestionTooltip position="top" size="sm" title={t('Only enter the Relay Key value from your credentials file. Never share the Secret key with Sentry or any third party')}/>
            </Label>} error={errors.publicKey} inline={false} stacked>
          <Input type="text" name="publicKey" onChange={handleChange('publicKey')} value={values.publicKey} onBlur={onValidateKey}/>
        </Field>)}
      <Field flexibleControlStateSize label={t('Description (Optional)')} inline={false} stacked>
        <Textarea name="description" onChange={handleChange('description')} value={values.description} disabled={disables.description}/>
      </Field>
    </React.Fragment>);
};
export default Form;
var Label = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: max-content max-content;\n  align-items: center;\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: max-content max-content;\n  align-items: center;\n"])), space(1));
var templateObject_1;
//# sourceMappingURL=form.jsx.map