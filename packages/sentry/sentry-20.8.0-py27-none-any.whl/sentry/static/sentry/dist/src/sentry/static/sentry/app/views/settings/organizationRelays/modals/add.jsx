import { __extends, __read, __spread } from "tslib";
import { t } from 'app/locale';
import ModalManager from './modalManager';
var Add = /** @class */ (function (_super) {
    __extends(Add, _super);
    function Add() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Add.prototype.getTitle = function () {
        return t('New Relay Key');
    };
    Add.prototype.getData = function () {
        var savedRelays = this.props.savedRelays;
        var trustedRelays = __spread(savedRelays, [this.state.values]);
        return { trustedRelays: trustedRelays };
    };
    return Add;
}(ModalManager));
export default Add;
//# sourceMappingURL=add.jsx.map