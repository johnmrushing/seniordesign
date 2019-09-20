import React, {Component} from 'react';
import Container from 'react-bootstrap/Container'
import Col from 'react-bootstrap/Col'
import Row from 'react-bootstrap/Row'
import {TelemetryCard} from "./TelemetryCard";


export class Telemetry extends Component {
    constructor(props) {
        super(props);
        this.state = {
            rawData: this.props.rawData
        };
    }

    render() {
        return (
            <div>
                <Container>
                    <Row className="justify-content-md-center">
                        <Col>
                            <TelemetryCard possibleCodes = {this.props.possibleCodes} rawData = {this.props.rawData}/>
                        </Col>
                        <Col>
                            <TelemetryCard possibleCodes = {this.props.possibleCodes} rawData = {this.props.rawData}/>
                        </Col>
                        <Col>
                            <TelemetryCard possibleCodes = {this.props.possibleCodes} rawData = {this.props.rawData}/>
                        </Col>
                    </Row>
                    <br/>
                    <Row className="justify-content-md-center">
                        <Col>
                            <TelemetryCard possibleCodes = {this.props.possibleCodes} rawData = {this.props.rawData}/>
                        </Col>
                        <Col>
                            <TelemetryCard possibleCodes = {this.props.possibleCodes} rawData = {this.props.rawData}/>
                        </Col>
                        <Col>
                            <TelemetryCard possibleCodes = {this.props.possibleCodes} rawData = {this.props.rawData}/>
                        </Col>
                    </Row>
                </Container>
            </div>
        )
    }


}


