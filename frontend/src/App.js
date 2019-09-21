import './App.css';
import React, { Component } from 'react';
import {Telemetry} from "./Components/Telemetry";
import {Header} from "./Components/Header";
import socketIOClient from "socket.io-client";
let socket = socketIOClient("http://localhost/");

export class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            rawData: null,
            possibleCodes: null,
        };
    }
    componentDidMount() {
        let that = this;
        that.setState({possibleCodes: ["Speed","RPM", "Throttle Position"]});
        socket.on('obd-out',function(data) {
            console.log(data);
            that.setState({rawData: data});
        });
        socket.on('possibleCodes',function(data) {
            console.log(data);
            that.setState({possibleCodes: data});
        });
    }
    render() {
        return (
          <div className="App">
              <Header/>
              <Telemetry rawData = {this.state.rawData} possibleCodes={this.state.possibleCodes}/>
          </div>
        );
  }
}

export default App;
