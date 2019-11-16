import React, {Component} from 'react';
import Button from 'react-bootstrap/Button'
import socketIOClient from "socket.io-client";
import {SettingsModal} from "./SettingsModal";
let socket = socketIOClient("http://localhost/");


export class Header extends Component {

    constructor(props) {
        super(props);
        this.handleSettingsClick = this.handleSettingsClick.bind(this);
        this.handleSettingsClose = this.handleSettingsClose.bind(this);
        this.handleClick = this.handleClick.bind(this);
        this.handleStop = this.handleStop.bind(this);
        this.state = {
            disable : false,
            show: false
        }
    }
    handleSettingsClick(){
        this.setState({
            show: true
        });
    }
    handleSettingsClose(){
        this.setState({
            show: false
        });
    }
    handleClick(){
        socket.emit('begin', true)
        this.setState({disable:true})

    }

    handleStop(){
        socket.emit('end', true)
        this.setState({disable:false})

    }

    render() {
        return (
            <div className={"App-header"}>
                <br/>
                <div className={"float-left"}>
                    <Button  variant="secondary" onClick={this.handleSettingsClick}>Settings</Button>&nbsp;&nbsp;
                    <Button  disabled={this.state.disable} onClick={this.handleClick} variant="primary">Begin Run</Button>&nbsp;&nbsp;
                    <Button  onClick={this.handleStop} variant="primary">Save</Button>
                    {
                        this.state.show ? <SettingsModal show = {this.state.show} onClick = {this.handleSettingsClick} onClose = {this.handleSettingsClose}/> : null
                    }
                </div>
                <div>

                    <br></br>

                </div>

                <br/>
            </div>
        )
    }


}


