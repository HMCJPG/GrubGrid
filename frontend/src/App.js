import React, { useState, useEffect } from 'react';
import axios from 'axios';

const api = axios.create({ baseURL: 'http://localhost:8000' });

function Login({ setToken }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);
    const res = await api.post('/auth/login', params);
    setToken(res.data.access_token);
  };

  return (
    <div>
      <h2>Login</h2>
      <input placeholder="username" value={username} onChange={e => setUsername(e.target.value)} />
      <input type="password" placeholder="password" value={password} onChange={e => setPassword(e.target.value)} />
      <button onClick={handleLogin}>Login</button>
    </div>
  );
}

function Feed({ token }) {
  const [posts, setPosts] = useState([]);
  const [caption, setCaption] = useState('');
  const [imageUrl, setImageUrl] = useState('');

  useEffect(() => {
    api.get('/posts/feed').then(res => setPosts(res.data));
  }, []);

  const addPost = async () => {
    const res = await api.post('/posts/', { caption, image_url: imageUrl }, { headers: { Authorization: `Bearer ${token}` }});
    setPosts([res.data, ...posts]);
    setCaption('');
    setImageUrl('');
  };

  const like = async (id) => {
    const res = await api.post(`/posts/${id}/like`, {}, { headers: { Authorization: `Bearer ${token}` }});
    setPosts(posts.map(p => p.id === id ? { ...p, likes: Array(res.data.likes).fill(0) } : p));
  };

  const [commentText, setCommentText] = useState('');

  const comment = async (id) => {
    await api.post('/comments/', { post_id: id, text: commentText }, { headers: { Authorization: `Bearer ${token}` }});
    setCommentText('');
    // reload comments optional
  };

  return (
    <div>
      <h2>Feed</h2>
      <div>
        <input placeholder="caption" value={caption} onChange={e => setCaption(e.target.value)} />
        <input placeholder="image url" value={imageUrl} onChange={e => setImageUrl(e.target.value)} />
        <button onClick={addPost}>Add Post</button>
      </div>
      {posts.map(p => (
        <div key={p.id} style={{ border: '1px solid black', margin: '10px', padding: '10px' }}>
          <img src={p.image_url} alt={p.caption} style={{ maxWidth: '100%' }} />
          <p>{p.caption}</p>
          <button onClick={() => like(p.id)}>Like ({p.likes.length})</button>
          <div>
            <input placeholder="comment" value={commentText} onChange={e => setCommentText(e.target.value)} />
            <button onClick={() => comment(p.id)}>Comment</button>
          </div>
        </div>
      ))}
    </div>
  );
}

function App() {
  const [token, setToken] = useState(null);

  if (!token) {
    return <Login setToken={setToken} />;
  }
  return <Feed token={token} />;
}

export default App;
