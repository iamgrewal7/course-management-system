import React, { Component } from "react";
import {
  Accordion,
  Icon,
  Segment,
  Card,
  Header,
  Button
} from "semantic-ui-react";
import { getCsrfToken } from "../utils/crsftoken";

export default class CourseInfo extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      activeIndex: -1,
      loaded: false,
      placeholder: "Loading"
    };
  }

  componentDidMount() {
    this.fetchInitialData();
  }

  fetchInitialData = () => {
    fetch("http://localhost:8000/api/course-info/")
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
  };

  dropCourse = async (courseID) => {
    const response = await fetch("http://localhost:8000/api/drop-course/", {
      method: "POST",
      headers: {
        "X-CSRFToken": await getCsrfToken()
      },
      body: JSON.stringify({ course_id: courseID })
    });
    const result = await response.json();
    alert(result.Result);
    this.fetchInitialData();
  };

  handleClick = (e, titleProps) => {
    const { index } = titleProps;
    const { activeIndex } = this.state;
    const newIndex = activeIndex === index ? -1 : index;

    this.setState({ activeIndex: newIndex });
  };

  getCourse = (offering) => (
    <Card
      header={offering.course.name}
      meta={"Section -> " + offering.section}
    />
  );

  getInstructor = (instructors) => (
    <div>
      <Header as="h3">Instructors</Header>
      {instructors.map((instructor, idx) => (
        <Card
          key={instructor.id}
          header={instructor.name}
          meta={"Email -> " + instructor.email}
          description={"Office -> " + instructor.office}
        />
      ))}
    </div>
  );

  getTa = (tas) => (
    <div>
      <Header as="h3">TAs</Header>
      {tas.map((ta, idx) => (
        <Card key={ta.id} header={ta.name} meta={"Email -> " + ta.email} />
      ))}
    </div>
  );

  render() {
    const { activeIndex } = this.state;
    return (
      <div style={{ padding: "10px" }}>
        {this.state.data.map((offering, idx) => {
          return (
            <Segment key={offering.id}>
              <Accordion>
                <Accordion.Title
                  active={activeIndex === 0}
                  index={idx}
                  onClick={this.handleClick}
                >
                  <Icon name="dropdown" />
                  {offering.course.number}
                </Accordion.Title>
                <Accordion.Content active={activeIndex === idx}>
                  {this.getCourse(offering)}
                  {this.getInstructor(offering.teaching_team.instructors)}
                  <br />
                  {offering.teaching_team.tas.length
                    ? this.getTa(offering.teaching_team.tas)
                    : ""}
                </Accordion.Content>
                <Button
                  color="red"
                  onClick={() => this.dropCourse(offering.course.id)}
                >
                  Drop This Course
                </Button>
              </Accordion>
            </Segment>
          );
        })}
      </div>
    );
  }
}
