import React, {Component} from 'react';
import ReactSpeedometer from "react-d3-speedometer"
import socketIOClient from "socket.io-client";
import Card from 'react-bootstrap/Card';
let socket = socketIOClient("http://localhost/");

export class Speedometer extends Component {
    constructor(props) {
        super(props);
        this.state = {
            speed: this.props.speed,
        };
    }

    componentDidMount() {
        let that = this;
        socket.on('obd-out',function(data) {
            console.log(data)
            that.setState({speed: data[1]});
        });
    }

    render() {
        return (
            <div>
                <Card style={{ height: '18rem' }}>
                    <p>Speed </p>
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
                </Card>
            </div>
        )
    }

}


