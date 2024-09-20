import { useState,useEffect } from "react";
import {useNavigate} from 'react-router-dom';
import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';


export const Home = () =>{
    const [data, setData] = useState(null);
    const [cl,setCl] = useState({});
    const [ah,setAh] = useState([]);

    const nav = useNavigate();
    const navb = () =>{
        nav('/login')
    }
    
    useEffect(()=>{
        fetch('http://localhost:5000/')
        .then(response=>response.json())
        .then(data => {
            setData(data);
            setCl(data['client_list'])
            setAh(data['allowed_hosts'])
        })
        
        // .then(data=>{
        //     setCl(data['client_list']);
        //     setAh(data['allowed_hosts']);
        //     console.log(data)
    })
    return (
        <div style = {{ display:'flex',alignItems:'center',justifyContent:'center',height:'90vh'}}>
        <Paper sx={{ width: '50%', overflow: 'hidden'}}>
            <TableContainer sx={{ maxHeight: 440 }}>
                <Table stickyHeader aria-label="sticky table">
                <TableHead>
                    <TableRow>
                        <TableCell align="center">User Name</TableCell>
                        <TableCell align="center">Ip Address</TableCell>
                        <TableCell align="center">Mac Address</TableCell>
                        <TableCell align="center">Status</TableCell>
                    {/* {columns.map((column) => (
                        <TableCell
                        key={column.id}
                        align={column.align}
                        style={{ minWidth: column.minWidth }}
                        >
                        {column.label}
                        </TableCell>
                    ))} */}
                    </TableRow>
                </TableHead>
                <TableBody>
                    {cl.length > 0 && 
                    cl.map((value,index) =>(
                        <TableRow hover role="checkbox" tabIndex={-1} >
                            <TableCell align="right">{value.user_name}</TableCell>
                            <TableCell align="right">{value.ip}</TableCell>
                            <TableCell align="right">{value.mac}</TableCell>
                            <TableCell align="right">status</TableCell>
                        </TableRow>
                    ))}
                    {/* {rows
                    .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                    .map((row) => {
                        return (
                        <TableRow hover role="checkbox" tabIndex={-1} key={row.code}>
                            {columns.map((column) => {
                            const value = row[column.id];
                            return (
                                <TableCell key={column.id} align={column.align}>
                                {column.format && typeof value === 'number'
                                    ? column.format(value)
                                    : value}
                                </TableCell>
                            );
                            })}
                        </TableRow>
                        );
                    })} */}
                </TableBody>
                </Table>
            </TableContainer>
            {/* <TablePagination
                rowsPerPageOptions={[10, 25, 100]}
                component="div"
                count={rows.length}
                rowsPerPage={rowsPerPage}
                page={page}
                onPageChange={handleChangePage}
                onRowsPerPageChange={handleChangeRowsPerPage}
            /> */}
            </Paper>
            {/* <table>
                <th>
                    <td>User Name</td>
                    <td>Ip Address</td>
                    <td>Mac Address</td>
                    <td>Status</td>
                </th>
            {cl.length > 0 && 
            cl.map((value,index)=>(
                <tr>
                    <td>{value['user_name']}</td>
                    <td>{value['ip']}</td>
                    <td>{value['mac']}</td>
                </tr>
            ))}
            </table> */}
        </div>
    )
}