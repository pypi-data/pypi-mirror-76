import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import classNames from 'classnames';
import { IconClose } from 'app/icons/iconClose';
import { callIfFunction } from 'app/utils/callIfFunction';
import { IconSearch } from 'app/icons';
var SearchBar = /** @class */ (function (_super) {
    __extends(SearchBar, _super);
    function SearchBar() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            query: _this.props.query || _this.props.defaultQuery,
            dropdownVisible: false,
        };
        _this.searchInputRef = React.createRef();
        _this.blur = function () {
            if (_this.searchInputRef.current) {
                _this.searchInputRef.current.blur();
            }
        };
        _this.onSubmit = function (evt) {
            evt.preventDefault();
            _this.blur();
            _this.props.onSearch(_this.state.query);
        };
        _this.clearSearch = function () {
            _this.setState({ query: _this.props.defaultQuery }, function () {
                _this.props.onSearch(_this.state.query);
                callIfFunction(_this.props.onChange, _this.state.query);
            });
        };
        _this.onQueryFocus = function () {
            _this.setState({
                dropdownVisible: true,
            });
        };
        _this.onQueryBlur = function () {
            _this.setState({ dropdownVisible: false });
        };
        _this.onQueryChange = function (evt) {
            var value = evt.target.value;
            _this.setState({ query: value });
            callIfFunction(_this.props.onChange, value);
        };
        return _this;
    }
    SearchBar.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        if (nextProps.query !== this.props.query) {
            this.setState({
                query: nextProps.query,
            });
        }
    };
    SearchBar.prototype.render = function () {
        var _a = this.props, className = _a.className, width = _a.width;
        return (<div className={classNames('search', className)}>
        <form className="form-horizontal" onSubmit={this.onSubmit}>
          <div>
            <Input type="text" className="search-input form-control" placeholder={this.props.placeholder} name="query" ref={this.searchInputRef} autoComplete="off" value={this.state.query} onBlur={this.onQueryBlur} onChange={this.onQueryChange} width={width}/>
            <StyledIconSearch className="search-input-icon" size="sm" color="gray500"/>
            {this.state.query !== this.props.defaultQuery && (<div>
                <a className="search-clear-form" onClick={this.clearSearch}>
                  <IconClose />
                </a>
              </div>)}
          </div>
        </form>
      </div>);
    };
    SearchBar.defaultProps = {
        query: '',
        defaultQuery: '',
        onSearch: function () { },
    };
    return SearchBar;
}(React.PureComponent));
var Input = styled('input')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  width: ", ";\n"], ["\n  width: ", ";\n"])), function (p) { return (p.width ? p.width : undefined); });
var StyledIconSearch = styled(IconSearch)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: absolute;\n  top: 50%;\n  transform: translateY(-50%);\n  left: 14px;\n"], ["\n  position: absolute;\n  top: 50%;\n  transform: translateY(-50%);\n  left: 14px;\n"])));
export default SearchBar;
var templateObject_1, templateObject_2;
//# sourceMappingURL=searchBar.jsx.map