import React, { useState,useEffect } from 'react';
import {useNavigate} from 'react-router-dom'; // Ensure React is imported correctly
import { TextField, Button, Typography, Container, Box } from '@mui/material';
// import ReactDOM,{flushSync} from 'react-dom';
import axios from 'axios';

export function Login(props) {
const [username, setUser] = useState('');
const [password, setPassword] = useState('');
const [login,setLogin] = useState(props.state);
const navigate = useNavigate();



// console.log(log
useEffect(()=>{
    if(login){
        navigate('/')
    }
    props.func(login)
},[login,navigate])

useEffect(()=>{
    setLogin(props.state)
},[props])

const handleSubmit = async (e) => {
e.preventDefault(); // Prevent default form submission
try {
const response = await axios.post('http://localhost:5000/submit', { user: username, passw: password })
if(response.data === 'success'){
    setLogin(true)
    console.log('success')
}
    // Handle response as needed
} catch (error) {
console.error(error);
alert('Error submitting data');
}
};

return (
    (login ? 
        <p>You are already logged in.</p>
    : 
    <div style={{display:'flex',alignItems:'center',justifyContent:'center',height:'90vh'}}>
        <Container component="main" maxWidth="xs" sx={{boxShadow:5,borderRadius:5}}>
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: 8 }}>
            <Typography component="h1" variant="h5">
            Log In
            </Typography>
            <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
            <TextField
            margin="normal"
            required
            fullWidth
            id="email"
            label="Username"
            name="email"
            autoComplete="email"
            autoFocus
            value={username}
            onChange={(e) => setUser(e.target.value)}
            />
            <TextField
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            />
            <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>
            Log In
            </Button>
            </Box>
            </Box>
            </Container>
            {/* {login ? 'true': 'false'} */}
    </div>)
    

);
}