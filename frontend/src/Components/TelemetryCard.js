import React, {Component} from 'react';
import Card from 'react-bootstrap/Card';
import {SettingsButton} from "./SettingsButton";
import {Speedometer} from "./Speedometer";
import {Tachometer} from "./Tachometer";

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
        });

    }


    render() {
        return (
            <div>
                <Card style={{height: '17rem'}}>
                    <SettingsButton possibleCodes = {this.props.possibleCodes} selectedData = {this.updateSelectedData}/>
                    <Card.Body>
                        <Card.Title>{(this.state.selectedData!= null) ? this.state.selectedData:null}</Card.Title>
                        {

                            (this.state.selectedData!= null && this.state.rawData!= null)  ? <p>{this.state.rawData.selectedData}</p>: null
                        }
                    </Card.Body>
                </Card>
            </div>
        )
    }


}


