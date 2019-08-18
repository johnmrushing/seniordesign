import React, {Component} from 'react';
import Card from 'react-bootstrap/Card';
import {SettingsButton} from "./SettingsButton";
import {Speedometer} from "./Speedometer";
import {Tachometer} from "./Tachometer";

export class TelemetryCard extends Component {
    constructor(props) {
        super(props);
        this.handleClick = this.handleClick.bind(this);
        this.state = {
            display: "digital",
            data: this.props.data,
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
                <Card style={{height: '17rem'}}>
                    <SettingsButton show = {this.handleClick}/>
                    {
                        //(this.state.show) ?  <p> ok</p> : null;
                        // (this.state.display === "digital") ? null:null

                        this.state.data === "Speed" ? <Speedometer/> : <Tachometer/>

                    }

                </Card>
            </div>
        )
    }


}


