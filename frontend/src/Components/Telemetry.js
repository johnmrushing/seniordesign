import React, {Component} from 'react';
import Container from 'react-bootstrap/Container'
import Col from 'react-bootstrap/Col'
import Row from 'react-bootstrap/Row'
import {TelemetryCard} from "./TelemetryCard";


export class Telemetry extends Component {
    constructor(props) {
        super(props);
        this.state = {
            rpm: this.props.rpm,
            speed: this.props.speed,
        };
    }

    render() {
        return (
            <div>
                <Container>
                    <Row className="justify-content-md-center"  >
                        <Col>
                           <TelemetryCard data = {"Speed"}/>
                        </Col>
                        <Col>
                            <TelemetryCard data = {"Speed"}/>
                        </Col>
                        <Col>
                            <TelemetryCard data = {"Speed"}/>
                        </Col>
                    </Row>
                    <br/>
                    <Row className="justify-content-md-center"  >
                        <Col>
                            <TelemetryCard data = {"Speed"}/>
                        </Col>
                        <Col>
                            <TelemetryCard data = {"Speed"}/>
                        </Col>
                        <Col>
                            <TelemetryCard data = {"Speed"}/>
                        </Col>
                    </Row>
                </Container>
            </div>
        )
    }


}


