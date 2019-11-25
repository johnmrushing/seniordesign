import React, {Component} from 'react';

export class RPMGraph extends Component {
    constructor(props) {
        super(props);
        this.state = {
            rawData: this.props.rawData,
            width: 0
        };
    }

    componentDidMount() {
        if(this.props.rawData !== undefined){
            this.setState({
                width: ((1-(this.props.rawData["Engine RPM"]/9000))*100)*0.675
            });
        }
    }




    render() {
        return (
            <div>

                <div className={"RPMGraphSlider"} style={{width:this.state.width + "%"}}/>

                <div className={"RPMGraph"}>

                    <div className={"square1"}/>
                    <div className={"square1"}/>
                    <div className={"square1"}/>
                    <div className={"square1"}/>
                    <div className={"square1"}/>
                    <div className={"square2"}/>
                    <div className={"square3"}/>
                    <div className={"square3"}/>
                    <div className={"square3"}/>
                    <div className={"square3"}/>
                    <div className={"square3"}/>
                    <div className={"square3"}/>
                    <div className={"square3"}/>
                    <div className={"square3"}/>
                    <div className={"square3"}/>
                    <div className={"square4"}/>
                    <div className={"square5"}/>
                    <div className={"square5"}/>

                </div>
                <div className={"RPMGraphNumbers"}>
                    <div className={"square0text"}>0</div>
                    <div></div>
                    <div className={"square0text"}>1</div>
                    <div></div>
                    <div className={"square0text"}>2</div>
                    <div></div>
                    <div className={"square1text"}>3</div>
                    <div></div>
                    <div className={"square1text"}>4</div>
                    <div></div>
                    <div className={"square1text"}>5</div>
                    <div></div>
                    <div className={"square1text"}>6</div>
                    <div></div>
                    <div className={"square1text"}>7</div>
                    <div></div>
                    <div className={"square2text"}>8</div>
                    <div></div>
                    <div className={"square2text"}>9</div>
                </div>

            </div>
        )
    }


}


