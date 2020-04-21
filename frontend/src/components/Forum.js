import React, { Component } from "react";
import { render } from "react-dom";

export default class Forum extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      loaded: false,
      placeholder: "Loading"
    };
  }

  componentDidMount() {
    fetch('http://localhost:8000/api/forum')
      .then(response => {
        if (response.status > 400) {
          return this.setState(() => {
            return { placeholder: "Something went wrong!" };
          });
        }
        return response.json();
      })
      .then(data => {
        this.setState(() => {
          return {
            data: data.Result,
            loaded: true
          };
        });
      });
  }

  render() {
    return (
      <h1>Hello</h1>
    )
  }
}