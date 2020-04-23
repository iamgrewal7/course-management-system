import React, { Component } from "react";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";

import CourseInfo from "./CourseInfo";
import Profile from "./Profile";
import Assignment from "./Assignment";
import Forum from "./Forum";
import Class from "./Class";
import { getStatus } from "../utils/status";

export default class Header extends Component {
  state = {
    isFaculty: false,
    loaded: false
  };

  handleChangePassword = () =>
    (window.location.href = "http://localhost:8000/change-password/");

  handleLogout = () => (window.location.href = "http://localhost:8000/logout/");

  componentDidMount() {
    this.isFaculty();
  }

  isFaculty = async () => {
    this.setState({ isFaculty: await getStatus(), loaded: true });
  };

  render() {
    return (
      <Router>
        <div className="ui secondary pointing menu">
          <Link className="item" to="/">
            Profile
          </Link>
          <Link className="item" to="/course-info">
            Courses
          </Link>
          <Link className="item" to="/assignments">
            Assignments/Exams
          </Link>
          <Link className="item" to="/forum">
            Forum
          </Link>
          {this.state.loaded & this.state.isFaculty ? (
            <Link className="item" to="/class">
              Class
            </Link>
          ) : null}
          <div className="right menu">
            <a className="ui item" onClick={this.handleLogout}>
              Logout
            </a>
            <a className="ui item" onClick={this.handleChangePassword}>
              Change Password
            </a>
          </div>
        </div>
        <Switch>
          <Route path="/course-info">
            <CourseInfo />
          </Route>
          <Route path="/assignments">
            <Assignment />
          </Route>
          <Route path="/forum">
            <Forum />
          </Route>
          <Route path="/class">
            <Class />
          </Route>
          <Route path="/">
            <Profile />
          </Route>
        </Switch>
      </Router>
    );
  }
}
