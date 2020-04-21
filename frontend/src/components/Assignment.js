import React, { Component } from "react";
import { Accordion, Icon, Segment, Card } from "semantic-ui-react";

export default class Assignment extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      loaded: false,
      activeIndex: -1,
      placeholder: "Loading"
    };
  }

  componentDidMount() {
    fetch("http://localhost:8000/api/assignment/get/")
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

  getAssignments = (assignments) => (
    <div>
      {assignments.map((assignment) => (
        <Card
          key={assignment.id}
          header={assignment.name}
          meta={"Grade -> " + assignment.grade}
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

  render() {
    const { activeIndex } = this.state;
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
                {data.course}
              </Accordion.Title>
              <Accordion.Content active={activeIndex === idx}>
                {this.getAssignments(data.assignments)}
                <br />
              </Accordion.Content>
            </Accordion>
          </Segment>
        ))}
      </div>
    );
  }
}
