import React, {Component} from 'react';
import Image from 'react-bootstrap/Image'
import img from './settings.png'
import Button from 'react-bootstrap/Button'


export class SettingsButton extends Component {
    constructor(props) {
        super(props);

    }


    render() {
        return (
            <div>

                <Button variant="light" className = {"settings"} onClick={this.props.show}>
                    <Image src={img} roundedCircle/>
                </Button>

            </div>
        )
    }


}


