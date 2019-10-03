import React, {Component} from 'react';
import Card from 'react-bootstrap/Card';
import {SettingsButton} from "./SettingsButton";
import socketIOClient from "socket.io-client";
let socket = socketIOClient("http://localhost/");

export class TelemetryCard extends Component {
    constructor(props) {
        super(props);
        this.updateSelectedData = this.updateSelectedData.bind(this);
        this.state = {
            rawData: this.props.rawData,
            selectedData: null,
        };
    }

    updateSelectedData(obj){
        this.setState({selectedData:obj},() => {
            console.log(this.state.selectedData)
            socket.emit('userSelectedCodes', {index: this.props.key, data: this.state.selectedData})
        });

    }


    render() {
        return (
                <Card className = {"card"}>
                    <SettingsButton possibleCodes = {this.props.possibleCodes} selectedData = {this.updateSelectedData}/>
                    <Card.Title>{(this.state.selectedData!= null) ? <h6>{this.state.selectedData}</h6> :null}</Card.Title>
                    <Card.Body>
                        {
                            (this.state.selectedData!= null && this.props.rawData!= null) ?
                                <p className={"font"}>
                                {
                                    <h2>{this.props.rawData[this.state.selectedData]}</h2>
                                }
                                </p>: 0

                        }
                    </Card.Body>
                </Card>
        )
    }


}


