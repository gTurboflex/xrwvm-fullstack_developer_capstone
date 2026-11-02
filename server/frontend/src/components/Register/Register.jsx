import React, { useState } from 'react';
import Header from '../Header/Header';
import '../Login/Login.css';

export default function Register() {
  const [userName, setUserName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const register = async (event) => {
    event.preventDefault();
    const response = await fetch('/djangoapp/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ userName, email, password }),
    });
    const result = await response.json();
    if (response.ok && result.status === 'Authenticated') {
      sessionStorage.setItem('username', result.userName);
      window.location.assign('/');
    } else {
      setMessage(result.error || 'Registration failed');
    }
  };
  return <div><Header /><main className="login_panel"><h1>Register</h1>
    <form onSubmit={register}>
      <label>Username <input required value={userName} onChange={e => setUserName(e.target.value)} /></label>
      <label>Email <input type="email" value={email} onChange={e => setEmail(e.target.value)} /></label>
      <label>Password <input required type="password" minLength="8" value={password} onChange={e => setPassword(e.target.value)} /></label>
      <button type="submit">Create account</button>
      {message && <p role="alert">{message}</p>}
    </form>
    <a href="/login">Already registered? Sign in</a>
  </main></div>;
}
