import { __extends, __makeTemplateObject, __read, __spread } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { components } from 'react-select';
import space from 'app/styles/space';
import InputField from 'app/views/settings/components/forms/inputField';
import FormFieldControlState from 'app/views/settings/components/forms/formField/controlState';
import FieldErrorReason from 'app/views/settings/components/forms/field/fieldErrorReason';
import SelectControl from 'app/components/forms/selectControl';
import IdBadge from 'app/components/idBadge';
import Button from 'app/components/button';
import { IconVercel, IconGeneric, IconDelete, IconOpen } from 'app/icons';
import ExternalLink from 'app/components/links/externalLink';
import { t } from 'app/locale';
import { removeAtArrayIndex } from 'app/utils/removeAtArrayIndex';
//Get the icon
var getIcon = function (iconType) {
    switch (iconType) {
        case 'vercel':
            return <IconVercel />;
        default:
            return <IconGeneric />;
    }
};
var RenderField = /** @class */ (function (_super) {
    __extends(RenderField, _super);
    function RenderField() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = { selectedSentryProjectId: null, selectedMappedValue: null };
        return _this;
    }
    RenderField.prototype.render = function () {
        var _this = this;
        var _a = this.props, onChange = _a.onChange, onBlur = _a.onBlur, incomingValues = _a.value, sentryProjects = _a.sentryProjects, _b = _a.mappedDropdown, mappedDropdownItems = _b.items, mappedValuePlaceholder = _b.placeholder, _c = _a.nextButton, nextUrl = _c.url, nextButtonText = _c.text, iconType = _a.iconType, model = _a.model, formElementId = _a.id, error = _a.error;
        var existingValues = incomingValues || [];
        var _d = this.state, selectedSentryProjectId = _d.selectedSentryProjectId, selectedMappedValue = _d.selectedMappedValue;
        // create maps by the project id for constant time lookups
        var sentryProjectsById = Object.fromEntries(sentryProjects.map(function (project) { return [project.id, project]; }));
        var mappedItemsByValue = Object.fromEntries(mappedDropdownItems.map(function (item) { return [item.value, item]; }));
        //build sets of values used so we don't let the user select them twice
        var projectIdsUsed = new Set(existingValues.map(function (tuple) { return tuple[0]; }));
        var mappedValuesUsed = new Set(existingValues.map(function (tuple) { return tuple[1]; }));
        var projectOptions = sentryProjects
            .filter(function (project) { return !projectIdsUsed.has(project.id); })
            .map(function (_a) {
            var slug = _a.slug, id = _a.id;
            return ({ label: slug, value: id });
        });
        var mappedItemsToShow = mappedDropdownItems.filter(function (item) { return !mappedValuesUsed.has(item.value); });
        var handleSelectProject = function (_a) {
            var value = _a.value;
            _this.setState({ selectedSentryProjectId: value });
        };
        var handleSelectMappedValue = function (_a) {
            var value = _a.value;
            _this.setState({ selectedMappedValue: value });
        };
        var handleAdd = function () {
            //add the new value to the list of existing values
            var projectMappings = __spread(existingValues, [
                [selectedSentryProjectId, selectedMappedValue],
            ]);
            //trigger events so we save the value and show the check mark
            onChange === null || onChange === void 0 ? void 0 : onChange(projectMappings, []);
            onBlur === null || onBlur === void 0 ? void 0 : onBlur(projectMappings, []);
            _this.setState({ selectedSentryProjectId: null, selectedMappedValue: null });
        };
        var handleDelete = function (index) {
            var projectMappings = removeAtArrayIndex(existingValues, index);
            //trigger events so we save the value and show the check mark
            onChange === null || onChange === void 0 ? void 0 : onChange(projectMappings, []);
            onBlur === null || onBlur === void 0 ? void 0 : onBlur(projectMappings, []);
        };
        var renderItem = function (itemTuple, index) {
            var _a = __read(itemTuple, 2), projectId = _a[0], mappedValue = _a[1];
            var project = sentryProjectsById[projectId];
            // TODO: add special formatting if deleted
            var mappedItem = mappedItemsByValue[mappedValue];
            return (<Item key={index}>
          {project ? (<StyledIdBadge project={project} avatarSize={20} displayName={project.slug} avatarProps={{ consistentWidth: true }}/>) : (<ItemValue>{t('Deleted')}</ItemValue>)}
          <MappedItemValue>
            {mappedItem ? (<React.Fragment>
                <IntegrationIconWrapper>{getIcon(iconType)}</IntegrationIconWrapper>
                {mappedItem.label}
                <StyledExternalLink href={mappedItem.url}>
                  <IconOpen />
                </StyledExternalLink>
              </React.Fragment>) : (t('Deleted'))}
          </MappedItemValue>
          <DeleteButton onClick={function () { return handleDelete(index); }} icon={<IconDelete color="gray500"/>} size="small" type="button" aria-label={t('Delete')}/>
        </Item>);
        };
        var customValueContainer = function (containerProps) {
            //if no value set, we want to return the default component that is rendered
            var project = sentryProjectsById[selectedSentryProjectId || ''];
            if (!project) {
                return <components.ValueContainer {...containerProps}/>;
            }
            return (<components.ValueContainer {...containerProps}>
          <IdBadge project={project} avatarSize={20} displayName={project.slug} avatarProps={{ consistentWidth: true }}/>
        </components.ValueContainer>);
        };
        var customOptionProject = function (projectProps) {
            var project = sentryProjectsById[projectProps.value];
            //Should never happen for a dropdown item
            if (!project) {
                return null;
            }
            return (<components.Option {...projectProps}>
          <IdBadge project={project} avatarSize={20} displayName={project.slug} avatarProps={{ consistentWidth: true }}/>
        </components.Option>);
        };
        var customMappedValueContainer = function (containerProps) {
            //if no value set, we want to return the default component that is rendered
            var mappedValue = mappedItemsByValue[selectedMappedValue || ''];
            if (!mappedValue) {
                return <components.ValueContainer {...containerProps}/>;
            }
            return (<components.ValueContainer {...containerProps}>
          <IntegrationIconWrapper>{getIcon(iconType)}</IntegrationIconWrapper>
          {mappedValue.label}
        </components.ValueContainer>);
        };
        var customOptionMappedValue = function (optionProps) {
            return (<components.Option {...optionProps}>
          <OptionWrapper>
            <IntegrationIconWrapper>{getIcon(iconType)}</IntegrationIconWrapper>
            {optionProps.label}
          </OptionWrapper>
        </components.Option>);
        };
        return (<Wrapper>
        {existingValues.map(renderItem)}
        <Item>
          <StyledSelectControl placeholder={t('Choose Sentry project\u2026')} name="project" openMenuOnFocus options={projectOptions} components={{
            Option: customOptionProject,
            ValueContainer: customValueContainer,
        }} onChange={handleSelectProject} value={selectedSentryProjectId}/>
          <StyledSelectControl placeholder={mappedValuePlaceholder} name="mappedDropdown" openMenuOnFocus options={mappedItemsToShow} components={{
            Option: customOptionMappedValue,
            ValueContainer: customMappedValueContainer,
        }} onChange={handleSelectMappedValue} value={selectedMappedValue}/>
          <StyledAddProjectButton type="button" disabled={!selectedSentryProjectId || !selectedMappedValue} size="small" priority="primary" onClick={handleAdd}>
            {t('Add Project')}
          </StyledAddProjectButton>
          <FieldControlWrapper>
            {formElementId && (<div>
                <FormFieldControlState model={model} name={formElementId}/>
                {error ? <StyledFieldErrorReason>{error}</StyledFieldErrorReason> : null}
              </div>)}
          </FieldControlWrapper>
          {nextUrl && (<StyledNextButton type="button" size="small" priority="default" icon={<IconOpen />} href={nextUrl} external>
              {nextButtonText}
            </StyledNextButton>)}
        </Item>
      </Wrapper>);
    };
    return RenderField;
}(React.Component));
export { RenderField };
var ProjectMapperField = function (props) { return (<StyledInputField {...props} resetOnError inline={false} stacked={false} hideControlState field={function (renderProps) { return <RenderField {...renderProps}/>; }}/>); };
export default ProjectMapperField;
var StyledSelectControl = styled(SelectControl)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  width: 272px;\n  margin-left: ", ";\n"], ["\n  width: 272px;\n  margin-left: ", ";\n"])), space(1.5));
var Item = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin: -1px;\n  border: 1px solid ", ";\n  display: flex;\n  align-items: center;\n  height: 60px;\n"], ["\n  margin: -1px;\n  border: 1px solid ", ";\n  display: flex;\n  align-items: center;\n  height: 60px;\n"])), function (p) { return p.theme.gray400; });
var ItemValue = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding: ", ";\n  margin-left: ", ";\n"], ["\n  padding: ", ";\n  margin-left: ", ";\n"])), space(0.5), space(2));
var MappedItemValue = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  padding: ", ";\n  position: absolute;\n  left: 300px;\n"], ["\n  display: flex;\n  padding: ", ";\n  position: absolute;\n  left: 300px;\n"])), space(0.5));
var DeleteButton = styled(Button)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  position: absolute;\n  right: ", ";\n"], ["\n  position: absolute;\n  right: ", ";\n"])), space(2));
var StyledIdBadge = styled(IdBadge)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(3));
var IntegrationIconWrapper = styled('span')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  margin-right: ", ";\n  display: flex;\n"], ["\n  margin-right: ", ";\n  display: flex;\n"])), space(0.5));
var StyledAddProjectButton = styled(Button)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(2));
var StyledNextButton = styled(Button)(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  position: absolute;\n  right: ", ";\n"], ["\n  position: absolute;\n  right: ", ";\n"])), space(2));
var StyledInputField = styled(InputField)(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var StyledExternalLink = styled(ExternalLink)(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(0.5));
var OptionWrapper = styled('div')(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  align-items: center;\n  display: flex;\n"], ["\n  align-items: center;\n  display: flex;\n"])));
var Wrapper = styled('div')(templateObject_13 || (templateObject_13 = __makeTemplateObject([""], [""])));
var FieldControlWrapper = styled('div')(templateObject_14 || (templateObject_14 = __makeTemplateObject(["\n  position: relative;\n  margin-left: ", ";\n"], ["\n  position: relative;\n  margin-left: ", ";\n"])), space(2));
var StyledFieldErrorReason = styled(FieldErrorReason)(templateObject_15 || (templateObject_15 = __makeTemplateObject(["\n  width: 100px;\n"], ["\n  width: 100px;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15;
//# sourceMappingURL=projectMapperField.jsx.map