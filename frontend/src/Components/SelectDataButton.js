import React, {Component} from 'react';
import Button from 'react-bootstrap/Button';
import {SelectDataModal} from "./SelectDataModal";


export class SelectDataButton extends Component {
    constructor(props) {
        super(props);
        this.handleClick = this.handleClick.bind(this);
        this.handleClose = this.handleClose.bind(this);
        this.handleSelect = this.handleSelect.bind(this);
        this.state = {
            show: false
        };
    }

    handleClick() {
        this.setState({
            show: true
        });
    }
    handleClose() {
        this.setState({
            show: false
        });
    }
    handleSelect(obj){
        this.props.selectedData(obj)
        this.setState({
            show: false
        });
    }

    render() {
        return (
            <div className={"settingsDiv"}>
                <Button variant="light" className = {"settings"} onClick={this.handleClick}>
                </Button>
                {
                    this.state.show ? <SelectDataModal show = {this.state.show} onClick = {this.handleClick} onClose = {this.handleClose} possibleCodes = {this.props.possibleCodes} onSelect = {this.handleSelect} selectedData = {this.props.selectedRawData}/> : null
                }
            </div>
        )
    }


}


