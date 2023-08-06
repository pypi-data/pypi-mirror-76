import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { IconCircle, IconCheckmark, IconFlag } from 'app/icons';
import Tooltip from 'app/components/tooltip';
import space from 'app/styles/space';
var PackageStatus = /** @class */ (function (_super) {
    __extends(PackageStatus, _super);
    function PackageStatus() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    PackageStatus.prototype.getIcon = function (status) {
        switch (status) {
            case 'success':
                return <IconCheckmark isCircled color="green500"/>;
            case 'empty':
                return <IconCircle />;
            case 'error':
            default:
                return <IconFlag color="red400"/>;
        }
    };
    PackageStatus.prototype.render = function () {
        var _a = this.props, status = _a.status, tooltip = _a.tooltip;
        var icon = this.getIcon(status);
        if (status === 'empty') {
            return null;
        }
        return (<Tooltip title={tooltip} disabled={!(tooltip && tooltip.length)}>
        <PackageStatusIcon>{icon}</PackageStatusIcon>
      </Tooltip>);
    };
    return PackageStatus;
}(React.Component));
export var PackageStatusIcon = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-left: ", ";\n  opacity: 0;\n"], ["\n  margin-left: ", ";\n  opacity: 0;\n"])), space(0.5));
export default PackageStatus;
var templateObject_1;
//# sourceMappingURL=packageStatus.jsx.map