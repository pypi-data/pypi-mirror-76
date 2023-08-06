import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import space from 'app/styles/space';
import TimeSince from 'app/components/timeSince';
import Button from 'app/components/button';
import { IconClock, IconDelete, IconDownload } from 'app/icons';
import ButtonBar from 'app/components/buttonBar';
import FileSize from 'app/components/fileSize';
import Confirm from 'app/components/confirm';
import Access from 'app/components/acl/access';
import Tooltip from 'app/components/tooltip';
import Tag from '../../components/tag';
var SourceMapsArtifactRow = function (_a) {
    var artifact = _a.artifact, onDelete = _a.onDelete, downloadUrl = _a.downloadUrl;
    var name = artifact.name, size = artifact.size, dateCreated = artifact.dateCreated, dist = artifact.dist, id = artifact.id;
    var handleDeleteClick = function () {
        onDelete(id);
    };
    return (<React.Fragment>
      <NameColumn>
        <Name>{name || "(" + t('empty') + ")"}</Name>
        <TimeAndDistWrapper>
          <TimeWrapper>
            <IconClock size="xs"/>
            <TimeSince date={dateCreated}/>
          </TimeWrapper>
          {dist && <Tag inline>{dist}</Tag>}
        </TimeAndDistWrapper>
      </NameColumn>
      <SizeColumn>
        <FileSize bytes={size}/>
      </SizeColumn>
      <ActionsColumn>
        <ButtonBar gap={0.5}>
          <Access access={['project:write']}>
            {function (_a) {
        var hasAccess = _a.hasAccess;
        return (<Tooltip title={t('You do not have the required permission to download this artifact.')} disabled={hasAccess}>
                <Button size="small" icon={<IconDownload size="sm"/>} disabled={!hasAccess} href={downloadUrl} title={t('Download Artifact')}/>
              </Tooltip>);
    }}
          </Access>
          <Confirm message={t('Are you sure you want to remove this artifact?')} onConfirm={handleDeleteClick}>
            <Button size="small" icon={<IconDelete size="sm"/>} title={t('Remove Artifact')}/>
          </Confirm>
        </ButtonBar>
      </ActionsColumn>
    </React.Fragment>);
};
var NameColumn = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  align-items: flex-start;\n  justify-content: center;\n"], ["\n  display: flex;\n  flex-direction: column;\n  align-items: flex-start;\n  justify-content: center;\n"])));
var SizeColumn = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  text-align: right;\n  align-items: center;\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  text-align: right;\n  align-items: center;\n"])));
var ActionsColumn = styled(SizeColumn)(templateObject_3 || (templateObject_3 = __makeTemplateObject([""], [""])));
var Name = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  padding-right: ", ";\n  overflow-wrap: break-word;\n  word-break: break-all;\n"], ["\n  padding-right: ", ";\n  overflow-wrap: break-word;\n  word-break: break-all;\n"])), space(4));
var TimeAndDistWrapper = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  width: 100%;\n  display: flex;\n  margin-top: ", ";\n  align-items: center;\n"], ["\n  width: 100%;\n  display: flex;\n  margin-top: ", ";\n  align-items: center;\n"])), space(1));
var TimeWrapper = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: min-content 1fr;\n  font-size: ", ";\n  color: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: min-content 1fr;\n  font-size: ", ";\n  color: ", ";\n"])), space(0.5), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray600; });
export default SourceMapsArtifactRow;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=sourceMapsArtifactRow.jsx.map