import React, { Component } from "react";
import { render } from "react-dom";

export default class Profile extends Component{

    state = {
        data: {},
        loaded: false,
        placeholder: "Loading"
    };


    componentDidMount() {
        fetch('http://localhost:8000/api/profile')
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

    render(){
        return(
            <div>
                <p>First Name: {this.state.data.firstName}</p>
                <p>Last Name: {this.state.data.lastName}</p>
                <p>Email: {this.state.data.email}</p>
                <p>Age: {this.state.data.age}</p>
                <p>Gender: {this.state.data.gender}</p>
            </div>
        )
    }
}