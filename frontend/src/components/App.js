import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import { render } from "react-dom";

import CourseInfo from './CourseInfo';
import Profile from './Profile';

export default function App() {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to="/">Profile</Link>
            </li>
            <li>
              <Link to="/course-info">Course</Link>
            </li>
          </ul>
        </nav>

        <Switch>
          <Route path="/course-info">
            <CourseInfo />
          </Route>
          <Route path="/">
            <Profile />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}


const container = document.getElementById("app");
render(<App />, container);