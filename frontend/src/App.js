import './App.css';
import React, { Component } from 'react';
import {Telemetry} from "./Components/Telemetry";
import {Header} from "./Components/Header";

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
        socket.on('obd-out',function(data) {
            console.log(data);
            that.setState({rawData: data});
        });
        socket.on('possibleCodes',function(possibleData) {
            console.log(possibleData);
            that.setState({possibleCodes: possibleData});
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
