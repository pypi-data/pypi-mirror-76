import { __extends } from "tslib";
import React from 'react';
import upperFirst from 'lodash/upperFirst';
import { t } from 'app/locale';
import ContextBlock from 'app/components/events/contexts/contextBlock';
import ClippedBox from 'app/components/clippedBox';
var StateContextType = /** @class */ (function (_super) {
    __extends(StateContextType, _super);
    function StateContextType() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    StateContextType.prototype.getKnownData = function () {
        var primaryState = this.props.data.state;
        if (!primaryState) {
            return [];
        }
        return [
            {
                key: 'state',
                subject: t('State') + (primaryState.type ? " (" + upperFirst(primaryState.type) + ")" : ''),
                value: primaryState.value,
            },
        ];
    };
    StateContextType.prototype.render = function () {
        return (<ClippedBox clipHeight={250}>
        <ContextBlock knownData={this.getKnownData()}/>
      </ClippedBox>);
    };
    return StateContextType;
}(React.Component));
export default StateContextType;
//# sourceMappingURL=state.jsx.map