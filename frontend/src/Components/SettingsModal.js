import React, {Component} from 'react';
import Button from 'react-bootstrap/Button'
import Modal from "react-bootstrap/Modal";
import Form from 'react-bootstrap/Form'

export class SettingsModal extends Component {
    constructor(props) {
        super(props);
        this.handleClick = this.handleClick.bind(this);
        this.handleClose = this.handleClose.bind(this);
        this.state = {
            toggle: true
        };
    }

    handleClick() {
        this.props.onClick()
    }
    handleClose() {
        this.props.onClose()
    }

    render() {
        return (
            <div>

                <Modal show={this.props.show} onHide={this.handleClose} size="lg"
                       aria-labelledby="contained-modal-title-vcenter" centered>

                    <Modal.Header closeButton>
                        <Modal.Title id="contained-modal-title-vcenter">Settings</Modal.Title>
                    </Modal.Header>

                    <Modal.Body>
                        <p>add profile</p>
                        <Form>
                            <Form.Check
                                custom
                                onChange={(e) =>this.setState(prevState => ({
                                    toggle: !prevState.toggle
                                }))}
                                type="switch"
                                id="custom-switch"
                                label="Record Video"
                            />
                        </Form>
                        <p>turn recording off</p>
                        <p>autocross layout</p>
                        <p>darkmode</p>

                    </Modal.Body>

                    <Modal.Footer>
                        <Button variant="secondary" onClick={this.handleClose}>
                            Close
                        </Button>

                    </Modal.Footer>
                </Modal>

            </div>
        )
    }


}


