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
        //that.setState({possibleCodes: ['Vehicle speed', 'Engine RPM' ,'Timing advance', 'Oxygen Sensor 2: Voltage', 'Catalyst Temperature: Bank 1, Sensor 2', 'Fuel-Air commanded equivalence ratio', 'Absolute Evap system Vapor Pressure', 'Run time since engine start', 'Distance traveled since codes cleared', 'Commanded evaporative purge', 'Long term fuel trim-Bank 1', 'Relative throttle position', 'Auxiliary input / output supported', 'Throttle position', 'Time since trouble codes cleared', 'Short term fuel trim-Bank 2', 'Short term fuel trim-Bank 1', 'Monitor status this drive cycle', 'Oxygen Sensor 5', 'MAF air flow rate', 'Monitor status since DTCs cleared', 'OBD standards this vehicle conforms to', 'Accelerator pedal position D', 'Catalyst Temperature: Bank 1, Sensor 1', 'Absolute throttle position B', 'Catalyst Temperature: Bank 2, Sensor 1', 'Calculated engine load', 'Control module voltage', 'Warm-ups since codes cleared', 'Absolute load value', 'Oxygen Sensor 1', 'Accelerator pedal position E', 'Catalyst Temperature: Bank 2, Sensor 2', 'Commanded throttle actuator', 'Absolute Barometric Pressure', 'Time run with MIL on', 'Distance traveled with malfunction indicator lamp (MIL) on', 'Intake air temperature', 'Fuel Type', 'Oxygen Sensor 6: Voltage', 'PIDs supported [61 - 80]', 'Fuel system status', 'Oxygen sensors present (in 2 banks)', 'Long term fuel trim-Bank 2']});
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
