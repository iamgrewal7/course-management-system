import React, { Component } from "react";
import { Accordion, Icon, Segment, Button, Input } from "semantic-ui-react";
import Post from "./Post";
import { getCsrfToken } from "../utils/crsftoken";

export default class Assignment extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      loaded: false,
      postText: "",
      commentText: "",
      activeIndex: -1,
      placeholder: "Loading"
    };
  }

  componentDidMount() {
    this.fetchInitialData();
  }

  fetchInitialData = () => {
    fetch("http://localhost:8000/api/forum/")
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

  handleClick = (e, titleProps) => {
    const { index } = titleProps;
    const { activeIndex } = this.state;
    const newIndex = activeIndex === index ? -1 : index;

    this.setState({ activeIndex: newIndex });
  };

  handleAddPost = async (forumID) => {
    const response = await fetch("http://localhost:8000/api/post/create/", {
      method: "POST",
      headers: {
        "X-CSRFToken": await getCsrfToken()
      },
      body: JSON.stringify({ forum_id: forumID, text: this.state.postText })
    });
    const result = await response.json();
    this.fetchInitialData();
  };

  handleAddComment = async (postID) => {
    const response = await fetch("http://localhost:8000/api/comment/add/", {
      method: "POST",
      headers: {
        "X-CSRFToken": await getCsrfToken()
      },
      body: JSON.stringify({ post_id: postID, text: this.state.commentText })
    });
    const result = await response.json();
    console.log(result);
    this.fetchInitialData();
  };

  handlePostChange = (e) => {
    this.setState({ postText: e.target.value });
    e.preventDefault();
  };

  handleCommentChange = (e) => {
    this.setState({ commentText: e.target.value });
    e.preventDefault();
  };

  render() {
    const { activeIndex } = this.state;
    return (
      <div style={{ padding: "10px" }}>
        {this.state.data.map((data, idx) => (
          <Segment key={data.id}>
            <Accordion>
              <Accordion.Title
                active={activeIndex === idx}
                index={idx}
                onClick={this.handleClick}
              >
                <Icon name="dropdown" />
                {data.course}
              </Accordion.Title>
              <Accordion.Content active={activeIndex === idx}>
                {data.posts.map((post) => (
                  <Post
                    key={post.id}
                    post={post}
                    handleAddComment={this.handleAddComment}
                    handleCommentChange={this.handleCommentChange}
                  />
                ))}
              </Accordion.Content>
              <Input
                placeholder="Add New Post..."
                name="post"
                onChange={this.handlePostChange}
              />
              <Button
                primary
                style={{ float: "right" }}
                onClick={() => this.handleAddPost(data.id)}
              >
                Add Post
              </Button>
            </Accordion>
          </Segment>
        ))}
      </div>
    );
  }
}
