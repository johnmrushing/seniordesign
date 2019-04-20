import React, {Component} from 'react';
import ReactSpeedometer from "react-d3-speedometer"
import socketIOClient from "socket.io-client";
let socket = socketIOClient("http://localhost/");

export class Guage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            rpm: this.props.rpm,
            speed: this.props.speed,
        };
    }

    /*
     * custom namespace "test" is used to read new data
     * being emitted to the socket
     */
    componentDidMount() {
        let that = this;
        socket.on('obd-out',function(data) {
            that.setState({rpm: data[0]/1000,speed: data[1]});
        });
    }

    render() {
        return (
            <div>
                <p>RPM x 1000</p>
                {this.state.rpm}
                <ReactSpeedometer
                    maxValue={10}
                    value={this.state.rpm}
                    needleColor="black"
                    startColor="orange"
                    segments={10}
                    endColor="red"
                    needleTransition={"easeBackOut"}
                    ringWidth={40}
                    textColor={"red"}

                />
                <p>Speed </p>
                {this.state.speed}
                <ReactSpeedometer
                    maxValue={200}
                    value={this.state.speed}
                    needleColor="black"
                    startColor="orange"
                    segments={10}
                    endColor="red"
                    needleTransition={"easeBackOut"}
                    ringWidth={40}
                    textColor={"red"}

                />
            </div>
        )
    }


}


