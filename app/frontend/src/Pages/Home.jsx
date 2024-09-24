import { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import Button from '@mui/material/Button';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import axios from 'axios';

export const Home = (props) => {
    const [login, setLogin] = useState(props.state);
    const [clientList, setClientList] = useState([]);
    const [allowedHosts, setAllowedHosts] = useState([]);
    const [clients, setClients] = useState([]);
    // const [count, setCount] = useState(0);

    const navigate = useNavigate();

    // Function to navigate to the login page
    const navigateToLogin = () => {
        navigate('/login');
    };

    // Check if a client is in the allowed hosts
    const isInAllowedHosts = (clientIp) => {
        return allowedHosts.includes(clientIp);
    };

    // Fetch data on component mount
    useEffect(() => {
        const fetchData = () =>{
            fetch('http://localhost:5000/')
                .then(response => response.json())
                .then(data => {
                    setClientList(data['client_list']);
                    setAllowedHosts(data['allowed_hosts']);
                    setClients(data['clients']);
                })
                .catch(error => console.error('Error fetching data:', error));
        }
        // console.log('hi')
        if (!login) {
            navigateToLogin();
        }
        fetchData(); // Initial fetch
        const intervalId = setInterval(fetchData, 1000); // Fetch data every 10 second
        return () => clearInterval(intervalId); // Cleanup on unmount
    },[login]);

    const result = async (state) =>{
        try{
            const response = await axios.post('http://localhost:5000/result',{ state: state});
            console.log(response);
        }
        catch(error){
            console.error(error);
        }
    }

    return (
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '90vh' }}>
            <Paper sx={{ width: '50%', overflow: 'hidden' }}>
                <TableContainer sx={{ maxHeight: 440 }}>
                    <Table stickyHeader aria-label="sticky table">
                        <TableHead>
                            <TableRow>
                                <TableCell align="center">User Name</TableCell>
                                <TableCell align="center">IP Address</TableCell>
                                <TableCell align="center">MAC Address</TableCell>
                                <TableCell align="center">Status</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {clients.length > 0 && 
                                clients.map((client, index) => {
                                    // Find client data based on IP address
                                    const clientData = clientList.find(c => c.ip === client);

                                    return (
                                        <TableRow hover role="checkbox" tabIndex={-1} key={index}>
                                            {isInAllowedHosts(client) && clientData ? (
                                                <>
                                                    <TableCell align="center">{clientData.user_name}</TableCell>
                                                    <TableCell align="center">{clientData.ip}</TableCell>
                                                    <TableCell align="center">{clientData.mac}</TableCell>
                                                    <TableCell align="center">Connected</TableCell>
                                                </>
                                            ) : (
                                                <>
                                                    <TableCell align="center">-</TableCell>
                                                    <TableCell align="center">{client}</TableCell>
                                                    <TableCell align="center">-</TableCell>
                                                    <TableCell align="center">
                                                        <Button variant="outlined" color="success" size='small' onClick={()=>{result('true')}}>Allow</Button>
                                                        <Button variant="outlined" color="error" size='small' onClick={()=>{result('false')}}>Block</Button> {/* Changed size to small */}
                                                    </TableCell>
                                                </>
                                            )}
                                        </TableRow>
                                    );
                                })
                            }
                        </TableBody>
                    </Table>
                </TableContainer>
            </Paper>
        </div>
    );
};