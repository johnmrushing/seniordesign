import React, {Component} from 'react';
import Button from 'react-bootstrap/Button'
import socketIOClient from "socket.io-client";
let socket = socketIOClient("http://localhost/");


export class Header extends Component {

    constructor(props) {
        super(props);
        this.handleClick = this.handleClick.bind(this);
        this.handleStop = this.handleStop.bind(this);
        this.state = {
            disable : false
        }
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
                    <Button  variant="secondary">Settings</Button>&nbsp;&nbsp;
                    <Button  disabled={this.state.disable} onClick={this.handleClick} variant="primary">Begin Run</Button>&nbsp;&nbsp;
                    <Button  onClick={this.handleStop} variant="primary">Save</Button>
                </div>
                <div>
                    <header>
                        <h1>OBDII Data Logger</h1>
                    </header>
                </div>

                <br/>
            </div>
        )
    }


}


