import React, {Component} from 'react';
import Container from 'react-bootstrap/Container'
import Col from 'react-bootstrap/Col'
import Row from 'react-bootstrap/Row'
import {TelemetryCard} from "./TelemetryCard";
import {RPMGraph} from "./RPMGraph";


export class Telemetry extends Component {
    constructor(props) {
        super(props);
        this.state = {
            rawData: this.props.rawData,
        };
    }

    render() {
        return (
            <div>
                <Container className = {"container"}>
                    <Row className="justify-content-md-center">
                        <Col className = {"colsize"}>
                            <TelemetryCard layout = {this.props.layout} profile={this.props.profile} possibleCodes = {this.props.possibleCodes} rawData = {this.props.rawData} listID = {0} key = {0}/>
                        </Col>
                        <Col className = {"colsize"}>
                            <TelemetryCard layout = {this.props.layout} profile={this.props.profile} possibleCodes = {this.props.possibleCodes} rawData = {this.props.rawData} listID = {1} key = {1}/>
                        </Col>
                        <Col className = {"colsize"}>
                            <TelemetryCard layout = {this.props.layout} profile={this.props.profile} possibleCodes = {this.props.possibleCodes} rawData = {this.props.rawData} listID = {2} key = {2}/>
                        </Col>
                    </Row>

                        {
                            (this.props.layout === false) ?
                                <Row className="justify-content-md-center">
                                    <Col className = {"colsize"}>
                                        <TelemetryCard layout = {this.props.layout} profile={this.props.profile} possibleCodes = {this.props.possibleCodes} rawData = {this.props.rawData} listID = {4} key = {4}/>
                                    </Col>
                                    <Col className = {"colsize"}>
                                        <TelemetryCard layout = {this.props.layout} profile={this.props.profile} possibleCodes = {this.props.possibleCodes} rawData = {this.props.rawData} listID = {5} key = {5}/>
                                    </Col>
                                </Row>
                            :
                                <div>
                                    <br/>
                                    <br/>
                                    <br/>
                                    <Row className="justify-content-md-center">
                                        <RPMGraph listID = {3} key = {3}/>
                                    </Row>
                                </div>
                        }

                </Container>
            </div>
        )
    }


}


