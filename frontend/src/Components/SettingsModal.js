import React, {Component} from 'react';
import Button from 'react-bootstrap/Button'
import Modal from "react-bootstrap/Modal";
import Toggle from "react-toggle";
import DropdownButton from 'react-bootstrap/DropdownButton'
import Dropdown from 'react-bootstrap/Dropdown'
import socketIOClient from "socket.io-client";
let socket = socketIOClient("http://localhost/");


export class SettingsModal extends Component {
    constructor(props) {
        super(props);
        this.handleClick = this.handleClick.bind(this);
        this.handleClose = this.handleClose.bind(this);
        this.handleLayoutChange = this.handleLayoutChange.bind(this);
        this.handleVideoChange = this.handleVideoChange.bind(this);
        this.handleProfileSelect = this.handleProfileSelect.bind(this);
        this.state = {
            video: this.props.video,
            layout: this.props.layout,
            profileData: null,
            profile: this.props.profile
        };
    }

    handleClick() {
        this.props.onClick()
    }
    handleClose() {
        this.props.onClose()
    }

    handleLayoutChange() {
        if(this.state.layout === false){
            this.setState({
                layout: true
            });
        }
        else{
            this.setState({
                layout: false
            });
        }
        this.props.layoutSelect(this.state.layout)
    }
    handleVideoChange() {
        if(this.state.video === false){
            this.setState({
                video: true
            });
        }
        else{
            this.setState({
                video: false
            });
        }
        this.props.videoSelect(this.state.video)
    }

    componentDidMount() {
        let that = this;
        socket.on('frontEndProfiles',function(data) {
            console.log(data);
            that.setState({profileData: data});
        });
    }
    handleProfileSelect(data){
        console.log(data);
        this.setState({profile: data});
        this.props.profileSelect(data)
        socket.emit('getProfile', data);
    }

    render() {
        return (
            <div>

                <Modal className={"settingModal"} show={this.props.show} onHide={this.handleClose} size="lg"
                       aria-labelledby="contained-modal-title-vcenter" centered>
                    <Modal.Header closeButton>
                        <Modal.Title id="contained-modal-title-vcenter" className = {"Normalfont"}>Settings</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>

                        <h5 className = {"Normalfont"}>Profiles:</h5>
                        <div className={"ProfileButtons"}>
                            <DropdownButton id="dropdown-basic-button" title={"Profile " + this.state.profile}>
                                { (this.state.profileData !== null)?
                                    this.state.profileData.map((obj) => {
                                        return(
                                            <Dropdown.Item onSelect={() => this.handleProfileSelect(obj.replace('.json',""))}>Profile {obj.replace('.json',"")}</Dropdown.Item>
                                        )
                                    })
                                    :
                                    null
                                }
                            </DropdownButton>

                        </div>
                        <br/>
                        <Toggle icons={false} onChange={this.handleLayoutChange} defaultChecked={this.state.layout}/>
                        <label className={"label-text"}>Racing Layout</label>
                        <br/>
                        <br/>
                        <Toggle icons={false} onChange={this.handleVideoChange} defaultChecked={this.state.video}/>
                        <label className={"label-text"}>Record Video</label>
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


