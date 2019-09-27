import React, {Component} from 'react';
import Image from 'react-bootstrap/Image';
import img from './settings.png';
import Button from 'react-bootstrap/Button';
import {Tachometer} from "./Tachometer";
import {SettingsModal} from "./SettingsModal";


export class SettingsButton extends Component {
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
            <div>
                <Button variant="light" className = {"settings"} onClick={this.handleClick}>
                    <Image src={img} roundedCircle/>
                </Button>
                {
                    this.state.show ? <SettingsModal show = {this.state.show} onClick = {this.handleClick} onClose = {this.handleClose} possibleCodes = {this.props.possibleCodes} onSelect = {this.handleSelect}/> : null
                }
            </div>
        )
    }


}


