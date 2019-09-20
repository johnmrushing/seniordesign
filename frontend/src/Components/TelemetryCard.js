import React, {Component} from 'react';
import Card from 'react-bootstrap/Card';
import {SettingsButton} from "./SettingsButton";
import {Speedometer} from "./Speedometer";
import {Tachometer} from "./Tachometer";

export class TelemetryCard extends Component {
    constructor(props) {
        super(props);
        this.state = {
            rawData: this.props.rawData,
            selectedData: null,
        };
    }


    render() {
        return (
            <div>
                <Card style={{height: '17rem'}}>
                    <SettingsButton possibleCodes = {this.props.possibleCodes}/>
                    {


                    }
                </Card>
            </div>
        )
    }


}


