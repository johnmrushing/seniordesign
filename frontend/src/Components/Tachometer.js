import React, {Component} from 'react';
import ReactSpeedometer from "react-d3-speedometer"
import socketIOClient from "socket.io-client";

let socket = socketIOClient("http://localhost/");

export class Tachometer extends Component {
    constructor(props) {
        super(props);
        this.state = {
            rpm: this.props.rpm,
        };
    }

    componentDidMount() {
        let that = this;
        socket.on('obd-out',function(data) {
            console.log(data)
            that.setState({rpm: data[0]});
        });
    }

    render() {
        return (
            <div>
                <Card style={{ height: '18rem' }}>
                    <p>RPM x 1000</p>
                    <ReactSpeedometer
                        maxValue={10}
                        value={this.state.rpm/100}
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

