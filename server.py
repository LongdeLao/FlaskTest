from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

# Path to the JSON file
DATA_FILE = 'posts.json'

def read_posts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []

def write_posts(posts):
    with open(DATA_FILE, 'w') as file:
        json.dump(posts, file, indent=4)

# Route to get all posts
@app.route('/posts', methods=['GET'])
def get_posts():
    posts = read_posts()
    return jsonify({'posts': posts})

# Route to get a specific post by id
@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    posts = read_posts()
    post = next((post for post in posts if post['id'] == post_id), None)
    if post:
        return jsonify({'post': post})
    return jsonify({'message': 'Post not found'}), 404

# Route to add a new post
@app.route('/posts', methods=['POST'])
def add_post():
    data = request.json
    if 'title' not in data or 'content' not in data:
        return jsonify({'message': 'Missing title or content'}), 400

    posts = read_posts()
    new_post = {
        'id': len(posts) + 1,
        'title': data['title'],
        'content': data['content']
    }
    posts.append(new_post)
    write_posts(posts)
    return jsonify({'message': 'Post added successfully', 'post': new_post}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
