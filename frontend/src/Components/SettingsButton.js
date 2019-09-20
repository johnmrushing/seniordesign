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
        this.state = {
            show: false
        };
    }

    handleClick() {
        if(this.state.show) {
            this.setState({
                show: false
            });
        }
        else{
            this.setState({
                show: true
            });
        }
    }

    render() {
        return (
            <div>
                <Button variant="light" className = {"settings"} onClick={this.handleClick}>
                    <Image src={img} roundedCircle/>
                </Button>
                {
                    this.state.show ? <SettingsModal/> : null
                }
            </div>
        )
    }


}


