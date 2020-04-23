import React, { Component } from "react";
import {
  Accordion,
  Icon,
  Segment,
  Card,
  Button,
  Input
} from "semantic-ui-react";
import { getCsrfToken } from "../utils/crsftoken";

export default class Assignment extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      loaded: false,
      activeIndex: -1,
      assignmentText: "",
      token: "",
      placeholder: "Loading"
    };
  }

  componentDidMount() {
    this.fetchInitialData();
  }

  fetchInitialData = async () => {
    const response = await fetch("http://localhost:8000/api/assignment/get/", {
      method: "GET"
    });
    const data = await response.json();
    this.setState({
      data: data.Result,
      loaded: true
    });
  };

  getAssignments = (assignments, role) => (
    <div>
      {assignments.map((assignment) => (
        <Card
          key={assignment.id}
          header={assignment.name}
          meta={role.is_student ? " Grade -> " + assignment.grade : ""}
        />
      ))}
    </div>
  );

  handleClick = (e, titleProps) => {
    const { index } = titleProps;
    const { activeIndex } = this.state;
    const newIndex = activeIndex === index ? -1 : index;

    this.setState({ activeIndex: newIndex });
  };

  handleAddAssignment = async (offeringId) => {
    const response = await fetch(
      "http://localhost:8000/api/assignment/create/",
      {
        method: "POST",
        headers: {
          "X-CSRFToken": await getCsrfToken()
        },
        body: JSON.stringify({
          offering_id: offeringId,
          name: this.state.assignmentText
        })
      }
    );
    const result = await response.json();
    this.fetchInitialData();
  };

  handleAssignmentTextChange = (e) => {
    this.setState({ assignmentText: e.target.value });
    e.preventDefault();
  };

  render() {
    const { activeIndex } = this.state;
    if (!this.state.loaded) return <h1>loadi</h1>;
    return (
      <div style={{ padding: "10px" }}>
        {this.state.data.map((data, idx) => (
          <Segment key={data.id}>
            <Accordion>
              <Accordion.Title
                active={activeIndex === 0}
                index={idx}
                onClick={this.handleClick}
              >
                <Icon name="dropdown" />
                {data.course + " Section: " + data.section}
              </Accordion.Title>
              <Accordion.Content active={activeIndex === idx}>
                {this.getAssignments(data.assignments, data.role)}
                <br />
              </Accordion.Content>
              <AssignmentInput
                role={data.role}
                handleAssignmentTextChange={this.handleAssignmentTextChange}
                handleAddAssignment={this.handleAddAssignment}
                offeringId={data.offering_id}
              />
            </Accordion>
          </Segment>
        ))}
      </div>
    );
  }
}

const AssignmentInput = (props) => {
  if (!props.role.is_student) {
    return (
      <div>
        <Input
          placeholder="Add New assignment.."
          onChange={props.handleAssignmentTextChange}
        />
        <Button
          primary
          style={{ float: "right" }}
          onClick={() => props.handleAddAssignment(props.offeringId)}
        >
          Add Assignment
        </Button>
      </div>
    );
  }
  return null;
};
