import React from "react";
import { Button, Input } from "semantic-ui-react";

const Post = ({ post, handleAddComment, handleCommentChange }) => (
  <div>
    <h3>Original Post: </h3>
    <p>Text: {post.text}</p>
    <p>Author: {post.by}</p>
    <Input placeholder="Add Comment..." onChange={handleCommentChange} />
    <Button
      secondary
      onClick={() => handleAddComment(post.id)}
      style={{ float: "right" }}
    >
      Add Comment
    </Button>
    <h3>Comments: </h3>
    {post.comments.map((comment) => (
      <div key={comment.id}>
        <p>Text: {comment.text}</p>
        <p>Author: {comment.by}</p>
      </div>
    ))}
  </div>
);

export default Post;
