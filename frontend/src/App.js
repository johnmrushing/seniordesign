import './App.css';
import React, { Component } from 'react';
import {Telemetry} from "./Components/Telemetry";
import {Header} from "./Components/Header";
import socketIOClient from "socket.io-client";
let socket = socketIOClient("http://localhost/");

export class App extends Component {
    constructor(props) {
        super(props);
        this.handleLayoutChange = this.handleLayoutChange.bind(this);
        this.handleVideoChange = this.handleVideoChange.bind(this);
        this.handleProfileChange= this.handleProfileChange.bind(this);
        this.state = {
            rawData:undefined,
            possibleCodes: undefined,
            layout: true,
            video : true,
            profile: 1,
            savedProfile: [{},{},{},{},{},{}]
        };
    }
    componentDidMount() {
        let that = this;
        socket.on('obd-out',function(data) {
            console.log(data);
            that.setState({rawData: JSON.parse(data)});
        });
        socket.on('frontEndPossibleCodes',function(data) {
            console.log(data);
            that.setState({possibleCodes: data});
            socket.emit('getProfile', that.state.profile);
        });
        socket.on('frontEndSavedProfile', function (data) {
            that.setState({savedProfile: data})
        })

    }
    handleProfileChange(data){
        this.setState({profile: data})

    }
    handleLayoutChange(layout) {
        if(layout === false){
            this.setState({
                layout: true
            });
        }
        else{
            this.setState({
                layout: false
            });
        }

    }
    handleVideoChange(video) {
        if(video === false){
            this.setState({video: true},() => {
            socket.emit('VideoSetting', this.state.video);
			});
        }
        else{
            this.setState({video: false},() => {
            socket.emit('VideoSetting', this.state.video);
			});
        }
		

    }
    render() {
        return (
            <div className="App">
                <Header profile={this.state.profile} video = {this.state.video} layout = {this.state.layout} profileSelect={this.handleProfileChange} layoutSelect ={this.handleLayoutChange} videoSelect={this.handleVideoChange}/>
                <Telemetry savedProfile = {this.state.savedProfile} profile = {this.state.profile} layout = {this.state.layout} rawData = {this.state.rawData} possibleCodes={this.state.possibleCodes}/>
            </div>
        );
    }
}

export default App;
