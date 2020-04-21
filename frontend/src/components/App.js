import React, { Component } from "react";
import { render } from "react-dom";
import { Button } from 'semantic-ui-react'

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      loaded: false,
      placeholder: "Loading"
    };
  }

  componentDidMount() {
    fetch('http://localhost:8000/account/course-info')
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

  getCourse = offering => (
    <div>
      <p>Course Name: {offering.course.name} </p>
      <p>Course Number: {offering.course.number} </p>
      <p>Course Credit: {offering.course.credit} </p>
    </div>
  )

  getInstructor = instructors => (
    instructors.map((instructor, idx )=> (
      <div>
        <div>Instructor {idx+1}</div>
        <p>Name: {instructor.name}</p>
        <p>Email: {instructor.email}</p>
        <p>Office Address: {instructor.office}</p>
      </div>
    ))
  )

  getTa = tas => (
    <div>
      <h3>TAs: </h3>
      {tas.map((ta, idx) => (
        <div>
          <div>TA {idx+1}</div>
          <p>Name: {ta.name}</p>
          <p>Email: {ta.email}</p>
        </div>
      ))}
    </div>
  )

  render() {
    return (
      <ul>
        {this.state.data.map(offering => {
          return (
            <div>
              <Button>Click</Button>
              {this.getCourse(offering)}
              <p>Section: {offering.section} </p>
              <h3>Instructors: </h3>
              {this.getInstructor(offering.teaching_team.instructors)}
              {offering.teaching_team.tas.length ? this.getTa(offering.teaching_team.tas): ''}
              <br/>
            </div>
          )
        })}
      </ul>
    );
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);
