import React, {Component} from 'react';
import Button from 'react-bootstrap/Button'
import Modal from "react-bootstrap/Modal";
import Badge from 'react-bootstrap/Badge'



export class SelectDataModal extends Component {
    constructor(props) {
        super(props);
        this.handleClick = this.handleClick.bind(this);
        this.handleClose = this.handleClose.bind(this);
        this.state = {
            display: "digital",
            data: this.props.data
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

                <Modal className={"settingModal"} show={this.props.show} onHide={this.handleClose} size="lg"
                       aria-labelledby="contained-modal-title-vcenter" centered>

                    <Modal.Header closeButton>
                        <Modal.Title className = {"Normalfont"} id="contained-modal-title-vcenter">Available Data</Modal.Title>
                    </Modal.Header>

                    <Modal.Body>

                        <h4 className = {"Normalfont"}>Select Data:</h4>
                        {
                            this.props.possibleCodes ?
                                (   <div  className={"test"}>
                                        {
                                            this.props.possibleCodes.map((obj) => {
                                                return (
                                                    <h6>
                                                        {
                                                            (obj === this.props.selectedData) ?
                                                                <Badge variant="success" onClick={() => {
                                                                    this.props.onSelect(obj)}}>
                                                                    {<h6>{obj}</h6>}
                                                                </Badge>
                                                                :
                                                                <Badge variant="primary" onClick={() => {
                                                                    this.props.onSelect(obj)}}>
                                                                    {<h6>{obj}</h6>}
                                                                </Badge>
                                                        }
                                                    </h6>
                                                )
                                            })}
                                    </div>
                                )
                                : (null)
                        }
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


