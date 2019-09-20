import React, {Component} from 'react';
import Button from 'react-bootstrap/Button'
import Modal from "react-bootstrap/Modal";


export class SettingsModal extends Component {
    constructor(props) {
        super(props);
        this.handleClick = this.handleClick.bind(this);
        this.handleClose = this.handleClose.bind(this);
        this.state = {
            display: "digital",
            data: this.props.data,
            show: true,
        };
    }

    handleClick() {
        this.setState({
            show: true
        });
    }
    handleClose() {
        this.setState({
            show: false
        });
    }

    render() {
        return (
            <div>

                <Modal show={this.state.show} onHide={this.handleClose} size="lg"
                       aria-labelledby="contained-modal-title-vcenter" centered>

                    <Modal.Header closeButton>
                        <Modal.Title id="contained-modal-title-vcenter">DB Deployment</Modal.Title>
                    </Modal.Header>

                    <Modal.Body>
                        Woohoo TESTTT!
                        <br/>
                        <br/>

                        <Button variant="primary" onClick={this.deployUpgrade}>
                            Upgrade DB
                        </Button>
                    </Modal.Body>

                    <Modal.Footer>
                        <Button variant="secondary" onClick={this.handleClose}>
                            Close
                        </Button>
                        <Button variant="primary" onClick={this.handleClose}>
                            Save Changes
                        </Button>

                    </Modal.Footer>
                </Modal>

            </div>
        )
    }


}


