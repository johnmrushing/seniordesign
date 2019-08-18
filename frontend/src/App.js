import './App.css';
import React, { Component } from 'react';
import {Telemetry} from "./Components/Telemetry";
import {Header} from "./Components/Header";

export class App extends Component {
  render() {
    return (
      <div className="App">
          <Header/>
          <Telemetry/>
      </div>
    );
  }
}

export default App;
