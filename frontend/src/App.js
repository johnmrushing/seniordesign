import React, { Component } from 'react';
import './App.css';
import {Guage} from "./Guage";

export class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h1>OBDII data stream test</h1>
        </header>
          <Guage/>
      </div>
    );
  }

}

export default App;
