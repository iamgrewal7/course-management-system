import React, { Component } from "react";
import { Accordion, Icon, Segment, Table, Button } from "semantic-ui-react";
import { getCsrfToken } from "../utils/crsftoken";

const validKeys = new Set(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]);

export default class Class extends Component {
  state = {
    data: [],
    scores: {},
    activeIndex: -1
  };

  componentDidMount() {
    this.fetchInitialData();
  }

  fetchInitialData = async () => {
    const response = await fetch("http://localhost:8000/api/class/", {
      method: "GET"
    });

    const data = await response.json();
    this.setState({
      data: data.Result
    });
  };

  handleClick = (e, titleProps) => {
    const { index } = titleProps;
    const { activeIndex } = this.state;
    const newIndex = activeIndex === index ? -1 : index;

    this.setState({ activeIndex: newIndex });
  };

  handleChange = (e, assignmentId, studentId) => {
    if (validKeys.has(e.key)) {
      let curr = this.state.scores;
      if (!(studentId in curr)) {
        curr[studentId] = {};
      }
      if (!(assignmentId in curr[studentId])) {
        curr[studentId][assignmentId] = "";
      }
      curr[studentId][assignmentId] += e.key;
      this.setState({ scores: curr }, () => console.log(this.state.scores));
    }
  };

  ScorePostRequest = async (assignmentId, studentId, grade) => {
    const response = await fetch("http://localhost:8000/api/submit-score/", {
      method: "POST",
      headers: {
        "X-CSRFToken": await getCsrfToken()
      },
      body: JSON.stringify({
        assignment_id: assignmentId,
        student_id: studentId,
        grade: grade
      })
    });

    const result = await response.json();
  };

  handleSubmitScore = (studentId) => {
    Object.keys(this.state.scores[studentId]).forEach((key) => {
      this.ScorePostRequest(key, studentId, this.state.scores[studentId][key]);
    });
    this.fetchInitialData();
  };

  render() {
    const { activeIndex } = this.state;
    return (
      <div style={{ padding: "10px" }}>
        {this.state.data.map((offering, idx) => {
          return (
            <Segment key={offering.id}>
              <Accordion>
                <Accordion.Title
                  active={activeIndex === idx}
                  index={idx}
                  onClick={this.handleClick}
                >
                  <Icon name="dropdown" />
                  {offering.course.number + " Section: " + offering.section}
                </Accordion.Title>
                <Accordion.Content active={activeIndex === idx}>
                  <RenderTable
                    handleChange={this.handleChange}
                    handleSubmitScore={this.handleSubmitScore}
                    offering={offering}
                  />
                </Accordion.Content>
              </Accordion>
            </Segment>
          );
        })}
      </div>
    );
  }
}

const RenderTable = ({ offering, handleChange, handleSubmitScore }) => {
  return (
    <Table celled>
      <Table.Header>
        <Table.Row>
          <Table.HeaderCell>Name</Table.HeaderCell>
          <Table.HeaderCell>Email</Table.HeaderCell>
          {offering.assignments.map((assignment) => (
            <Table.HeaderCell key={assignment.id}>
              {assignment.name}
            </Table.HeaderCell>
          ))}
          <Table.HeaderCell>Action</Table.HeaderCell>
        </Table.Row>
      </Table.Header>

      <Table.Body>
        {offering.students.map((student) => (
          <Table.Row key={student.id}>
            <Table.Cell>{student.last_name}</Table.Cell>
            <Table.Cell>{student.email}</Table.Cell>
            {student.assignments.map((assignment) => (
              <Table.Cell
                ContentEditable="true"
                key={assignment.id}
                onKeyDown={(e) => handleChange(e, assignment.id, student.id)}
              >
                {assignment.grade}
              </Table.Cell>
            ))}
            <Table.Cell>
              <Button secondary onClick={() => handleSubmitScore(student.id)}>
                Update
              </Button>
            </Table.Cell>
          </Table.Row>
        ))}
      </Table.Body>
    </Table>
  );
};
