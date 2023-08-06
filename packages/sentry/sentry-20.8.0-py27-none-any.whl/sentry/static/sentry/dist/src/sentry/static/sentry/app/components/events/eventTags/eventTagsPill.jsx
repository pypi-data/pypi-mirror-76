import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { Link } from 'react-router';
import * as queryString from 'query-string';
import AnnotatedText from 'app/components/events/meta/annotatedText';
import DeviceName from 'app/components/deviceName';
import { isUrl } from 'app/utils';
import Pill from 'app/components/pill';
import VersionHoverCard from 'app/components/versionHoverCard';
import TraceHoverCard from 'app/utils/discover/traceHoverCard';
import Version from 'app/components/version';
import { IconOpen, IconInfo } from 'app/icons';
var EventTagsPill = function (_a) {
    var tag = _a.tag, query = _a.query, orgId = _a.orgId, projectId = _a.projectId, streamPath = _a.streamPath, releasesPath = _a.releasesPath, meta = _a.meta, location = _a.location, hasQueryFeature = _a.hasQueryFeature;
    var locationSearch = "?" + queryString.stringify(query);
    var isRelease = tag.key === 'release';
    var isTrace = tag.key === 'trace';
    return (<Pill key={tag.key} name={tag.key} value={tag.value}>
      <Link to={{
        pathname: streamPath,
        search: locationSearch,
    }}>
        {isRelease ? (<Version version={tag.value} anchor={false} tooltipRawVersion truncate/>) : (<DeviceName value={tag.value}>
            {function (deviceName) { return <AnnotatedText value={deviceName} meta={meta}/>; }}
          </DeviceName>)}
      </Link>
      {isUrl(tag.value) && (<a href={tag.value} className="external-icon">
          <StyledIconOpen size="xs"/>
        </a>)}
      {isRelease && (<div className="pill-icon">
          <VersionHoverCard orgSlug={orgId} projectSlug={projectId} releaseVersion={tag.value}>
            <Link to={{
        pathname: "" + releasesPath + tag.value + "/",
        search: locationSearch,
    }}>
              <StyledIconInfo size="xs"/>
            </Link>
          </VersionHoverCard>
        </div>)}
      {isTrace && hasQueryFeature && (<TraceHoverCard containerClassName="pill-icon" traceId={tag.value} orgId={orgId} location={location}>
          {function (_a) {
        var to = _a.to;
        return (<Link to={to}>
                <StyledIconOpen size="xs"/>
              </Link>);
    }}
        </TraceHoverCard>)}
    </Pill>);
};
var StyledIconInfo = styled(IconInfo)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  top: 1px;\n"], ["\n  position: relative;\n  top: 1px;\n"])));
var StyledIconOpen = styled(IconOpen)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: relative;\n  top: 1px;\n"], ["\n  position: relative;\n  top: 1px;\n"])));
export default EventTagsPill;
var templateObject_1, templateObject_2;
//# sourceMappingURL=eventTagsPill.jsx.map