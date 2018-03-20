import React, {Component} from 'react';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip } from 'recharts';
import fs from 'fs';

const data = [
    {name: 'Page A', passengers: 4000},
    {name: 'Page B', passengers: 3000},
    {name: 'Page C', passengers: 2000},
    {name: 'Page D', passengers: 2780},
    {name: 'Page E', passengers: 1890},
    {name: 'Page F', passengers: 2390},
    {name: 'Page G', passengers: 3490},
];

let test2 = 
<LineChart width={400} height={400} data={data} margin={{top: 5, right: 30, left: 20, bottom: 5}}>
  <Line type="monotone" dataKey="passengers" stroke="#8884d8" />
  <CartesianGrid stroke="#ccc" strokeDasharray="5 5"/>
  <XAxis dataKey="name" />
  <YAxis />
  <Tooltip />
</LineChart>

export default class App extends Component {
    
    componentDidMount() {
        var fs = require("fs");
        var text = fs.readFileSync("./mytext.txt", "utf-8");
        var textByLine = text.split("\n")
        conslole.log("This is a test: ", textByLine);
    }

    render () {
        return (
            test2
          )
    }
}