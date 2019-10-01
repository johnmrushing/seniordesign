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
                            <TelemetryCard possibleCodes = {this.props.possibleCodes} rawData = {this.props.rawData} key = {0}/>
                        </Col>
                        <Col>
                            <TelemetryCard possibleCodes = {this.props.possibleCodes} rawData = {this.props.rawData} key = {1}/>
                        </Col>
                        <Col>
                            <TelemetryCard possibleCodes = {this.props.possibleCodes} rawData = {this.props.rawData} key = {2}/>
                        </Col>
                    </Row>
                    <br/>
                    <Row className="justify-content-md-center">
                        <Col>
                            <TelemetryCard possibleCodes = {this.props.possibleCodes} rawData = {this.props.rawData} key = {3}/>
                        </Col>
                        <Col>
                            <TelemetryCard possibleCodes = {this.props.possibleCodes} rawData = {this.props.rawData} key = {4}/>
                        </Col>
                        <Col>
                            <TelemetryCard possibleCodes = {this.props.possibleCodes} rawData = {this.props.rawData} key = {5}/>
                        </Col>
                    </Row>
                </Container>
            </div>
        )
    }


}


