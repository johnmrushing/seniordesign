import React, {Component} from 'react';
import Card from 'react-bootstrap/Card';
import {SelectDataButton} from "./SelectDataButton";
import socketIOClient from "socket.io-client";
let socket = socketIOClient("http://localhost/");

export class TelemetryCard extends Component {
    constructor(props) {
        super(props);
        this.updateSelectedData = this.updateSelectedData.bind(this);
        this.state = {
            rawData: this.props.rawData,
            selectedData: null,
            units:{
                'Vehicle Speed': 'MPH',
                'Engine RPM': 'RPM',
                'Intake Air Temperature': '°C',
                'Engine Coolant Temperature': '°C',
                'Throttle Position': '%',
                'Evap System Vapor Pressure': 'Pa',
                'Maximum Value For Air Flow From Mass Air Flow Sensor': 'g/s',
                'Calculated Engine Load': '%',
                'Evap. System Vapor Pressure': 'Pa',
                'Ambient Air Temperature': '°C',
                'Oxygen Sensor 1: Voltage': 'V',
                'Oxygen Sensor 1: Short Term Fuel Trim': '%',
                'Oxygen Sensor 2: Voltage': 'V',
                'Oxygen Sensor 2: Short Term Fuel Trim': '%',
                'Oxygen Sensor 3: Voltage': 'V',
                'Oxygen Sensor 3: Short Term Fuel Trim': '%',
                'Oxygen Sensor 4: Voltage': 'V',
                'Oxygen Sensor 4: Short Term Fuel Trim': '%',
                'Oxygen Sensor 5: Voltage': 'V',
                'Oxygen Sensor 5: Short Term Fuel Trim': '%',
                'Oxygen Sensor 6: Voltage': 'V',
                'Oxygen Sensor 6: Short Term Fuel Trim': '%',
                'Oxygen Sensor 7: Voltage': 'V',
                'Oxygen Sensor 7: Short Term Fuel Trim': '%',
                'Oxygen Sensor 8: Voltage': 'V',
                'Oxygen Sensor 8: Short Term Fuel Trim': '%',
                'Oxygen Sensor 1 AB: Fuel-Air Equivalence Ratio': '',
                'Oxygen Sensor 1 CD: Voltage': 'V',
                'Oxygen Sensor 2 AB: Fuel-Air Equivalence Ratio': '',
                'Oxygen Sensor 2 CD: Voltage': 'V',
                'Oxygen Sensor 3 AB: Fuel-Air Equivalence Ratio': '',
                'Oxygen Sensor 3 CD: Voltage': 'V',
                'Oxygen Sensor 4 AB: Fuel-Air Equivalence Ratio': '',
                'Oxygen Sensor 4 CD: Voltage': 'V',
                'Oxygen Sensor 5 AB: Fuel-Air Equivalence Ratio': '',
                'Oxygen Sensor 5 CD: Voltage': 'V',
                'Oxygen Sensor 6 AB: Fuel-Air Equivalence Ratio': '',
                'Oxygen Sensor 6 CD: Voltage': 'V',
                'Oxygen Sensor 7 AB: Fuel-Air Equivalence Ratio': '',
                'Oxygen Sensor 7 CD: Voltage': 'V',
                'Oxygen Sensor 8 AB: Fuel-Air Equivalence Ratio': '',
                'Oxygen Sensor 8 CD: Voltage': 'V',
                'Oxygen Sensor 1 AB: Fuel-Air Equivalence Ratio 2': '',
                'Oxygen Sensor 1 CD: Current': 'mA',
                'Oxygen Sensor 2 AB: Fuel-Air Equivalence Ratio 2': '',
                'Oxygen Sensor 2 CD: Current': 'mA',
                'Oxygen Sensor 3 AB: Fuel-Air Equivalence Ratio 2': '',
                'Oxygen Sensor 3 CD: Current': 'mA',
                'Oxygen Sensor 4 AB: Fuel-Air Equivalence Ratio 2': '',
                'Oxygen Sensor 4 CD: Current': 'mA',
                'Oxygen Sensor 5 AB: Fuel-Air Equivalence Ratio 2': '',
                'Oxygen Sensor 5 CD: Current': 'mA',
                'Oxygen Sensor 6 AB: Fuel-Air Equivalence Ratio 2': '',
                'Oxygen Sensor 6 CD: Current': 'mA',
                'Oxygen Sensor 7 AB: Fuel-Air Equivalence Ratio 2': '',
                'Oxygen Sensor 7 CD: Current': 'mA',
                'Oxygen Sensor 8 AB: Fuel-Air Equivalence Ratio 2': '',
                'Oxygen Sensor 8 CD: Current': 'mA',
                'Maximum Value For Fuel-Air Equivalence Ratio': '',
                'Maximum Value For Oxygen Sensor Voltage': 'V',
                'Maximum Value For Oxygen Sensor Current': 'mA',
                'Maximum Value For Intake Manifold Absolute Pressure': 'kPa',
                'Short Term Secondary Oxygen Sensor Trim, A: Bank 1': '%',
                'Short Term Secondary Oxygen Sensor Trim, B: Bank 3': '%',
                'Long Term Secondary Oxygen Sensor Trim, A: Bank 1': '%',
                'Long Term Secondary Oxygen Sensor Trim, B: bank 3': '%',
                'Short Term Secondary Oxygen Sensor Trim, A: bank 2': '%',
                'Short Term Secondary Oxygen Sensor Trim, B: bank 4': '%',
                'Long Term Secondary Oxygen Sensor Trim, A: bank 2': '%',
                'Long Term Secondary Oxygen Sensor Trim, B: bank 4': '%',
                'Fuel-Air Commanded Equivalence Ratio': '',
                'Hybrid Battery Pack Remaining Life': '%',
                'Actual Engine-Percent Torque': '%',
                'Relative Accelerator Pedal Position': '%',
                'Distance Traveled Since Codes Cleared': 'km',
                'Drivers Demand Engine-Percent Torque': '%',
                'Engine Fuel Rate': 'L/h',
                'Absolute Evap System Vapor Pressure': 'kPa',
                'Run Time Since Engine Start': 'seconds',
                'Fuel Injection Timing': 'C',
                'Long Term Fuel Trim-Bank 1': '%',
                'Long Term Fuel Trim-Bank 2': '%',
                'Catalyst Temperature: Bank 1, Sensor 2': '°C',
                'Catalyst Temperature: Bank 1, Sensor 1': '°C',
                'Commanded Throttle Actuator': '%',
                'Warm-ups Since Codes Cleared': 'count',
                'Fuel Rail Pressure': 'kPa',
                'Fuel Rail Absolute Pressure': 'kPa',
                'Time Since Trouble Codes Cleared': 'minutes',
                'Commanded EGR': '%',
                'Ethanol Fuel Percent': '%',
                'Engine Reference Torque': 'Nm',
                'Time Run With MIL On': 'minutes',
                'Fuel Pressure': 'kPa',
                'Absolute Load Value': '%',
                'Absolute Throttle Position B': '%',
                'Absolute Throttle Position C': '%',
                'Monitor Status This Drive Cycle': '',
                'Control Module Voltage': 'V',
                'Absolute Barometric Pressure': 'kPa',
                'Relative Throttle Position': '%',
                'MAF Air Flow Rate': 'grams/sec',
                'Fuel Rail Gauge Pressure': 'kPa',
                'Catalyst Temperature: Bank 2, Sensor 1': '°C',
                'Catalyst Temperature: Bank 2, Sensor 2': '°C',
                'Timing Advance': '° before TDC',
                'Short Term Fuel Trim-Bank 1': '%',
                'Short Term Fuel Trim-Bank 2': '%',
                'Fuel Tank Level Input': '%',
                'Distance Traveled With Malfunction Indicator Lamp (MIL) On': 'km',
                'Commanded Evaporative Purge': '%',
                'Engine Oil Temperature': '°C',
                'EGR Error': '%',
            }
        };
    }

    updateSelectedData(obj){
        this.setState({selectedData:obj},() => {
            console.log(this.state.selectedData)
            console.log(this.props.listID)
            socket.emit('userSelectedCodes', {listID: this.props.listID, data: this.state.selectedData})
        });

    }


    render() {
        return (
            <Card className = {"card"}>
                <SelectDataButton possibleCodes = {this.props.possibleCodes} selectedRawData = {this.state.selectedData} selectedData = {this.updateSelectedData}/>
                {(this.state.selectedData!= null) ? <p>{this.state.selectedData}</p> :null}
                <Card.Body className={"cardBody"}>
                    {
                        (this.state.selectedData!= null && this.props.rawData!= undefined) ?
                            <p className={"font"}>
                                {
                                    <h2>{this.props.rawData[this.state.selectedData]}</h2>
                                }
                            </p>: "Click to Select Data"

                    }
                </Card.Body>
                <Card.Footer className = {"cardFooter"}>
                    <div>
                        <h7>{this.state.units[this.state.selectedData]}</h7>
                    </div>
                </Card.Footer>
            </Card>
        )
    }


}


