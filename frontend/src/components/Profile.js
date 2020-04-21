import React, { Component } from "react";

export default class Profile extends Component {
  state = {
    data: {},
    loaded: false,
    placeholder: "Loading"
  };

  componentDidMount() {
    fetch("http://localhost:8000/api/profile/")
      .then((response) => {
        if (response.status > 400) {
          return this.setState(() => {
            return { placeholder: "Something went wrong!" };
          });
        }
        return response.json();
      })
      .then((data) => {
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
      <div style={{ padding: "10px" }}>
        <h3>First Name: {this.state.data.firstName}</h3>
        <h3>Last Name: {this.state.data.lastName}</h3>
        <h3>Email: {this.state.data.email}</h3>
        <h3>Age: {this.state.data.age}</h3>
        <h3>Gender: {this.state.data.gender}</h3>
      </div>
    );
  }
}
